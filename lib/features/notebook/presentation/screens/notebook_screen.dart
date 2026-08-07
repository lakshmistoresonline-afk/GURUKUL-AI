import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../domain/models/note.dart';
import '../../../ai/data/ai_tutor_service.dart';

class NotebookScreen extends StatefulWidget {
  const NotebookScreen({super.key});

  @override
  State<NotebookScreen> createState() => _NotebookScreenState();
}

class _NotebookScreenState extends State<NotebookScreen> {
  final List<Note> _notes = [];
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Smart Notebook')),
      body: _notes.isEmpty
          ? const Center(child: Text('No notes yet. Start writing!'))
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _notes.length,
              itemBuilder: (context, index) {
                final note = _notes[index];
                return _NoteCard(note: note);
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _createNewNote,
        child: const Icon(Icons.add),
      ),
    );
  }

  void _createNewNote() {
    // Show dialog or navigate to editor
  }
}

class _NoteCard extends StatelessWidget {
  final Note note;
  const _NoteCard({required this.note});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(note.title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(note.content, maxLines: 3, overflow: TextOverflow.ellipsis),
            const SizedBox(height: 12),
            if (note.aiSummary != null)
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: Colors.blue.shade50, borderRadius: BorderRadius.circular(8)),
                child: Row(
                  children: [
                    const Icon(Icons.auto_awesome, size: 16, color: Colors.blue),
                    const SizedBox(width: 8),
                    Expanded(child: Text(note.aiSummary!, style: const TextStyle(fontSize: 12, fontStyle: FontStyle.italic))),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}
