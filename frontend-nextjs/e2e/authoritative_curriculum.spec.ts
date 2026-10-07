import { test, expect } from '@playwright/test';

test.describe('Authoritative Curriculum E2E UAT Suite', () => {
  const testCases = [
    { grade: '5', subject: 'English', book: 'main', part: 'none', unit: 'U01', chapterId: 'G5-ENG-U01-C01' },
    { grade: '5', subject: 'Hindi', book: 'main', part: 'none', unit: 'U01', chapterId: 'G5-HIN-U01-C01' },
    { grade: '5', subject: 'Maths', book: 'main', part: 'none', unit: 'U01', chapterId: 'G5-MAT-U01-C01' },
    { grade: '5', subject: 'Science', book: 'main', part: 'none', unit: 'U01', chapterId: 'G5-SCI-U01-C01' },
    { grade: '6', subject: 'Social', book: 'main', part: 'none', unit: 'U01', chapterId: 'G6-SOC-U01-C01' },
    { grade: '7', subject: 'Mathematics', book: 'maths_i', part: 'part1', unit: 'U01', chapterId: 'G7-MAT-U01-C01' },
    { grade: '7', subject: 'Mathematics', book: 'maths_ii', part: 'part2', unit: 'U01', chapterId: 'G7-MAT-U01-C01' },
    { grade: '7', subject: 'Social Science', book: 'social_i', part: 'part1', unit: 'U01', chapterId: 'G7-SOC-U01-C01' },
  ];

  const contentTypes = ['Overview', 'Notes', 'Master', 'Foundational', 'Flashcards', 'Mindmaps', 'Quiz', 'Question Papers'];

  for (const tc of testCases) {
    test(`Test Class ${tc.grade} ${tc.subject} (${tc.book})`, async ({ page }) => {
      const consoleErrors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') consoleErrors.push(msg.text());
      });

      const failedRequests: string[] = [];
      page.on('requestfailed', req => {
        failedRequests.push(req.url());
      });

      const url = `/curriculum/${tc.grade}/${encodeURIComponent(tc.subject)}/${tc.book}/${tc.part}/${tc.unit}/${tc.chapterId}`;
      await page.goto(url);

      // Verify identity header
      await expect(page.locator(`text=Class ${tc.grade}`)).toBeVisible();

      // Test all content type tabs
      for (const ct of contentTypes) {
        const tabButton = page.locator(`button:has-text("${ct}")`).first();
        if (await tabButton.isVisible()) {
          await tabButton.click();
          await page.waitForTimeout(200);
        }
      }

      expect(consoleErrors.length).toBe(0);
      expect(failedRequests.length).toBe(0);
    });
  }

  test('Test Invalid Identity Handling', async ({ page }) => {
    await page.goto('/curriculum/99/InvalidSubject/main/none/U99/NONEXISTENT-C99');
    await expect(page.locator('text=Curriculum Identity Not Found')).toBeVisible();
  });
});
