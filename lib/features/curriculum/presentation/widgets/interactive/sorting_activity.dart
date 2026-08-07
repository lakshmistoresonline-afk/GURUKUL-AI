import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class SortingActivity extends StatefulWidget {
  final Map<String, List<String>> categories;
  final Function(bool) onComplete;

  const SortingActivity({super.key, required this.categories, required this.onComplete});

  @override
  State<SortingActivity> createState() => _SortingActivityState();
}

class _SortingActivityState extends State<SortingActivity> {
  late List<String> _allItems;
  final Map<String, List<String>> _currentSorting = {};

  @override
  void initState() {
    super.initState();
    _allItems = widget.categories.values.expand((x) => x).toList()..shuffle();
    for (var cat in widget.categories.keys) {
      _currentSorting[cat] = [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Text('Drag items to correct boxes', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 24),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: _allItems.map((item) => Draggable<String>(
            data: item,
            feedback: _buildItem(item, true),
            childWhenDragging: Opacity(opacity: 0.3, child: _buildItem(item, false)),
            child: _buildItem(item, false),
          )).toList(),
        ),
        const SizedBox(height: 48),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: widget.categories.keys.map((cat) => DragTarget<String>(
            onAccept: (item) {
              setState(() {
                _currentSorting[cat]!.add(item);
                _allItems.remove(item);
              });
              _checkCompletion();
            },
            builder: (context, candidateData, rejectedData) => _buildCategoryBox(cat, _currentSorting[cat]!),
          )).toList(),
        ),
      ],
    );
  }

  Widget _buildItem(String label, bool isFeedback) {
    return Material(
      color: Colors.transparent,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: DesignSystem.surface,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: Colors.grey.shade300),
          boxShadow: isFeedback ? DesignSystem.shadowMd : null,
        ),
        child: Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
      ),
    );
  }

  Widget _buildCategoryBox(String category, List<String> items) {
    return Container(
      width: 150,
      height: 200,
      decoration: BoxDecoration(
        color: DesignSystem.primary.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: DesignSystem.primary.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(8),
            decoration: const BoxDecoration(
              color: DesignSystem.primary,
              borderRadius: BorderRadius.only(topLeft: Radius.circular(11), topRight: Radius.circular(11)),
            ),
            child: Text(category, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12), textAlign: TextAlign.center),
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(8),
              children: items.map((i) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Text('• $i', style: const TextStyle(fontSize: 13)),
              )).toList(),
            ),
          ),
        ],
      ),
    );
  }

  void _checkCompletion() {
    if (_allItems.isEmpty) {
      bool allCorrect = true;
      _currentSorting.forEach((cat, items) {
        for (var item in items) {
          if (!widget.categories[cat]!.contains(item)) allCorrect = false;
        }
      });
      widget.onComplete(allCorrect);
    }
  }
}
