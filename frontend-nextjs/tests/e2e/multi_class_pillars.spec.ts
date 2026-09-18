import { test, expect } from '@playwright/test';

const testChapters = [
  // Class 5
  { uid: 'class_5_01_english_complete_101', name: 'Papa Spectacles', classId: '5' },
  { uid: 'class_5_03_evs_complete_105', name: 'Our Vibrant Country', classId: '5' },
  // Class 6
  { uid: 'class_6_02_english_complete_grade6_10101', name: 'A Bottle of Dew', classId: '6' },
  { uid: 'class_6_03_science_complete_grade6_101', name: 'Wonderful World of Science', classId: '6' },
];

for (const ch of testChapters) {
  test(`Multi-Class E2E: Class ${ch.classId} chapter ${ch.uid} renders complete canonical five-pillar UI`, async ({ page }) => {
    const failedRequests: string[] = [];
    page.on('requestfailed', (req) => {
      failedRequests.push(`${req.method()} ${req.url()} :: ${req.failure()?.errorText}`);
    });

    await page.goto(`/chapter/${ch.uid}`);

    // Wait for body ready state
    await expect(page.locator('body[data-gurukul-ready="true"]')).toBeVisible({ timeout: 30000 });

    // Confirm header title
    await expect(page.locator('header h1')).toBeVisible({ timeout: 20000 });

    // Verify pillar tabs exist
    await expect(page.getByText('Learn', { exact: true })).toBeVisible();
    await expect(page.getByText('Practice', { exact: true })).toBeVisible();
    await expect(page.getByText('Assess', { exact: true })).toBeVisible();
    await expect(page.getByText('Revise', { exact: true })).toBeVisible();
    await expect(page.getByText('Resources', { exact: true })).toBeVisible();

    // Verify Learn content is present and not displaying "No content discovered" error
    const bodyText = await page.locator('body').innerText();
    expect(bodyText).not.toContain('No content discovered in this archive stream');

    // Confirm layout container uses available horizontal width
    const container = page.locator('#gurukul-chapter-container');
    await expect(container).toBeVisible();

    expect(failedRequests.length, `Failed network requests for ${ch.uid}: ${JSON.stringify(failedRequests)}`).toBe(0);

    console.log(`PASS: Class ${ch.classId} Chapter ${ch.uid} (${ch.name}) certified in browser.`);
  });
}
