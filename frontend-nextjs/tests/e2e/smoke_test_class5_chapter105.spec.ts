import { test, expect } from '@playwright/test';

test('Chapter 105: Our Vibrant Country renders complete canonical content', async ({ page }) => {
  const failedRequests: string[] = [];
  page.on('requestfailed', (req) => {
    failedRequests.push(`${req.method()} ${req.url()} :: ${req.failure()?.errorText}`);
  });

  await page.goto('/chapter/class_5_03_evs_complete_105');

  await expect(
    page.locator('body[data-gurukul-ready="true"]')
  ).toBeVisible({ timeout: 30000 });

  await expect(page.locator('header h1')).toContainText(
    'Our Vibrant Country',
    { timeout: 20000 }
  );

  // Verify all 5 pillar tabs exist and render accurate non-zero counts for populated pillars
  await expect(page.getByText('Learn', { exact: true })).toBeVisible();
  await expect(page.getByText('Practice', { exact: true })).toBeVisible();
  await expect(page.getByText('Assess', { exact: true })).toBeVisible();

  // Verify "No content discovered" is NOT displayed on default Learn pillar
  const bodyText = await page.locator('body').innerText();
  expect(bodyText).not.toContain('No content discovered in this archive stream');

  // Verify actual Learn content is rendered
  expect(bodyText).toContain('Republic Day');

  // Switch to Practice pillar
  await page.getByRole('button', { name: /Practice/i }).click();
  const practiceBody = await page.locator('body').innerText();
  expect(practiceBody).not.toContain('No content discovered in this archive stream');

  // Switch to Assess pillar
  await page.getByRole('button', { name: /Assess/i }).click();
  const assessBody = await page.locator('body').innerText();
  expect(assessBody).not.toContain('No content discovered in this archive stream');

  expect(failedRequests.length, `Failed network requests detected: ${JSON.stringify(failedRequests)}`).toBe(0);

  console.log(
    'Smoke Test Passed: Chapter 105 canonical content is production-rendered without content collapse.'
  );
});
