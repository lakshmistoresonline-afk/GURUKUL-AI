# Firebase Hosting Deployment Guide

Follow these steps to build and publish Project Gurukul AI to the web.

## 1. Local Environment Setup
Ensure you have the following installed on your machine:
- **Flutter SDK**: [Install Flutter](https://docs.flutter.dev/get-started/install/windows)
- **Node.js**: Required for Firebase CLI.
- **Firebase CLI**:
  ```bash
  npm install -g firebase-tools
  ```

## 2. Authenticate
Open your terminal and log in to Firebase:
```bash
firebase login
```

## 3. Build the Web Application
Run the Flutter build command to generate the `build/web` directory:
```bash
flutter build web --dart-define=GEMINI_API_KEY=your_actual_key_here
```

## 4. Deploy to Firebase
Once the build is complete, deploy the hosting configuration:
```bash
firebase deploy --only hosting
```

## 5. View Your Live Site
After a successful deployment, Firebase will provide a URL. It should be:
**https://com-ncert-projectgurukul-e5e60.web.app**

---

> [!TIP]
> **Custom Domain:** If you want to use a custom domain (e.g., `learn.gurukul.ai`), you can add it in the Firebase Console under the Hosting section.

> [!WARNING]
> **API Keys:** Never hardcode your `GEMINI_API_KEY` in the source code. Always pass it via `--dart-define` during the build process as shown in step 3.
