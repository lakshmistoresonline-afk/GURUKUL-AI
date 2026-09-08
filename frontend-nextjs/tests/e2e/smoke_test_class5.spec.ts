import { test, expect } from '@playwright/test';

test('Chapter 102 renders correctly with canonical data attributes', async ({ page }) => {
  // Go to Chapter 102
  await page.goto('http://localhost:3000/chapter/class_5_01_english_102');

  // Wait for loading to finish
  await page.waitForSelector('body[data-gurukul-ready="true"]', { timeout: 30000 });

  // Verify Title
  const title = await page.textContent('h1');
  expect(title).toContain('Gone with the Scooter');

  // Verify canonical record attributes
  const firstRecord = await page.locator('[data-gurukul-record-id]').first();
  await expect(firstRecord).toBeVisible();

  const recordId = await firstRecord.getAttribute('data-gurukul-record-id');
  expect(recordId).toMatch(/^class05_01_english_102_learn_/);

  const section = await firstRecord.getAttribute('data-section');
  expect(section).toBe('learn');

  console.log('Smoke Test Passed: Chapter 102 is visible and functional.');
});
