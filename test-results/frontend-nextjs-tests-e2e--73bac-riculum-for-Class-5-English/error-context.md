# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend-nextjs\tests\e2e\subject_page.spec.ts >> Subject page renders curriculum for Class 5 English
- Location: frontend-nextjs\tests\e2e\subject_page.spec.ts:3:5

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/subject/01_english_complete", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('Subject page renders curriculum for Class 5 English', async ({ page }) => {
> 4  |   await page.goto('/subject/01_english_complete');
     |              ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  5  | 
  6  |   await expect(
  7  |     page.locator('body[data-gurukul-ready="true"]')
  8  |   ).toBeVisible({ timeout: 30000 });
  9  | 
  10 |   // The current canonical UI uses the stream name.
  11 |   await expect(
  12 |     page.locator('header h1')
  13 |   ).toContainText('ENGLISH COMPLETE', { timeout: 30000 });
  14 | 
  15 |   // Canonical Class 5 English contains 10 chapters.
  16 |   const chapterCards = page.locator('a[href^="/chapter/"]');
  17 | 
  18 |   await expect(chapterCards.first()).toBeVisible({
  19 |     timeout: 30000
  20 |   });
  21 | 
  22 |   const count = await chapterCards.count();
  23 |   expect(count).toBe(10);
  24 | 
  25 |   // Verify known canonical chapters.
  26 |   await expect(
  27 |     page.getByText('Papas Spectacles', { exact: true })
  28 |   ).toBeVisible({ timeout: 20000 });
  29 | 
  30 |   await expect(
  31 |     page.getByText('Gone with the Scooter', { exact: true })
  32 |   ).toBeVisible({ timeout: 20000 });
  33 | 
  34 |   console.log(
  35 |     'Smoke Test Passed: Class 5 English subject page is canonical and complete.'
  36 |   );
  37 | });
  38 | 
```