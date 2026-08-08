import 'package:flutter/material.dart';
import '../../../teacher/domain/models/homework.dart';

class HomeworkScreen extends StatefulWidget {
  const HomeworkScreen({super.key});

  @override
  State<HomeworkScreen> createState() => _HomeworkScreenState();
}

class _HomeworkScreenState extends State<HomeworkScreen> {
  final List<Homework> _homeworkList = [
    Homework(id: '1', title: 'Chapter 1: The Fish Tale', description: 'Solve the word problems on page 5.', subject: 'Mathematics', dueDate: DateTime.now().add(const Duration(days: 1))),
    Homework(id: '2', title: 'Super Senses Observation', description: 'Observe and list 3 super senses of a pet or local animal.', subject: 'EVS', dueDate: DateTime.now().add(const Duration(days: 2))),
    Homework(id: '3', title: 'Hindi: Raakh ki Rassi', description: 'Write a summary of the story in your own words.', subject: 'Hindi', dueDate: DateTime.now().add(const Duration(days: 3))),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Homework')),
      body: ListView.builder(
        padding: const EdgeInsets.all(20),
        itemCount: _homeworkList.length,
        itemBuilder: (context, index) {
          final hw = _homeworkList[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            child: ListTile(
              contentPadding: const EdgeInsets.all(16),
              title: Text(hw.title, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 4),
                  Text(hw.description),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(Icons.timer_outlined, size: 14, color: Colors.grey),
                      const SizedBox(width: 4),
                      Text('Due: ${hw.dueDate.day}/${hw.dueDate.month}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                    ],
                  ),
                ],
              ),
              trailing: FilledButton.tonal(onPressed: () {}, child: const Text('Submit')),
            ),
          );
        },
      ),
    );
  }
}
