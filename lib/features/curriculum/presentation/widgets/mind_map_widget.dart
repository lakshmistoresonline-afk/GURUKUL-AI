import 'package:flutter/material.dart';

class MindMapWidget extends StatelessWidget {
  final String topic;
  final List<String> branches;

  const MindMapWidget({super.key, required this.topic, required this.branches});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildNode(topic, isRoot: true),
        const SizedBox(height: 20),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          alignment: WrapAlignment.center,
          children: branches.map((b) => _buildNode(b)).toList(),
        ),
      ],
    );
  }

  Widget _buildNode(String text, {bool isRoot = false}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        color: isRoot ? Colors.blue : Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.blue.withValues(alpha: 0.3)),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 10, offset: const Offset(0, 4)),
        ],
      ),
      child: Text(
        text,
        style: TextStyle(
          color: isRoot ? Colors.white : Colors.blue.shade900,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
