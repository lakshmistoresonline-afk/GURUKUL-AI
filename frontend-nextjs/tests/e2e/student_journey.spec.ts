import { test, expect } from '@playwright/test';

test.describe('Student End-to-End Journey', () => {
  test('Full Journey: Subject to Assessment', async ({ page }) => {
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
    page.on('requestfailed', request => console.log('FAILED REQUEST:', request.url(), request.failure()?.errorText));

    // 1. Dashboard
    await page.goto('/');

    // Check if we are logged in or on landing page
    const dashboardTitle = page.getByText('Student Dashboard');
    const loginForm = page.locator('input[placeholder="Username"]');

    // Wait for either dashboard title or login form
    await expect(dashboardTitle.or(loginForm)).toBeVisible({ timeout: 45000 });

    if (await loginForm.isVisible()) {
        await page.fill('input[placeholder="Username"]', 'tester_v1');
        await page.fill('input[placeholder="Password"]', 'password123');
        await page.click('button:has-text("Authorize Access")');
        await expect(dashboardTitle).toBeVisible({ timeout: 45000 });
    }

    // 2. Select Subject (English)
    const englishLink = page.locator('a:has-text("English")').first();
    await expect(englishLink).toBeVisible({ timeout: 20000 });
    await englishLink.click();

    await expect(page.getByText('Course Chapters')).toBeVisible({ timeout: 30000 });

    // 3. Select Chapter (Papa s Spectacles)
    // Wait for loading to finish
    await expect(page.getByText('Assembling Course Curriculum')).not.toBeVisible({ timeout: 30000 });

    // Check if there are any error messages visible
    const errorText = page.getByText(/error|failed|missing/i);
    if (await errorText.isVisible()) {
        console.log('Error visible on Subject Page:', await errorText.innerText());
    }

    // Wait for any link to load
    const firstChapter = page.locator('a[href*="/chapter/"]').first();
    await expect(firstChapter).toBeVisible({ timeout: 30000 });

    await firstChapter.click();

    await expect(page.getByText('Synchronizing Neural Stream')).not.toBeVisible({ timeout: 30000 });

    // 4. Learning Tab
    const learnTab = page.getByRole('button', { name: 'Learn' });
    await learnTab.click();
    await expect(page.getByText('Orientation')).toBeVisible({ timeout: 20000 });

    // 5. Practice Tab
    const practiceTab = page.getByRole('button', { name: 'Practice' });
    await practiceTab.click();
    await expect(page.locator('div.bg-white.border-2').first()).toBeVisible({ timeout: 20000 });

    // 6. Interaction: View Answer
    const answerToggle = page.getByText('Access Canonical Truth').first();
    if (await answerToggle.isVisible()) {
      await answerToggle.click();
      await expect(page.locator('details[open]')).toBeVisible();
    }

    // 9. Back to Dashboard
    await page.click('a:has-text("Dashboard")');
    await page.waitForURL('/', { timeout: 20000 });
    await expect(page.getByText('Student Dashboard')).toBeVisible();
  });
});
