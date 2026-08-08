import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/learning_journey_screen.dart';
import 'package:project_gurukul_ai/features/content_acquisition/controllers/acquisition_bloc.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';
import 'package:path/path.dart' as p;
import '../bloc/auth_bloc.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isPasswordVisible = false;

  // Quick Start Selections
  int? _selectedClass;
  String? _selectedSubject;
  Map<String, dynamic>? _selectedChapter;

  List<int> _classes = [];
  List<String> _subjects = [];
  List<Map<String, dynamic>> _chapters = [];

  @override
  void initState() {
    super.initState();
    _loadInitialData();
  }

  Future<void> _loadInitialData() async {
    final repo = sl<FrameworkRepository>();
    final classes = await repo.getClasses();
    if (mounted) {
      setState(() {
        _classes = classes;
        if (classes.isNotEmpty) {
          _selectedClass = classes.first;
          _onClassChanged(_selectedClass!);
        }
      });
    }
  }

  Future<void> _onClassChanged(int level) async {
    final repo = sl<FrameworkRepository>();
    final subjects = await repo.getSubjects(level);
    if (mounted) {
      setState(() {
        _selectedClass = level;
        _subjects = subjects;
        _selectedSubject = subjects.isNotEmpty ? subjects.first : null;
        _chapters = [];
        _selectedChapter = null;
        if (_selectedSubject != null) {
          _onSubjectChanged(_selectedSubject!);
        }
      });
    }
  }

  Future<void> _onSubjectChanged(String subject) async {
    final repo = sl<FrameworkRepository>();
    final chapters = await repo.getChapters(_selectedClass!, subject);
    if (mounted) {
      setState(() {
        _selectedSubject = subject;
        _chapters = chapters;
        _selectedChapter = chapters.isNotEmpty ? chapters.first : null;
      });
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter both email and password')),
      );
      return;
    }

    context.read<AuthBloc>().add(AuthLoginRequested(email, password));
  }

  Future<void> _handleQuickStart() async {
    if (_selectedChapter == null) return;

    final repo = sl<FrameworkRepository>();
    final node = await repo.getConceptNode(_selectedChapter!['id']);

    if (node != null && mounted) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: node)),
      );
    }
  }

  Future<void> _handleUploadAndEnrich() async {
    // 1. Pick PDF
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result == null || result.files.single.path == null) return;

    final pickedFile = File(result.files.single.path!);
    final fileName = result.files.single.name;

    // 2. Show Processing Dialog
    if (!mounted) return;
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const AlertDialog(
        title: Text('Enriching Lesson'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(),
            const SizedBox(height: 16),
            Text('Extracting and generating content via Local AI...', textAlign: TextAlign.center),
          ],
        ),
      ),
    );

    try {
      // 3. Setup context
      final classLevel = _selectedClass ?? 5;
      final subject = _selectedSubject ?? 'General';
      final classDir = 'class_${classLevel.toString().padLeft(2, '0')}';

      // 4. Copy to Source
      final destDir = Directory('D:/GURUKUL-AI/datasets/ncert_source/$classDir/${subject.toLowerCase()}');
      if (!await destDir.exists()) await destDir.create(recursive: true);
      final destPath = p.join(destDir.path, fileName);
      await pickedFile.copy(destPath);

      // 5. Trigger Scan
      if (!mounted) return;
      context.read<AcquisitionBloc>().add(StartScan());

      // Since this is a one-by-one flow, we wait for the scan and subsequent processing to be available.
      await Future.delayed(const Duration(seconds: 2));

      if (!mounted) return;
      Navigator.pop(context); // Close dialog

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('File uploaded successfully! It is now being processed in the background.')),
      );

      _loadInitialData(); // Refresh chapters dropdown

    } catch (e) {
      if (!mounted) return;
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Upload failed: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(DesignSystem.spacingLg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 40),
              const Center(
                child: Hero(
                  tag: 'app_logo',
                  child: Icon(Icons.school, size: 80, color: DesignSystem.primary),
                ),
              ),
              const SizedBox(height: 24),
              Text(
                'Gurukul AI',
                textAlign: TextAlign.center,
                style: DesignSystem.h1.copyWith(fontSize: 32),
              ),
              const SizedBox(height: 8),
              Text(
                'Personalized Learning Powered by local AI',
                textAlign: TextAlign.center,
                style: DesignSystem.bodySmall.copyWith(fontSize: 16),
              ),
              const SizedBox(height: 40),

              // Login Form
              Container(
                padding: const EdgeInsets.all(DesignSystem.spacingMd),
                decoration: DesignSystem.cardDecoration,
                child: Column(
                  children: [
                    TextField(
                      controller: _emailController,
                      decoration: InputDecoration(
                        labelText: 'Email Address',
                        prefixIcon: const Icon(Icons.email_outlined),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                        ),
                      ),
                      keyboardType: TextInputType.emailAddress,
                    ),
                    const SizedBox(height: 20),
                    TextField(
                      controller: _passwordController,
                      decoration: InputDecoration(
                        labelText: 'Password',
                        prefixIcon: const Icon(Icons.lock_outline),
                        suffixIcon: IconButton(
                          icon: Icon(
                            _isPasswordVisible ? Icons.visibility_off : Icons.visibility,
                          ),
                          onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible),
                        ),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                        ),
                      ),
                      obscureText: !_isPasswordVisible,
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: FilledButton(
                        onPressed: _handleLogin,
                        style: FilledButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                          ),
                        ),
                        child: const Text('Login to Dashboard', style: TextStyle(fontSize: 16)),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 32),
              Row(
                children: [
                  const Expanded(child: Divider()),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    child: Text('OR QUICK START', style: DesignSystem.labelSmall),
                  ),
                  const Expanded(child: Divider()),
                ],
              ),
              const SizedBox(height: 32),

              // Quick Start Selection
              Container(
                padding: const EdgeInsets.all(DesignSystem.spacingMd),
                decoration: DesignSystem.cardDecoration.copyWith(
                  color: DesignSystem.primary.withValues(alpha: 0.05),
                  border: Border.all(color: DesignSystem.primary.withValues(alpha: 0.2)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Select Your Context', style: DesignSystem.titleSmall),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<int>(
                      value: _selectedClass,
                      decoration: const InputDecoration(labelText: 'Class', border: OutlineInputBorder()),
                      items: _classes.map((l) => DropdownMenuItem(value: l, child: Text('Class $l'))).toList(),
                      onChanged: (v) => _onClassChanged(v!),
                    ),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<String>(
                      value: _selectedSubject,
                      decoration: const InputDecoration(labelText: 'Subject', border: OutlineInputBorder()),
                      items: _subjects.map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
                      onChanged: (v) => _onSubjectChanged(v!),
                    ),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<Map<String, dynamic>>(
                      value: _selectedChapter,
                      decoration: const InputDecoration(labelText: 'Chapter', border: OutlineInputBorder()),
                      items: _chapters.map((c) => DropdownMenuItem(value: c, child: Text(c['title'] ?? 'Untitled'))).toList(),
                      onChanged: (v) => setState(() => _selectedChapter = v),
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        onPressed: _selectedChapter != null ? _handleQuickStart : null,
                        icon: const Icon(Icons.bolt_rounded),
                        label: const Text('Launch Lesson Directly'),
                        style: OutlinedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 14),
                          side: const BorderSide(color: DesignSystem.primary),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      child: FilledButton.icon(
                        onPressed: _handleUploadAndEnrich,
                        icon: const Icon(Icons.upload_file),
                        label: const Text('Upload & Enrich PDF'),
                        style: FilledButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 14),
                          backgroundColor: DesignSystem.secondary,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 40),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text("Don't have an account?"),
                  TextButton(
                    onPressed: () {},
                    child: const Text('Sign Up', style: TextStyle(fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}
