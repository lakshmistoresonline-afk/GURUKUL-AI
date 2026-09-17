# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend-nextjs\tests\e2e\student_journey.spec.ts >> Student End-to-End Journey >> Full canonical Journey: Home → Subject → Chapter → Pillars
- Location: frontend-nextjs\tests\e2e\student_journey.spec.ts:5:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | test.describe('Student End-to-End Journey', () => {
  4   | 
  5   |   test('Full canonical Journey: Home → Subject → Chapter → Pillars', async ({ page }) => {
  6   | 
  7   |     page.on('console', msg => {
  8   |       if (msg.type() === 'error') {
  9   |         console.log('BROWSER ERROR:', msg.text());
  10  |       }
  11  |     });
  12  | 
  13  |     page.on('requestfailed', request => {
  14  |       console.log(
  15  |         'FAILED REQUEST:',
  16  |         request.url(),
  17  |         request.failure()?.errorText
  18  |       );
  19  |     });
  20  | 
  21  |     // 1. Home / Unified Dashboard
> 22  |     await page.goto('/');
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  23  | 
  24  |     await expect(
  25  |       page.getByText('Gurukul Unified Dashboard', { exact: true })
  26  |     ).toBeVisible({ timeout: 30000 });
  27  | 
  28  |     // 2. Canonical Class 5 English stream.
  29  |     const englishLink = page.locator(
  30  |       'a[href="/subject/01_english_complete"]'
  31  |     );
  32  | 
  33  |     await expect(englishLink).toBeVisible({
  34  |       timeout: 20000
  35  |     });
  36  | 
  37  |     await englishLink.click();
  38  | 
  39  |     // 3. Subject page.
  40  |     await expect(page).toHaveURL(
  41  |       /\/subject\/01_english_complete$/,
  42  |       { timeout: 20000 }
  43  |     );
  44  | 
  45  |     await expect(
  46  |       page.locator('body[data-gurukul-ready="true"]')
  47  |     ).toBeVisible({ timeout: 30000 });
  48  | 
  49  |     await expect(
  50  |       page.locator('header h1')
  51  |     ).toContainText('ENGLISH COMPLETE', {
  52  |       timeout: 30000
  53  |     });
  54  | 
  55  |     const chapterLinks = page.locator(
  56  |       'a[href^="/chapter/"]'
  57  |     );
  58  | 
  59  |     await expect(chapterLinks.first()).toBeVisible({
  60  |       timeout: 30000
  61  |     });
  62  | 
  63  |     expect(await chapterLinks.count()).toBe(10);
  64  | 
  65  |     // 4. Open canonical Chapter 101.
  66  |     const papaChapter = page.locator(
  67  |       'a[href="/chapter/class_5_01_english_complete_101"]'
  68  |     );
  69  | 
  70  |     await expect(papaChapter).toBeVisible({
  71  |       timeout: 20000
  72  |     });
  73  | 
  74  |     await papaChapter.click();
  75  | 
  76  |     // 5. Chapter page.
  77  |     await expect(page).toHaveURL(
  78  |       /\/chapter\/class_5_01_english_complete_101$/,
  79  |       { timeout: 20000 }
  80  |     );
  81  | 
  82  |     await expect(
  83  |       page.locator('body[data-gurukul-ready="true"]')
  84  |     ).toBeVisible({ timeout: 30000 });
  85  | 
  86  |     await expect(
  87  |       page.locator('header h1')
  88  |     ).toContainText('Papas Spectacles', {
  89  |       timeout: 20000
  90  |     });
  91  | 
  92  |     // 6. Verify all canonical pillars exist.
  93  |     await expect(
  94  |       page.getByText('Learn', { exact: true })
  95  |     ).toBeVisible();
  96  | 
  97  |     await expect(
  98  |       page.getByText('Practice', { exact: true })
  99  |     ).toBeVisible();
  100 | 
  101 |     await expect(
  102 |       page.getByText('Assess', { exact: true })
  103 |     ).toBeVisible();
  104 | 
  105 |     await expect(
  106 |       page.getByText('Revise', { exact: true })
  107 |     ).toBeVisible();
  108 | 
  109 |     await expect(
  110 |       page.getByText('Resources', { exact: true })
  111 |     ).toBeVisible();
  112 | 
  113 |     // 7. Verify actual educational content.
  114 |     const bodyText = await page.locator('body').innerText();
  115 | 
  116 |     expect(bodyText).toContain('Today our papa');
  117 |     expect(bodyText).toContain('spectacles');
  118 | 
  119 |     // 8. No obvious generated/duplicate junk.
  120 |     expect(bodyText).not.toContain('water water water');
  121 |     expect(bodyText).not.toContain('elephant elephant elephant');
  122 | 
```