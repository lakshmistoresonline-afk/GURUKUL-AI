import { test, expect } from '@playwright/test';

test('Chapter 102 renders correctly with canonical runtime content', async ({ page }) => {
  await page.goto('/chapter/class_5_01_english_complete_102');

  await expect(
    page.locator('body[data-gurukul-ready="true"]')
  ).toBeVisible({ timeout: 30000 });

  await expect(page.locator('header h1')).toContainText(
    'Gone with the Scooter',
    { timeout: 20000 }
  );

  // Verify canonical pillar navigation.
  await expect(page.getByText('Learn', { exact: true })).toBeVisible();
  await expect(page.getByText('Practice', { exact: true })).toBeVisible();
  await expect(page.getByText('Assess', { exact: true })).toBeVisible();
  await expect(page.getByText('Revise', { exact: true })).toBeVisible();

  // Verify actual canonical content.
  const bodyText = await page.locator('body').innerText();

  expect(bodyText).toContain('Gopi');
  expect(bodyText).toContain('hockey ball');
  expect(bodyText).toContain('Gone with the Scooter');

  console.log(
    'Smoke Test Passed: Chapter 102 canonical content is production-rendered.'
  );
});
