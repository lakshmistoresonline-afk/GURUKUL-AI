import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import '../widgets/mind_map_widget.dart';

class MindMapScreen extends StatelessWidget {
  final String topic;
  final List<String> branches;

  const MindMapScreen({super.key, required this.topic, required this.branches});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: Text('$topic Mind Map'),
        backgroundColor: DesignSystem.background,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DesignSystem.spacingLg),
        child: Center(
          child: Column(
            children: [
              const SizedBox(height: 40),
              MindMapWidget(topic: topic, branches: branches),
              const SizedBox(height: 60),
              _buildMindMapInfo(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMindMapInfo() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingLg),
      decoration: DesignSystem.cardDecoration,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.info_outline, color: DesignSystem.primary, size: 20),
              const SizedBox(width: 8),
              Text('Interactive View', style: DesignSystem.title.copyWith(fontSize: 16)),
            ],
          ),
          const SizedBox(height: 12),
          const Text(
            'This mind map represents the key concepts and their relationships within the chapter. Tap on nodes to deep dive into specific sub-topics.',
            style: DesignSystem.bodySmall,
          ),
        ],
      ),
    );
  }
}
