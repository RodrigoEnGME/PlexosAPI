import { expect, test, type Page } from '@playwright/test';

const topologySnapshot = {
  stage: 1,
  block: 1,
  as_of: '2023-01-01',
  study: {
    initial_year: 2023,
    stages: 24,
    blocks: 3,
    frequency: 'monthly',
    warnings: ['Fixture warning with source context.'],
    systems: [{ code: 'pe', name: 'Peru', country_code: 'pe' }],
    layout: 'topology layout',
  },
  entities: [{
    id: '1', source_code: '800', name: 'Central Lima', technology: 'hydro', asset_type: 'hydro',
    system_code: 'pe', bus: 800, capacity_mw: 100, source_file: 'chidrope.dat', source_line: 3,
    latitude: null, longitude: null, coordinate_status: 'missing', lifecycle_status: 'existing',
    is_active: true, modifications: [],
  }],
  buses: [
    { source_code: '800', name: 'Lima', system_code: 'pe', latitude: null, longitude: null },
    { source_code: '900', name: 'Load-only node', system_code: 'pe', demand_mw: 18, latitude: null, longitude: null },
  ],
  circuits: [{ source_code: 'c1', from_bus: '800', to_bus: '900', name: 'Lima load link', system_code: 'pe' }],
  demands: [],
  maintenance: [],
  provenance: 'intermediate database snapshot',
};

async function mockWorkspace(page: Page) {
  await page.route(/\/api\/projects$/, (route) => route.fulfill({ json: [{ id: 1, name: 'PE responsive' }] }));
  await page.route(/\/api\/projects\/1\/revisions$/, (route) => route.fulfill({ json: [{ id: 1, revision_number: 1, status: 'ready', is_active: true }] }));
  await page.route(/\/api\/projects\/1\/imports(?:\?.*)?$/, (route) => route.fulfill({ json: [] }));
  await page.route(/\/api\/projects\/1\/maintenance-settings$/, (route) => route.fulfill({ json: { project_id: 1, revision_id: 1, availability_basis: 'short_term', review_status: 'confirmed', override: {} } }));
  await page.route(/\/api\/projects\/1\/maintenance-review$/, (route) => route.fulfill({ json: { project_id: 1, revision_id: 1, review_status: 'confirmed', availability_basis: 'short_term', tables: [] } }));
  await page.route(/\/api\/projects\/1\/analytics\/status$/, (route) => route.fulfill({ json: { status: 'ready', progress: 100, processed_assets: 1, total_assets: 1 } }));
  await page.route(/\/api\/projects\/1\/snapshot.*/, (route) => route.fulfill({ json: topologySnapshot }));
  await page.route(/\/api\/projects\/1\/buses\/900\/demand.*/, (route) => route.fulfill({ json: {
    bus_code: '900', bus_name: 'Load-only node', authority: 'DBF', selected_date: '2023-01-01',
    available_dates: ['2023-01-01'], available_blocks: [1], demand_codes: ['1'],
    records: [{ block: 1, demand_mw: 18, demand_code: '1', effective_date: '2023-01-01', source_file: 'dbf.dat', source_line: 2, value_kind: 'input' }],
    summary: { total_mw: 18, peak_mw: 18, block_count: 1 }, warnings: [], provenance: 'DBF responsive fixture',
  } }));
  await page.route(/\/api\/projects\/1\/buses\/800\/demand.*/, (route) => route.fulfill({ status: 404, json: { detail: 'No demand input for bus 800' } }));
  await page.route(/\/api\/projects\/1\/assets\/1\/history.*/, (route) => route.fulfill({ json: { frequency: 'monthly', series: [] } }));
  await page.route(/\/api\/projects\/1\/assets\/1\/profile-statistics$/, (route) => route.fulfill({ json: { status: 'not-applicable', grouping: 'monthly', unit: 'MW', statistics: null, series: [] } }));
}

test.beforeEach(async ({ page }) => {
  await mockWorkspace(page);
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /PE responsive system view/i })).toBeVisible();
});

test('workspace has no document overflow and retains non-geographic semantics', async ({ page }) => {
  await expect(page.getByText('01 / NETWORK TOPOLOGY')).toBeVisible();
  await expect(page.getByText('DERIVED TOPOLOGY · NOT GEOGRAPHIC')).toBeVisible();
  await expect(page.getByRole('region', { name: /Derived electrical topology layout/i })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});

test('mobile workspace uses bottom navigation and map timeline inspector order', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name === 'chromium', 'Mobile-only acceptance');

  expect(await page.evaluate(() => window.innerWidth)).toBe(testInfo.project.name === 'mobile-390' ? 390 : 412);
  const rail = await page.locator('.rail').boundingBox();
  const map = await page.locator('.map-panel').boundingBox();
  const timeline = await page.locator('.timeline-panel').boundingBox();
  const inspector = await page.locator('.inspector').boundingBox();
  expect(rail).not.toBeNull();
  expect(map).not.toBeNull();
  expect(timeline).not.toBeNull();
  expect(inspector).not.toBeNull();
  expect(rail!.y).toBeGreaterThan(760);
  expect(map!.y).toBeLessThan(timeline!.y);
  expect(timeline!.y).toBeLessThan(inspector!.y);
  const activeNavigation = page.getByRole('button', { name: '01 Map workspace' });
  await activeNavigation.focus();
  expect(await activeNavigation.evaluate((element) => Number.parseFloat(getComputedStyle(element).outlineWidth))).toBeGreaterThanOrEqual(2);

  const targetSelectors = [
    '.rail nav button',
    '.topology-toolbar button',
    '#node-search-input',
    '.timeline-meta select',
  ];
  for (const selector of targetSelectors) {
    const sizes = await page.locator(selector).evaluateAll((elements) => elements.map((element) => {
      const box = element.getBoundingClientRect();
      return { width: box.width, height: box.height };
    }));
    expect(sizes.length).toBeGreaterThan(0);
    for (const size of sizes) {
      expect(size.width).toBeGreaterThanOrEqual(44);
      expect(size.height).toBeGreaterThanOrEqual(44);
    }
  }

  const search = page.getByLabel('FIND NODE');
  await search.fill('900');
  await search.press('ArrowDown');
  await search.press('Enter');
  await expect(page.getByRole('heading', { name: 'BUS 900' })).toBeVisible();
  await expect(page.getByText('NODE DEMAND')).toBeVisible();

  await page.getByRole('button', { name: /Select bus 800/i }).click();
  await expect(page.getByRole('heading', { name: 'BUS 800' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);

  await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  const navigationTop = (await page.locator('.rail').boundingBox())!.y;
  const finalPanel = page.locator('.generator-details-panel');
  const finalBox = await finalPanel.boundingBox();
  const contentBottom = finalBox!.y + finalBox!.height;
  expect(contentBottom).toBeLessThanOrEqual(navigationTop + 1);
});

test('geographic map remains selectable and touch-scroll safe', async ({ page }, testInfo) => {
  await page.unroute(/\/api\/projects\/1\/snapshot.*/);
  const geographicSnapshot = {
    ...topologySnapshot,
    study: { ...topologySnapshot.study, layout: 'geographic map' },
    entities: topologySnapshot.entities.map((entity) => ({ ...entity, latitude: -12.05, longitude: -77.04, coordinate_status: 'bus-reference' })),
    buses: topologySnapshot.buses.map((bus, index) => ({ ...bus, latitude: -12.05 - index * 0.01, longitude: -77.04 - index * 0.01 })),
  };
  await page.route(/\/api\/projects\/1\/snapshot.*/, (route) => route.fulfill({ json: geographicSnapshot }));
  await page.reload();

  const map = page.getByLabel('Geographic map of input assets');
  await expect(map).toBeVisible();
  await page.locator('.generator-marker-wrapper').click();
  await expect(page.getByRole('heading', { name: 'BUS 800' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  if (testInfo.project.name !== 'chromium') {
    expect(await map.evaluate((element) => getComputedStyle(element.closest('.map-canvas')!).touchAction)).toContain('pan-y');
    const zoomControls = await page.locator('.leaflet-control-zoom a').evaluateAll((elements) => elements.map((element) => element.getBoundingClientRect().height));
    expect(zoomControls.length).toBeGreaterThan(0);
    zoomControls.forEach((height) => expect(height).toBeGreaterThanOrEqual(44));
  }
});

test('desktop retains left rail and side inspector', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium', 'Desktop-only acceptance');
  await page.setViewportSize({ width: 1280, height: 900 });
  const rail = await page.locator('.rail').boundingBox();
  const map = await page.locator('.map-panel').boundingBox();
  const inspector = await page.locator('.inspector').boundingBox();
  expect(rail?.x).toBe(0);
  expect(rail?.width).toBe(84);
  expect(inspector!.x).toBeGreaterThan(map!.x + map!.width - 1);
  await expect(page.getByRole('button', { name: '01 Map workspace' })).toHaveAttribute('aria-current', 'page');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});
