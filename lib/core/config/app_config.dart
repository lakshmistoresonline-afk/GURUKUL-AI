class AppConfig {
  static const String geminiApiKey = String.fromEnvironment(
    'GEMINI_API_KEY',
    defaultValue: 'YOUR_GEMINI_API_KEY',
  );

  static const String environment = String.fromEnvironment(
    'APP_ENV',
    defaultValue: 'development',
  );

  static const bool useLocalAi = bool.fromEnvironment(
    'USE_LOCAL_AI',
    defaultValue: true,
  );

  static const String ollamaBaseUrl = String.fromEnvironment(
    'OLLAMA_URL',
    defaultValue: 'http://localhost:11434',
  );
}
