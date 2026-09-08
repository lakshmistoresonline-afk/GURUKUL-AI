import { test, expect } from '@playwright/test';

test('Chapter 101: Papa Spectacles renders correctly', async ({ page }) => {
  // Go to Chapter 101
  await page.goto('http://localhost:3000/chapter/class_5_01_english_101');

  // Wait for loading to finish
  await page.waitForSelector('body[data-gurukul-ready="true"]', { timeout: 30000 });

  // Verify Title
  const title = await page.textContent('h1');
  expect(title).toContain('Papas Spectacles');

  // Verify Navigation
  await expect(page.getByText('1 / 10')).toBeVisible();

  // Verify First Stanza (Poem)
  const firstRecord = await page.locator('[data-gurukul-record-id]').first();
  await expect(firstRecord).toBeVisible();

  // Verify data attributes
  const recordId = await firstRecord.getAttribute('data-gurukul-record-id');
  expect(recordId).toMatch(/^class05_01_english_101_learn_/);

  // Verify no obvious duplications like "water water water"
  const bodyText = await page.innerText('body');
  expect(bodyText).not.toContain('water water water');
  expect(bodyText).not.toContain('elephant elephant elephant');

  // Verify no standalone OCR junk like isolated "1." or "2." in cards
  const cards = await page.locator('[data-gurukul-record-id]').all();
  for (const card of cards) {
    const text = await card.innerText();
    if (text.length < 5 && text.trim().match(/^\d+\.$/)) {
        throw new Error(`Orphan fragment detected: "${text}"`);
    }
  }

  console.log('Smoke Test Passed: Chapter 101 is Production Ready.');
});
