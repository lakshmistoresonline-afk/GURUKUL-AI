import { test, expect } from '@playwright/test';

test.describe('Gurukul AI Dashboard Visual UAT & Regression', () => {
  test('Dashboard loads successfully and displays classes', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page).toHaveTitle(/Gurukul/i);
    const heading = page.locator('text=Class 5');
    await expect(heading.first()).toBeVisible();
  });

  test('Chapter client view renders all navigation tabs', async ({ page }) => {
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
});
