# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend-nextjs\tests\e2e\smoke_test_class5.spec.ts >> Chapter 102 renders correctly with canonical runtime content
- Location: frontend-nextjs\tests\e2e\smoke_test_class5.spec.ts:3:5

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/chapter/class_5_01_english_complete_102", waiting until "load"

```

# Test source

```ts
  1  | ﻿import { test, expect } from '@playwright/test';
  2  | 
  3  | test('Chapter 102 renders correctly with canonical runtime content', async ({ page }) => {
> 4  |   await page.goto('/chapter/class_5_01_english_complete_102');
     |              ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  5  | 
  6  |   await expect(
  7  |     page.locator('body[data-gurukul-ready="true"]')
  8  |   ).toBeVisible({ timeout: 30000 });
  9  | 
  10 |   await expect(page.locator('header h1')).toContainText(
  11 |     'Gone with the Scooter',
  12 |     { timeout: 20000 }
  13 |   );
  14 | 
  15 |   // Verify canonical pillar navigation.
  16 |   await expect(page.getByText('Learn', { exact: true })).toBeVisible();
  17 |   await expect(page.getByText('Practice', { exact: true })).toBeVisible();
  18 |   await expect(page.getByText('Assess', { exact: true })).toBeVisible();
  19 |   await expect(page.getByText('Revise', { exact: true })).toBeVisible();
  20 | 
  21 |   // Verify actual canonical content.
  22 |   const bodyText = await page.locator('body').innerText();
  23 | 
  24 |   expect(bodyText).toContain('Gopi');
  25 |   expect(bodyText).toContain('hockey ball');
  26 |   expect(bodyText).toContain('Gone with the Scooter');
  27 | 
  28 |   console.log(
  29 |     'Smoke Test Passed: Chapter 102 canonical content is production-rendered.'
  30 |   );
  31 | });
  32 | 
```