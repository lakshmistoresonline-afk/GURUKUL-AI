import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const STORAGE_STATE = path.join(__dirname, '../../playwright/.auth/user.json');
const manifestPath = 'D:/GURUKUL-AI/Contents/GURUKUL_AI_CLASS_5_STUDENT_DASHBOARD_READY_FINAL_V3/dashboard/chapter_display_manifest.json';

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
const chapters = manifest.chapters;

test.describe('Class 5 Chapter Audit', () => {
  test.use({ storageState: STORAGE_STATE });

  for (const chapter of chapters) {
    test(`Audit Chapter: ${chapter.chapter_id} - ${chapter.chapter_name}`, async ({ page }) => {
      await page.goto(`/chapter/${chapter.chapter_id}`);

      // 1. Loading State
      await expect(page.getByText('Synchronizing Neural Stream')).not.toBeVisible({ timeout: 30000 });

      // 2. Verification
      const title = chapter.chapter_name === 'UNKNOWN' ? `Unit ${chapter.chapter_number}` : chapter.chapter_name;
      const expectedTitle = title.replace(/\s+/g, ' ').trim();

      const h1 = page.locator('h1');
      await expect(h1).toBeVisible({ timeout: 15000 });
      const h1Text = await h1.innerText();
      expect(h1Text.toLowerCase().replace(/\s+/g, ' ')).toContain(expectedTitle.toLowerCase());

      // 3. Section Availability
      const tabs = page.locator('button:has(svg)');
      const tabCount = await tabs.count();
      expect(tabCount).toBeGreaterThan(0);

      // 4. Content Scan
      const bodyText = await page.innerText('body');
      const placeholders = ['Concept 1', 'Concept 2', 'Concept 3', 'Concept 4', 'Concept 5'];
      for (const p of placeholders) {
        expect(bodyText, `Placeholder found: ${p}`).not.toContain(p);
      }

      const artifacts = ['.indd', 'Reprint 2026-27'];
      for (const a of artifacts) {
        expect(bodyText, `Extraction artifact found: ${a}`).not.toContain(a);
      }

      await expect(page.getByText('Application error: a client-side exception')).not.toBeVisible();
    });
  }
});
