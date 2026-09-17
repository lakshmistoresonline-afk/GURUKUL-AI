# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend-nextjs\tests\e2e\chapter_audit.spec.ts >> Canonical Student Chapter Audit >> All Class 5 chapters render from the canonical API
- Location: frontend-nextjs\tests\e2e\chapter_audit.spec.ts:8:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/chapter/class_5_01_english_complete_101", waiting until "load"

```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | const API_URL =
  4   |   process.env.NEXT_PUBLIC_API_URL_STUDENT ||
  5   |   'http://127.0.0.1:8000/api/v1/student';
  6   | 
  7   | test.describe('Canonical Student Chapter Audit', () => {
  8   |   test('All Class 5 chapters render from the canonical API', async ({ page, request }) => {
  9   |     const catalogResponse = await request.get(`${API_URL}/catalog`);
  10  | 
  11  |     expect(
  12  |       catalogResponse.ok(),
  13  |       `Catalog request failed: ${catalogResponse.status()}`
  14  |     ).toBeTruthy();
  15  | 
  16  |     const catalog = await catalogResponse.json();
  17  | 
  18  |     const class5 = catalog.classes?.find(
  19  |       (item: any) => item.id === 'class_5'
  20  |     );
  21  | 
  22  |     expect(
  23  |       class5,
  24  |       'Canonical Class 5 not found in API catalog'
  25  |     ).toBeTruthy();
  26  | 
  27  |     const chapters: Array<{
  28  |       id: string;
  29  |       chapter_id: string;
  30  |       title?: string;
  31  |       chapter_name?: string;
  32  |     }> = [];
  33  | 
  34  |     for (const subject of class5.subjects ?? []) {
  35  |       for (const chapter of subject.chapters ?? []) {
  36  |         chapters.push(chapter);
  37  |       }
  38  |     }
  39  | 
  40  |     expect(chapters.length).toBe(47);
  41  | 
  42  |     console.log(
  43  |       `Canonical Class 5 chapters discovered: ${chapters.length}`
  44  |     );
  45  | 
  46  |     for (const chapter of chapters) {
  47  |       const canonicalChapterId = chapter.id;
  48  |       const chapterNumber = chapter.chapter_id;
  49  |       const expectedTitle =
  50  |         chapter.title ||
  51  |         chapter.chapter_name ||
  52  |         `Chapter ${chapterNumber}`;
  53  | 
  54  |       expect(
  55  |         canonicalChapterId,
  56  |         `Missing canonical ID for chapter ${chapterNumber}`
  57  |       ).toBeTruthy();
  58  | 
  59  |       await test.step(
  60  |         `Audit ${canonicalChapterId} - ${expectedTitle}`,
  61  |         async () => {
> 62  |           await page.goto(`/chapter/${canonicalChapterId}`);
      |                      ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  63  | 
  64  |           await expect(
  65  |             page.getByText('Synchronizing Neural Stream')
  66  |           ).not.toBeVisible({ timeout: 30000 });
  67  | 
  68  |           const bodyText = await page.innerText('body');
  69  | 
  70  |           expect(
  71  |             bodyText,
  72  |             `Chapter Not Found for ${canonicalChapterId}`
  73  |           ).not.toContain('Chapter Not Found');
  74  | 
  75  |           const h1 = page.locator('header h1');
  76  | 
  77  |           await expect(
  78  |             h1,
  79  |             `Missing H1 for ${canonicalChapterId}`
  80  |           ).toBeVisible({ timeout: 15000 });
  81  | 
  82  |           const h1Text = (await h1.innerText())
  83  |             .replace(/\s+/g, ' ')
  84  |             .trim();
  85  | 
  86  |           expect(
  87  |             h1Text.toLowerCase(),
  88  |             `Unexpected chapter title for ${canonicalChapterId}`
  89  |           ).toContain(
  90  |             expectedTitle
  91  |               .toLowerCase()
  92  |               .replace(/\s+/g, ' ')
  93  |               .trim()
  94  |           );
  95  | 
  96  |           const tabs = page.locator('button:has(svg)');
  97  | 
  98  |           expect(
  99  |             await tabs.count(),
  100 |             `No chapter navigation controls for ${canonicalChapterId}`
  101 |           ).toBeGreaterThan(0);
  102 | 
  103 |           for (const placeholder of [
  104 |             'Concept 1',
  105 |             'Concept 2',
  106 |             'Concept 3',
  107 |             'Concept 4',
  108 |             'Concept 5',
  109 |           ]) {
  110 |             expect(
  111 |               bodyText,
  112 |               `Placeholder found in ${canonicalChapterId}: ${placeholder}`
  113 |             ).not.toContain(placeholder);
  114 |           }
  115 | 
  116 |           for (const artifact of ['.indd', 'Reprint 2026-27']) {
  117 |             expect(
  118 |               bodyText,
  119 |               `Extraction artifact found in ${canonicalChapterId}: ${artifact}`
  120 |             ).not.toContain(artifact);
  121 |           }
  122 | 
  123 |           await expect(
  124 |             page.getByText('Application error: a client-side exception')
  125 |           ).not.toBeVisible();
  126 |         }
  127 |       );
  128 |     }
  129 | 
  130 |     console.log(
  131 |       `Canonical Class 5 chapter audit completed: ${chapters.length} chapters`
  132 |     );
  133 |   });
  134 | });
  135 | 
```