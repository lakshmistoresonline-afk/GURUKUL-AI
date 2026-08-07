import 'package:flutter/material.dart';
import '../../curriculum/presentation/screens/content_viewer_screen.dart';

class ContentStoreScreen extends StatelessWidget {
  const ContentStoreScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final contents = [
      {'title': 'Science Ch 1 PDF', 'type': ContentType.pdf, 'size': '2.4 MB'},
      {'title': 'Math Geometry HTML', 'type': ContentType.html, 'size': '1.1 MB'},
      {'title': 'History Video', 'type': ContentType.video, 'size': '15 MB'},
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Content Store')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: contents.length,
        itemBuilder: (context, index) {
          final c = contents[index];
          final type = c['type'] as ContentType;
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            child: ListTile(
              leading: Icon(_getIcon(type), color: Colors.blue),
              title: Text(c['title'] as String),
              subtitle: Text(c['size'] as String),
              trailing: IconButton(
                onPressed: () {},
                icon: const Icon(Icons.download_for_offline_outlined),
              ),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ContentViewerScreen(
                      contentId: 'store_$index',
                      title: c['title'] as String,
                      url: 'https://example.com/demo.pdf', // Mock
                      type: type,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }

  IconData _getIcon(ContentType type) {
    switch (type) {
      case ContentType.pdf: return Icons.picture_as_pdf;
      case ContentType.html: return Icons.html;
      case ContentType.video: return Icons.play_circle;
    }
  }
}
