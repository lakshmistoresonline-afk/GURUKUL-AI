import { test, expect } from '@playwright/test';

const API_URL =
  process.env.NEXT_PUBLIC_API_URL_STUDENT ||
  'http://127.0.0.1:8000/api/v1/student';

test.describe('Canonical Student Chapter Audit', () => {
  test('All Class 5 chapters render from the canonical API', async ({ page, request }) => {
    const catalogResponse = await request.get(`${API_URL}/catalog`);

    expect(
      catalogResponse.ok(),
      `Catalog request failed: ${catalogResponse.status()}`
    ).toBeTruthy();

    const catalog = await catalogResponse.json();

    const class5 = catalog.classes?.find(
      (item: any) => item.id === 'class_5'
    );

    expect(
      class5,
      'Canonical Class 5 not found in API catalog'
    ).toBeTruthy();

    const chapters: Array<{
      id: string;
      chapter_id: string;
      title?: string;
      chapter_name?: string;
    }> = [];

    for (const subject of class5.subjects ?? []) {
      for (const chapter of subject.chapters ?? []) {
        chapters.push(chapter);
      }
    }

    expect(chapters.length).toBe(47);

    console.log(
      `Canonical Class 5 chapters discovered: ${chapters.length}`
    );

    for (const chapter of chapters) {
      const canonicalChapterId = chapter.id;
      const chapterNumber = chapter.chapter_id;
      const expectedTitle =
        chapter.title ||
        chapter.chapter_name ||
        `Chapter ${chapterNumber}`;

      expect(
        canonicalChapterId,
        `Missing canonical ID for chapter ${chapterNumber}`
      ).toBeTruthy();

      await test.step(
        `Audit ${canonicalChapterId} - ${expectedTitle}`,
        async () => {
          await page.goto(`/chapter/${canonicalChapterId}`);

          await expect(
            page.getByText('Synchronizing Neural Stream')
          ).not.toBeVisible({ timeout: 30000 });

          const bodyText = await page.innerText('body');

          expect(
            bodyText,
            `Chapter Not Found for ${canonicalChapterId}`
          ).not.toContain('Chapter Not Found');

          const h1 = page.locator('header h1');

          await expect(
            h1,
            `Missing H1 for ${canonicalChapterId}`
          ).toBeVisible({ timeout: 15000 });

          const h1Text = (await h1.innerText())
            .replace(/\s+/g, ' ')
            .trim();

          expect(
            h1Text.toLowerCase(),
            `Unexpected chapter title for ${canonicalChapterId}`
          ).toContain(
            expectedTitle
              .toLowerCase()
              .replace(/\s+/g, ' ')
              .trim()
          );

          const tabs = page.locator('button:has(svg)');

          expect(
            await tabs.count(),
            `No chapter navigation controls for ${canonicalChapterId}`
          ).toBeGreaterThan(0);

          for (const placeholder of [
            'Concept 1',
            'Concept 2',
            'Concept 3',
            'Concept 4',
            'Concept 5',
          ]) {
            expect(
              bodyText,
              `Placeholder found in ${canonicalChapterId}: ${placeholder}`
            ).not.toContain(placeholder);
          }

          for (const artifact of ['.indd', 'Reprint 2026-27']) {
            expect(
              bodyText,
              `Extraction artifact found in ${canonicalChapterId}: ${artifact}`
            ).not.toContain(artifact);
          }

          await expect(
            page.getByText('Application error: a client-side exception')
          ).not.toBeVisible();
        }
      );
    }

    console.log(
      `Canonical Class 5 chapter audit completed: ${chapters.length} chapters`
    );
  });
});
