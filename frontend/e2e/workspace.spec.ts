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
  buses: [{ source_code: '800', latitude: -32.9, longitude: -56 }],
  circuits: [],
  maintenance: [],
  provenance: 'intermediate database snapshot',
};

test('system workspace loads API data and changes stage context', async ({ page }) => {
  await page.route('http://127.0.0.1:8000/api/projects', async (route) => route.fulfill({ json: [{ id: 1, name: 'UY revision' }] }));
  await page.route('http://127.0.0.1:8000/api/projects/1/revisions', async (route) => route.fulfill({ json: [{ id: 1, revision_number: 1, status: 'parsed', is_active: true }] }));
  await page.route(/http:\/\/127\.0\.0\.1:8000\/api\/projects\/1\/snapshot.*/, async (route) => {
    const url = new URL(route.request().url());
    await route.fulfill({ json: { ...snapshot, stage: Number(url.searchParams.get('stage') ?? 1) } });
  });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /UY revision system view/i })).toBeVisible();
  await expect(page.getByLabel('Generators by shared node').getByRole('button', { name: 'Select Terra' })).toBeVisible();
  await expect(page.getByText('2 generators')).toBeVisible();
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
  await page.route('http://127.0.0.1:8000/api/projects', async (route) => route.fulfill({ json: [{ id: 1, name: 'PE_BC' }] }));
  await page.route('http://127.0.0.1:8000/api/projects/1/revisions', async (route) => route.fulfill({ json: [{ id: 1, revision_number: 1, status: 'ready', is_active: true }] }));
  await page.route(/http:\/\/127\.0\.0\.1:8000\/api\/projects\/1\/snapshot.*/, async (route) => route.fulfill({ json: peruSnapshot }));
  await page.goto('/');
  await expect(page.getByText('Topology layout')).toBeVisible();
  await expect(page.getByText('DERIVED NETWORK VIEW')).toBeVisible();
  await expect(page.getByText('DERIVED TOPOLOGY · NOT GEOGRAPHIC')).toBeVisible();
});
