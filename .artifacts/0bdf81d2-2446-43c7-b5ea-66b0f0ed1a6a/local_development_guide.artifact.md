# Project Gurukul AI: Local Development Guide

This guide provides the complete set of steps to set up, run, and test Project Gurukul AI on your local machine.

## 1. Environment Setup

### Flutter SDK
1.  **Download**: Get the Flutter SDK from [flutter.dev](https://docs.flutter.dev/get-started/install/windows).
2.  **Extract**: Extract the zip file to a permanent location (e.g., `C:\src\flutter`).
3.  **PATH Configuration**:
    - Press **Windows Key**, type "env", and select "Edit the system environment variables".
    - Click **Environment Variables**.
    - Under **User variables**, find `Path` and click **Edit**.
    - Click **New** and add the path to Flutter's `bin` folder: `C:\src\flutter\bin`.
    - Click **OK** to save.
4.  **Verify**: Open a **new** terminal and run:
    ```bash
    flutter --version
    ```

### Android Setup (Optional but Recommended)
- Install **Android Studio**.
- Install the **Android SDK Build-Tools** and **Platform-Tools**.
- Ensure your `ANDROID_USER_HOME` is set correctly if you encounter Gradle errors.

---

## 2. Project Initialization

Navigate to the project root (`G:\PROJECT GURUKUL AI`) and run:

```bash
# 1. Clear any old build artifacts
flutter clean

# 2. Fetch all dependencies
flutter pub get

# 3. Check for any environment issues
flutter doctor
```

---

## 3. Running the Application

### Browser (Web)
This is the fastest way to test the UI and AI Tutor.
```bash
flutter run -d chrome --dart-define=GEMINI_API_KEY=your_key_here
```

### Android Emulator / Physical Device
Ensure a device is connected and recognized by `flutter devices`.
```bash
flutter run -d android --dart-define=GEMINI_API_KEY=your_key_here
```

---

## 4. Key Troubleshooting

### Firebase Initialization
If the app fails to start due to Firebase errors, ensure you have the Firebase configuration for each platform.
- **Android**: `android/app/google-services.json` (Already present).
- **Web/iOS**: Run `flutterfire configure` to generate `lib/firebase_options.dart`.

### Gradle Errors
If you see errors related to `ANDROID_PREFS_ROOT` or `ANDROID_USER_HOME`:
```powershell
# In PowerShell
$env:ANDROID_PREFS_ROOT = $null
./gradlew assembleDebug
```

---

> [!IMPORTANT]
> **Gemini API Key**: The app requires a valid Google Gemini API key to function. You can get one from the [Google AI Studio](https://aistudio.google.com/).
