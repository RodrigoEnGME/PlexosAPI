import { expect, test } from '@playwright/test';

const snapshot = {
  stage: 1,
  block: 1,
  as_of: '2023-01-01',
  study: { initial_year: 2023, stages: 228, blocks: 21, frequency: 'monthly', warnings: [], systems: [{ code: 'ur', name: 'Uruguay' }], layout: 'geographic map' },
  entities: [{
    id: '1', source_code: '800', name: 'Terra', technology: 'hydro', asset_type: 'hydro',
    bus: 800, capacity_mw: 100, source_file: 'chidrour.dat', source_line: 3,
    latitude: -32.9, longitude: -56, coordinate_status: 'bus-reference',
    lifecycle_status: 'existing', is_active: true, modifications: [],
  }, {
    id: '2', source_code: '301', name: 'Cambel EOL', technology: 'EOL', asset_type: 'renewable', bus: 800,
    capacity_mw: 25, source_file: 'cgndur.dat', source_line: 4, latitude: -32.9, longitude: -56,
    coordinate_status: 'bus-reference', lifecycle_status: 'existing', is_active: true, modifications: [],
  }],
  buses: [{ source_code: '800', name: 'Salto', latitude: -32.9, longitude: -56 }],
  circuits: [],
  maintenance: [],
  provenance: 'intermediate database snapshot',
};

test('system workspace loads API data and changes stage context', async ({ page }) => {
  await page.route(/\/api\/projects$/, async (route) => route.fulfill({ json: [{ id: 1, name: 'UY revision' }] }));
  await page.route(/\/api\/projects\/1\/revisions$/, async (route) => route.fulfill({ json: [{ id: 1, revision_number: 1, status: 'parsed', is_active: true }] }));
  await page.route(/\/api\/projects\/1\/analytics\/status$/, async (route) => route.fulfill({ json: { status: 'running', phase: 'profile statistics', progress: 40, processed_assets: 2, total_assets: 5, error: null } }));
  await page.route(/\/api\/projects\/1\/snapshot.*/, async (route) => {
    const url = new URL(route.request().url());
    await route.fulfill({ json: { ...snapshot, stage: Number(url.searchParams.get('stage') ?? 1) } });
  });
  await page.route(/\/api\/projects\/1\/assets\/1\/history.*/, async (route) => route.fulfill({ json: { series: [{ stage: 1, as_of: '2023-01-01', lifecycle_status: 'existing', is_active: true, capacity_available_mw: 100, events: [{ kind: 'modification', effective_date: '2023-01-01', source_file: 'mtermiur.dat', source_line: 4, fields: { capacity: '120' } }] }] } }));
  await page.route(/\/api\/projects\/1\/assets\/1\/profile-statistics$/, async (route) => route.fulfill({ json: { status: 'ready', grouping: 'daily hour', unit: 'MW', statistics: { mean: 50, p10: 20, p90: 80, min: 10, max: 90, stddev: 12, valid_count: 24 }, series: Array.from({ length: 24 }, (_, index) => ({ hour: index + 1, mean: 50, p10: 20, p90: 80, min: 10, max: 90, stddev: 12, valid_count: 1 })) } }));
  await page.route(/\/api\/projects\/1\/buses\/800\/demand.*/, async (route) => route.fulfill({ json: { bus_code: '800', bus_name: 'Salto', authority: 'DBF', selected_date: '2023-01-01', available_dates: ['2023-01-01'], records: [{ block: 1, demand_mw: 10, demand_code: '1', effective_date: '2023-01-01', source_file: 'dbf.dat', source_line: 2, value_kind: 'input' }], summary: { total_mw: 10, peak_mw: 10, block_count: 1 }, warnings: [], provenance: 'DBF test fixture' } }));
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /UY revision system view/i })).toBeVisible();
  await expect(page.getByRole('progressbar', { name: 'Historical data processing progress' })).toHaveAttribute('aria-valuenow', '40');
  await expect(page.getByText('Calculating historical profiles')).toBeVisible();
  await expect(page.getByLabel('FIND NODE')).toBeVisible();
  await page.getByLabel('FIND NODE').focus();
  await page.getByRole('option', { name: /BUS 800/ }).click();
  await expect(page.getByText('GENERATORS AT THIS NODE')).toBeVisible();
  await expect(page.getByText('NODE DEMAND')).toBeVisible();
  await page.getByRole('button', { name: /Terra/ }).click();
  await expect(page.getByRole('heading', { name: 'Terra' })).toBeVisible();
  await expect(page.locator('.capacity-history-chart')).toBeVisible();
  await expect(page.getByText('Potencia instalada: 120 MW')).toBeVisible();
  await expect(page.getByLabel('Months shown in capacity history')).toHaveValue('60');
  await expect(page.getByLabel('Y scale')).toHaveValue('absolute');
  await expect(page.getByText('P10-P90 empirical band')).toBeVisible();
  await expect(page.getByLabel('System')).toHaveValue('all');
  await page.getByLabel('System').selectOption('ur');
  await expect(page.getByLabel('System')).toHaveValue('ur');
  const themeButton = page.getByRole('button', { name: /Switch to (light|dark) theme/i });
  await expect(themeButton).toBeVisible();
  const themeLabel = await themeButton.getAttribute('aria-label');
  await themeButton.click();
  await expect(page.getByRole('button', { name: themeLabel?.includes('light') ? /Switch to dark theme/i : /Switch to light theme/i })).toBeVisible();
  await page.getByRole('slider', { name: 'Study stage' }).fill('22');
  await expect(page.locator('.timeline-meta').getByText('22', { exact: true })).toBeVisible();
  await page.locator('nav[aria-label="Workspace navigation"] button').nth(1).click();
  await expect(page.getByRole('heading', { name: 'Study imports' })).toBeVisible();
});

test('country context and derived topology appear without bus coordinates', async ({ page }) => {
  const peruSnapshot = { ...snapshot, study: { ...snapshot.study, systems: [{ code: 'pe', name: 'Peru', country_code: 'pe' }], layout: 'topology layout' }, entities: snapshot.entities.map((entity) => ({ ...entity, system_code: 'pe', latitude: null, longitude: null })), buses: [{ source_code: '800', name: 'Lima', system_code: 'pe', latitude: null, longitude: null }], circuits: [{ source_code: 'c1', from_bus: '800', to_bus: '800', name: 'local', system_code: 'pe' }] };
  await page.route(/\/api\/projects$/, async (route) => route.fulfill({ json: [{ id: 1, name: 'PE_BC' }] }));
  await page.route(/\/api\/projects\/1\/revisions$/, async (route) => route.fulfill({ json: [{ id: 1, revision_number: 1, status: 'ready', is_active: true }] }));
  await page.route(/\/api\/projects\/1\/snapshot.*/, async (route) => route.fulfill({ json: peruSnapshot }));
  await page.goto('/');
  await expect(page.getByText('Topology layout')).toBeVisible();
  await expect(page.getByText('DERIVED NETWORK VIEW')).toBeVisible();
  await expect(page.getByText('DERIVED TOPOLOGY · NOT GEOGRAPHIC')).toBeVisible();
});

test('demand-only nodes remain selectable without generators', async ({ page }) => {
  const demandOnlySnapshot = {
    ...snapshot,
    entities: [],
    buses: [{ source_code: '900', name: 'Load-only node', demand_mw: 18, latitude: -33.1, longitude: -55.8 }],
  };
  await page.route(/\/api\/projects$/, async (route) => route.fulfill({ json: [{ id: 1, name: 'Demand study' }] }));
  await page.route(/\/api\/projects\/1\/revisions$/, async (route) => route.fulfill({ json: [{ id: 1, revision_number: 1, status: 'ready', is_active: true }] }));
  await page.route(/\/api\/projects\/1\/snapshot.*/, async (route) => route.fulfill({ json: demandOnlySnapshot }));
  await page.route(/\/api\/projects\/1\/buses\/900\/demand.*/, async (route) => route.fulfill({ json: { bus_code: '900', bus_name: 'Load-only node', authority: 'DBF', selected_date: '2023-01-01', available_dates: ['2023-01-01'], available_blocks: [1, 2], demand_codes: ['1'], records: [{ block: 1, demand_mw: 18, demand_code: '1', effective_date: '2023-01-01', source_file: 'dbf.dat', source_line: 2, value_kind: 'input' }, { block: 2, demand_mw: 12, demand_code: '1', effective_date: '2023-01-01', source_file: 'dbf.dat', source_line: 3, value_kind: 'input' }], summary: { total_mw: 30, peak_mw: 18, block_count: 2 }, warnings: [], provenance: 'DBF demand-only fixture' } }));
  await page.goto('/');
  await page.getByLabel('FIND NODE').fill('900');
  await page.getByRole('option', { name: /BUS 900/ }).click();
  await expect(page.getByText('GENERATORS AT THIS NODE')).toBeVisible();
  await expect(page.getByText('Select a node with active generators to inspect its assets.')).toBeVisible();
  await expect(page.getByText('NODE DEMAND')).toBeVisible();
  await expect(page.locator('#demand-block')).toHaveValue('all');
});

test('active import blocks stale temporal requests while refreshing the revision', async ({ page }) => {
  await page.route(/\/api\/projects$/, async (route) => route.fulfill({ json: [{ id: 1, name: 'CRIE Gatun' }] }));
  await page.route(/\/api\/projects\/1\/revisions$/, async (route) => route.fulfill({ json: [{ id: 2, revision_number: 2, status: 'inspecting', is_active: false }] }));
  await page.route(/\/api\/projects\/1\/imports(?:\?.*)?$/, async (route) => route.fulfill({ json: [{ id: 23, project_id: 1, status: 'running', files_total: 150, files_processed: 150, files_binary: 1, errors: 0, message: JSON.stringify({ phase: 'mapping', progress: 70, logs: [] }) }] }));
  await page.route(/\/api\/projects\/1\/analytics\/status$/, async (route) => route.fulfill({ json: { status: 'not-started', progress: 0, processed_assets: 0, total_assets: 0 } }));
  await page.route(/\/api\/projects\/1\/snapshot.*/, async (route) => route.fulfill({ json: snapshot }));

  await page.goto('/');
  await expect(page.getByText('Processing source data in background')).toBeVisible();
  await expect(page.getByRole('progressbar', { name: 'Active revision update progress' })).toHaveAttribute('aria-valuenow', '70');
  await expect(page.locator('.pipeline-busy')).toHaveAttribute('aria-busy', 'true');
});
