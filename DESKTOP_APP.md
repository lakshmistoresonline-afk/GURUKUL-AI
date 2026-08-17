# Gurukul AI Desktop App (Windows)

This directory contains the Tauri-based Windows desktop application for Gurukul AI. It serves as a lightweight standalone wrapper around the existing Next.js web application.

## Architecture

- **Frontend**: Next.js (Static Export)
- **Desktop Wrapper**: Tauri (Rust + WebView2)
- **Backend**: Remote FastAPI (Same as Web/PWA)
- **Auth**: Firebase Authentication (Same as Web/PWA)

## Prerequisites

To develop or build the desktop app locally, you need:
- [Node.js](https://nodejs.org/) (v20+)
- [Rust](https://www.rust-lang.org/) (Stable)
- [WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) (Usually pre-installed on Windows 10/11)

## Development Setup

1. Install dependencies for both frontend and desktop:
   ```bash
   cd frontend-nextjs && npm install
   cd ../desktop && npm install
   ```

2. Run in development mode:
   ```bash
   cd frontend-nextjs
   npm run desktop:dev
   ```
   This will start the Next.js dev server and launch the Tauri window pointing to `localhost:3000`.

## Production Build

1. Ensure your environment variables (Firebase, API URL) are set in `frontend-nextjs/.env.local` or `.env.production`.
2. Build the installer:
   ```bash
   cd frontend-nextjs
   npm run desktop:build
   ```
   The installer will be generated in `desktop/src-tauri/target/release/bundle/nsis/GurukulAI-Setup.exe`.

## Configuration

### Production API URL
The desktop app uses the same `NEXT_PUBLIC_BACKEND_URL` as the web app. Ensure this is set to your production API domain during the build process.

### GitHub Actions
The project includes a GitHub Action `.github/workflows/desktop-windows.yml` that automatically builds the Windows installer on manual dispatch or when a new version tag (e.g., `v1.0.0`) is pushed.

## Distribution
Students can download the `GurukulAI-Setup.exe` from the GitHub Releases page.

## Future Auto-Update Plan
Auto-updates can be enabled in the future using the built-in Tauri updater. This requires a signature key and a public update server (or GitHub Releases).

## Known Limitations
- Offline mode is not supported; an internet connection is required to communicate with the FastAPI backend and Firebase.
- External links (like YouTube) are configured to open within the application or system browser based on Tauri's security configuration.
