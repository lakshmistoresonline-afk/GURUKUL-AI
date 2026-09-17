# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend-nextjs\tests\e2e\smoke_test_class5_chapter101.spec.ts >> Chapter 101: Papa Spectacles renders correctly
- Location: frontend-nextjs\tests\e2e\smoke_test_class5_chapter101.spec.ts:3:5

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/chapter/class_5_01_english_complete_101", waiting until "load"

```

# Test source

```ts
  1  | ﻿import { test, expect } from '@playwright/test';
  2  | 
  3  | test('Chapter 101: Papa Spectacles renders correctly', async ({ page }) => {
> 4  |   await page.goto('/chapter/class_5_01_english_complete_101');
     |              ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  5  | 
  6  |   await expect(
  7  |     page.locator('body[data-gurukul-ready="true"]')
  8  |   ).toBeVisible({ timeout: 30000 });
  9  | 
  10 |   await expect(page.locator('header h1')).toContainText(
  11 |     'Papas Spectacles',
  12 |     { timeout: 20000 }
  13 |   );
  14 | 
  15 |   // Canonical pillar navigation/counts.
  16 |   await expect(page.getByText('Learn', { exact: true })).toBeVisible();
  17 |   await expect(page.getByText('Practice', { exact: true })).toBeVisible();
  18 |   await expect(page.getByText('Assess', { exact: true })).toBeVisible();
  19 |   await expect(page.getByText('Revise', { exact: true })).toBeVisible();
  20 |   await expect(page.getByText('Resources', { exact: true })).toBeVisible();
  21 | 
  22 |   // Canonical chapter content must be rendered.
  23 |   const bodyText = await page.locator('body').innerText();
  24 | 
  25 |   expect(bodyText).toContain('Today our papa');
  26 |   expect(bodyText).toContain('spectacles');
  27 |   expect(bodyText).not.toContain('water water water');
  28 |   expect(bodyText).not.toContain('elephant elephant elephant');
  29 | 
  30 |   // Production baseline marker.
  31 |   await expect(
  32 |     page.getByText('VERIFIED NCERT CURRICULUM')
  33 |   ).toBeVisible();
  34 | 
  35 |   console.log(
  36 |     'Smoke Test Passed: Chapter 101 canonical content is production-rendered.'
  37 |   );
  38 | });
  39 | 
```