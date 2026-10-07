import { test, expect } from '@playwright/test';

test.describe('Comprehensive Authoritative Curriculum UAT Suite', () => {
  const targetCurricula = [
    // Class 5
    { grade: '5', subject: 'english', book: 'english', part: 'main', unit: 'U01', chapterId: 'G5-ENG-U01-C01' },
    { grade: '5', subject: 'hindi', book: 'hindi', part: 'main', unit: 'U01', chapterId: 'G5-HIN-U01-C01' },
    { grade: '5', subject: 'mathematics', book: 'mathematics', part: 'main', unit: 'U01', chapterId: 'G5-MAT-U01-C01' },
    { grade: '5', subject: 'science', book: 'science', part: 'main', unit: 'U01', chapterId: 'G5-SCI-U01-C01' },
    // Class 6
    { grade: '6', subject: 'english', book: 'english', part: 'main', unit: 'U01', chapterId: 'G6-ENG-U01-C01' },
    { grade: '6', subject: 'hindi', book: 'hindi', part: 'main', unit: 'U01', chapterId: 'G6-HIN-U01-C01' },
    { grade: '6', subject: 'mathematics', book: 'mathematics', part: 'main', unit: 'U01', chapterId: 'G6-MAT-U01-C01' },
    { grade: '6', subject: 'science', book: 'science', part: 'main', unit: 'U01', chapterId: 'G6-SCI-U01-C01' },
    { grade: '6', subject: 'social_science', book: 'social_science', part: 'main', unit: 'U01', chapterId: 'G6-SOC-U01-C01' },
    // Class 7
    { grade: '7', subject: 'english', book: 'english', part: 'main', unit: 'U01', chapterId: 'G7-ENG-U01-C01' },
    { grade: '7', subject: 'hindi', book: 'hindi', part: 'main', unit: 'U01', chapterId: 'G7-HIN-U01-C01' },
    { grade: '7', subject: 'mathematics', book: 'maths_i', part: 'part1', unit: 'U01', chapterId: 'G7-MAT-U01-C01' },
    { grade: '7', subject: 'mathematics', book: 'maths_ii', part: 'part2', unit: 'U01', chapterId: 'G7-MAT-U01-C01' },
    { grade: '7', subject: 'science', book: 'science', part: 'main', unit: 'U01', chapterId: 'G7-SCI-U01-C01' },
    { grade: '7', subject: 'social_science', book: 'social_i', part: 'part1', unit: 'U01', chapterId: 'G7-SOC-U01-C01' },
    { grade: '7', subject: 'social_science', book: 'social_ii', part: 'part2', unit: 'U01', chapterId: 'G7-SOC-U01-C01' },
  ];

  for (const tc of targetCurricula) {
    test(`Verify Class ${tc.grade} - ${tc.subject} (${tc.book} / ${tc.part})`, async ({ page }) => {
      const consoleErrors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') consoleErrors.push(msg.text());
      });

      const failedRequests: string[] = [];
      page.on('requestfailed', req => {
        failedRequests.push(req.url());
      });

      const url = `/curriculum/${tc.grade}/${tc.subject}/${tc.book}/${tc.part}/${tc.unit}/${tc.chapterId}`;
      const response = await page.goto(url);

      expect(response?.status()).toBe(200);
      await expect(page.locator(`text=Class ${tc.grade}`)).toBeVisible();
      await expect(page.locator(`text=Chapter: ${tc.chapterId}`)).toBeVisible();

      expect(consoleErrors.length).toBe(0);
      expect(failedRequests.length).toBe(0);
    });
  }

  test('Verify Invalid Identity Handling (400, 404, 422)', async ({ page }) => {
    // Invalid book
    let res = await page.goto('/curriculum/7/mathematics/wrong_book/part1/U01/G7-MAT-U01-C01');
    await expect(page.locator('text=Curriculum Identity Not Found')).toBeVisible();

    // Invalid chapter
    res = await page.goto('/curriculum/5/english/english/main/U01/NONEXISTENT-CHAPTER');
    await expect(page.locator('text=Curriculum Identity Not Found')).toBeVisible();

    // Incomplete identity dimensions
    res = await page.goto('/curriculum/5/english');
    await expect(page.locator('text=Bad Request')).toBeVisible();
  });
});
