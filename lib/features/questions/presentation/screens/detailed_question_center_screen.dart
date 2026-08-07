import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../domain/models/question_paper.dart';

class DetailedQuestionCenterScreen extends StatefulWidget {
  final String subject;
  const DetailedQuestionCenterScreen({super.key, required this.subject});

  @override
  State<DetailedQuestionCenterScreen> createState() => _DetailedQuestionCenterScreenState();
}

class _DetailedQuestionCenterScreenState extends State<DetailedQuestionCenterScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.subject} Question Bank'),
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: const [
            Tab(text: 'Chapter-wise'),
            Tab(text: 'Unit Tests'),
            Tab(text: 'Model Papers'),
            Tab(text: 'Bookmarks'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildChapterList(),
          _buildPaperList('Unit Test'),
          _buildPaperList('Model Paper'),
          _buildPaperList('Bookmark'),
        ],
      ),
    );
  }

  Widget _buildChapterList() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: 10,
      itemBuilder: (context, index) {
        return ExpansionTile(
          title: Text('Chapter ${index + 1}: Important Concepts'),
          children: [
            ListTile(title: const Text('Practice Set 1 (Basic)'), trailing: const Icon(Icons.chevron_right), onTap: () {}),
            ListTile(title: const Text('Practice Set 2 (Advanced)'), trailing: const Icon(Icons.chevron_right), onTap: () {}),
            ListTile(title: const Text('HOTS Questions'), trailing: const Icon(Icons.local_fire_department, color: Colors.orange), onTap: () {}),
          ],
        );
      },
    );
  }

  Widget _buildPaperList(String type) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: 5,
      itemBuilder: (context, index) {
        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          child: ListTile(
            leading: const CircleAvatar(child: Icon(Icons.description)),
            title: Text('$type ${2024 - index}'),
            subtitle: const Text('80 Marks • 3 Hours'),
            trailing: const Icon(Icons.download),
            onTap: () {},
          ),
        );
      },
    );
  }
}
