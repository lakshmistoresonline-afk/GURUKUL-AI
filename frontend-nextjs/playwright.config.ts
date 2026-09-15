import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export const STORAGE_STATE = path.join(__dirname, 'playwright/.auth/user.json');

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [['html', { open: 'never' }], ['json', { outputFile: 'test-results/report.json' }]],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 20000,
    navigationTimeout: 30000,
  },
  timeout: 120000,
  webServer: [
    {
      command: 'python backend/run_server.py',
      url: 'http://localhost:8000/api/v1/student/catalog',
      reuseExistingServer: true,
      cwd: '..',
      timeout: 30000,
    },
    {
      command: 'npm --prefix frontend-nextjs run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: true,
      cwd: '..',
      timeout: 30000,
    },
  ],
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: STORAGE_STATE },
      dependencies: ['setup'],
    },
  ],
});
