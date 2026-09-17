# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend-nextjs\tests\e2e\phase10_dom_inspection.spec.ts >> PHASE 10 - inspect actual canonical frontend DOM
- Location: frontend-nextjs\tests\e2e\phase10_dom_inspection.spec.ts:3:5

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/chapter/class_5_01_english_complete_101", waiting until "networkidle"

```

# Test source

```ts
  1   | ﻿import { test } from '@playwright/test';
  2   | 
  3   | test('PHASE 10 - inspect actual canonical frontend DOM', async ({ page }) => {
  4   | 
  5   |   const failures: string[] = [];
  6   | 
  7   |   page.on('console', msg => {
  8   |     console.log(`CONSOLE [${msg.type()}]: ${msg.text()}`);
  9   |   });
  10  | 
  11  |   page.on('requestfailed', request => {
  12  |     const line = `FAILED REQUEST: ${request.method()} ${request.url()} :: ${request.failure()?.errorText}`;
  13  |     failures.push(line);
  14  |     console.log(line);
  15  |   });
  16  | 
  17  |   const urls = [
  18  |     '/chapter/class_5_01_english_complete_101',
  19  |     '/chapter/class_5_01_english_complete_102',
  20  |     '/subject/01_english_complete',
  21  |     '/'
  22  |   ];
  23  | 
  24  |   for (const url of urls) {
  25  | 
  26  |     console.log('');
  27  |     console.log('======================================================');
  28  |     console.log(`INSPECTING ${url}`);
  29  |     console.log('======================================================');
  30  | 
> 31  |     await page.goto(url, {
      |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  32  |       waitUntil: 'networkidle',
  33  |       timeout: 60000
  34  |     });
  35  | 
  36  |     await page.waitForTimeout(2000);
  37  | 
  38  |     console.log(`FINAL URL: ${page.url()}`);
  39  |     console.log(`PAGE TITLE: ${await page.title()}`);
  40  | 
  41  |     const body = await page.locator('body').innerText().catch(() => '');
  42  |     console.log('');
  43  |     console.log('--- BODY TEXT ---');
  44  |     console.log(body.substring(0, 12000));
  45  | 
  46  |     const subjectLinks = await page.locator('a[href*="/subject/"]').evaluateAll(
  47  |       els => els.map(e => ({
  48  |         text: (e.textContent || '').trim(),
  49  |         href: (e as HTMLAnchorElement).getAttribute('href')
  50  |       }))
  51  |     );
  52  | 
  53  |     console.log('');
  54  |     console.log('--- SUBJECT LINKS ---');
  55  |     console.log(JSON.stringify(subjectLinks, null, 2));
  56  | 
  57  |     const chapterLinks = await page.locator('a[href*="/chapter/"]').evaluateAll(
  58  |       els => els.map(e => ({
  59  |         text: (e.textContent || '').trim(),
  60  |         href: (e as HTMLAnchorElement).getAttribute('href')
  61  |       })).slice(0, 20)
  62  |     );
  63  | 
  64  |     console.log('');
  65  |     console.log('--- CHAPTER LINKS ---');
  66  |     console.log(JSON.stringify(chapterLinks, null, 2));
  67  | 
  68  |     const gurukulAttributes = await page.locator('*').evaluateAll(els => {
  69  |       const result: any[] = [];
  70  | 
  71  |       for (const el of els) {
  72  |         const attrs = Array.from(el.attributes)
  73  |           .filter(a => a.name.startsWith('data-gurukul'))
  74  |           .map(a => ({
  75  |             name: a.name,
  76  |             value: a.value
  77  |           }));
  78  | 
  79  |         if (attrs.length) {
  80  |           result.push({
  81  |             tag: el.tagName,
  82  |             text: (el.textContent || '').trim().substring(0, 200),
  83  |             attrs
  84  |           });
  85  |         }
  86  |       }
  87  | 
  88  |       return result.slice(0, 100);
  89  |     });
  90  | 
  91  |     console.log('');
  92  |     console.log('--- GURUKUL DATA ATTRIBUTES ---');
  93  |     console.log(JSON.stringify(gurukulAttributes, null, 2));
  94  | 
  95  |     console.log('');
  96  |     console.log('--- HEADINGS ---');
  97  | 
  98  |     const headings = await page.locator('h1,h2,h3,h4').evaluateAll(
  99  |       els => els.map(e => ({
  100 |         tag: e.tagName,
  101 |         text: (e.textContent || '').trim()
  102 |       }))
  103 |     );
  104 | 
  105 |     console.log(JSON.stringify(headings, null, 2));
  106 |   }
  107 | 
  108 |   console.log('');
  109 |   console.log('======================================================');
  110 |   console.log('FAILED REQUEST SUMMARY');
  111 |   console.log('======================================================');
  112 |   console.log(failures.join('\n') || 'NONE');
  113 | });
  114 | 
  115 | 
```