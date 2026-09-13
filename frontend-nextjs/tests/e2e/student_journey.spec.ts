import { test, expect } from '@playwright/test';

test.describe('Student End-to-End Journey', () => {

  test('Full canonical Journey: Home → Subject → Chapter → Pillars', async ({ page }) => {

    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('BROWSER ERROR:', msg.text());
      }
    });

    page.on('requestfailed', request => {
      console.log(
        'FAILED REQUEST:',
        request.url(),
        request.failure()?.errorText
      );
    });

    // 1. Home / Unified Dashboard
    await page.goto('/');

    await expect(
      page.getByText('Gurukul Unified Dashboard', { exact: true })
    ).toBeVisible({ timeout: 30000 });

    // 2. Canonical Class 5 English stream.
    const englishLink = page.locator(
      'a[href="/subject/01_english_complete"]'
    );

    await expect(englishLink).toBeVisible({
      timeout: 20000
    });

    await englishLink.click();

    // 3. Subject page.
    await expect(page).toHaveURL(
      /\/subject\/01_english_complete$/,
      { timeout: 20000 }
    );

    await expect(
      page.locator('body[data-gurukul-ready="true"]')
    ).toBeVisible({ timeout: 30000 });

    await expect(
      page.locator('header h1')
    ).toContainText('ENGLISH COMPLETE', {
      timeout: 30000
    });

    const chapterLinks = page.locator(
      'a[href^="/chapter/"]'
    );

    await expect(chapterLinks.first()).toBeVisible({
      timeout: 30000
    });

    expect(await chapterLinks.count()).toBe(10);

    // 4. Open canonical Chapter 101.
    const papaChapter = page.locator(
      'a[href="/chapter/class_5_01_english_complete_101"]'
    );

    await expect(papaChapter).toBeVisible({
      timeout: 20000
    });

    await papaChapter.click();

    // 5. Chapter page.
    await expect(page).toHaveURL(
      /\/chapter\/class_5_01_english_complete_101$/,
      { timeout: 20000 }
    );

    await expect(
      page.locator('body[data-gurukul-ready="true"]')
    ).toBeVisible({ timeout: 30000 });

    await expect(
      page.locator('header h1')
    ).toContainText('Papas Spectacles', {
      timeout: 20000
    });

    // 6. Verify all canonical pillars exist.
    await expect(
      page.getByText('Learn', { exact: true })
    ).toBeVisible();

    await expect(
      page.getByText('Practice', { exact: true })
    ).toBeVisible();

    await expect(
      page.getByText('Assess', { exact: true })
    ).toBeVisible();

    await expect(
      page.getByText('Revise', { exact: true })
    ).toBeVisible();

    await expect(
      page.getByText('Resources', { exact: true })
    ).toBeVisible();

    // 7. Verify actual educational content.
    const bodyText = await page.locator('body').innerText();

    expect(bodyText).toContain('Today our papa');
    expect(bodyText).toContain('spectacles');

    // 8. No obvious generated/duplicate junk.
    expect(bodyText).not.toContain('water water water');
    expect(bodyText).not.toContain('elephant elephant elephant');

    // 9. Return through canonical Back link.
    const backLink = page.locator(
      'a[href="/subject/01_english_complete"]'
    ).first();

    await expect(backLink).toBeVisible({
      timeout: 20000
    });

    await backLink.click();

    await expect(page).toHaveURL(
      /\/subject\/01_english_complete$/,
      { timeout: 20000 }
    );

    console.log(
      'E2E Passed: canonical Home → Subject → Chapter → Pillars → Back journey.'
    );
  });

});
