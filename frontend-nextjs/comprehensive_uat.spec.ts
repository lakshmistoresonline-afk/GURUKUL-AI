import { test, expect } from '@playwright/test';

test.describe('Gurukul AI Comprehensive UAT & Visual Regression Suite', () => {
  test('Class 5 English Chapter 1 renders all 8 tabs correctly', async ({ page }) => {
    await page.goto('http://localhost:3000/5/English/G5-ENG-U01-C01');
    await expect(page.locator('text=Papa\'s Spectacles')).toBeVisible();
    await expect(page.locator('text=Overview')).toBeVisible();
    await expect(page.locator('text=Notes')).toBeVisible();
    await expect(page.locator('text=Master Practice')).toBeVisible();
    await expect(page.locator('text=Flashcards')).toBeVisible();
    await expect(page.locator('text=Mindmaps')).toBeVisible();
    await expect(page.locator('text=Quiz')).toBeVisible();
    await expect(page.locator('text=Question Papers')).toBeVisible();
    await expect(page.locator('text=Foundational Core')).toBeVisible();
  });

  test('Class 6 Social Chapter 1 renders without errors', async ({ page }) => {
    await page.goto('http://localhost:3000/6/Social/G6-SOC-U01-C01');
    await expect(page.locator('text=Locating Places on the Earth')).toBeVisible();
  });
});
