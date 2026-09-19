# GURUKUL AI — PWA CONFIGURATION FORENSIC REPORT

## 1. Investigation of Generated Assets
- **Files:** `frontend-nextjs/public/sw.js`, `frontend-nextjs/public/workbox-4754cb34.js`
- **Origin:** Generated automatically by the `next-pwa` webpack plugin during production builds (`npm run build`).
- **Tracked State:** Untracked in Git (`??`).
- **Git Ignore Status:** Currently NOT ignored by `.gitignore` (`git check-ignore` returns exit code 1).

## 2. Analysis
- These files are build artifacts produced dynamically by the Next.js PWA compilation process.
- Committing them is unnecessary since they are deterministically generated during `next build`.
- Leaving them untracked pollutes the working tree git status.

## 3. Recommendation
- **Recommendation:** `IGNORE`
- **Action Required:** Add service worker emission patterns (`/public/sw.js`, `/public/workbox-*.js`) to `.gitignore` during the subsequent staging phase upon user approval.
