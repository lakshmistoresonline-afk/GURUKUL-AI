import { test, expect } from '@playwright/test';

test('Chapter 101: Papa Spectacles renders correctly', async ({ page }) => {
  await page.goto('/chapter/class_5_01_english_complete_101');

  await expect(
    page.locator('body[data-gurukul-ready="true"]')
  ).toBeVisible({ timeout: 30000 });

  await expect(page.locator('header h1')).toContainText(
    'Papas Spectacles',
    { timeout: 20000 }
  );

  // Canonical pillar navigation/counts.
  await expect(page.getByText('Learn', { exact: true })).toBeVisible();
  await expect(page.getByText('Practice', { exact: true })).toBeVisible();
  await expect(page.getByText('Assess', { exact: true })).toBeVisible();
  await expect(page.getByText('Revise', { exact: true })).toBeVisible();
  await expect(page.getByText('Resources', { exact: true })).toBeVisible();

  // Canonical chapter content must be rendered.
  const bodyText = await page.locator('body').innerText();

  expect(bodyText).toContain('Today our papa');
  expect(bodyText).toContain('spectacles');
  expect(bodyText).not.toContain('water water water');
  expect(bodyText).not.toContain('elephant elephant elephant');

  // Production baseline marker.
  await expect(
    page.getByText('VERIFIED NCERT CURRICULUM')
  ).toBeVisible();

  console.log(
    'Smoke Test Passed: Chapter 101 canonical content is production-rendered.'
  );
});
