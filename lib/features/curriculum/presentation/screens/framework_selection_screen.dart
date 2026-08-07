import 'package:flutter/material.dart';

class FrameworkSelectionScreen extends StatefulWidget {
  const FrameworkSelectionScreen({super.key});

  @override
  State<FrameworkSelectionScreen> createState() => _FrameworkSelectionScreenState();
}

class _FrameworkSelectionScreenState extends State<FrameworkSelectionScreen> {
  String _selectedBoard = 'CBSE';
  String _selectedGrade = 'Class 6';
  String _selectedMedium = 'English';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Change Framework')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Board', style: TextStyle(fontWeight: FontWeight.bold)),
            DropdownButton<String>(
              isExpanded: true,
              value: _selectedBoard,
              items: ['CBSE', 'NCERT', 'State Board (Delhi)', 'State Board (Karnataka)'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (v) => setState(() => _selectedBoard = v!),
            ),
            const SizedBox(height: 24),
            const Text('Grade', style: TextStyle(fontWeight: FontWeight.bold)),
            DropdownButton<String>(
              isExpanded: true,
              value: _selectedGrade,
              items: ['Class 5', 'Class 6', 'Class 7', 'Class 8'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (v) => setState(() => _selectedGrade = v!),
            ),
            const SizedBox(height: 24),
            const Text('Medium', style: TextStyle(fontWeight: FontWeight.bold)),
            DropdownButton<String>(
              isExpanded: true,
              value: _selectedMedium,
              items: ['English', 'Hindi', 'Kannada', 'Tamil'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (v) => setState(() => _selectedMedium = v!),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Save Framework'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
