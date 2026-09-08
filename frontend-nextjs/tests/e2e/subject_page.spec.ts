import { test, expect } from '@playwright/test';

test('Subject page renders curriculum for Class 5 English', async ({ page }) => {
  await page.goto('http://localhost:3000/subject/class_5_01_english');

  // Verify Title
  const title = page.locator('h1');
  await expect(title).toContainText('ENGLISH Curriculum');

  // Verify Chapters are listed
  const chapterCards = page.locator('a[href^="/chapter/"]');
  const count = await chapterCards.count();
  expect(count).toBeGreaterThan(0);

  // Verify Chapter 102 specifically
  const ch102 = page.locator('h3:has-text("Gone with the Scooter")');
  await expect(ch102).toBeVisible();
});
