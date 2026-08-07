import 'package:flutter/material.dart';

class MatchingActivity extends StatefulWidget {
  final Map<String, String> pairs;
  final Function(bool) onComplete;

  const MatchingActivity({
    super.key,
    required this.pairs,
    required this.onComplete,
  });

  @override
  State<MatchingActivity> createState() => _MatchingActivityState();
}

class _MatchingActivityState extends State<MatchingActivity> {
  String? _selectedLeft;
  String? _selectedRight;
  final Set<String> _matchedKeys = {};
  late List<String> _leftItems;
  late List<String> _rightItems;

  @override
  void initState() {
    super.initState();
    _leftItems = widget.pairs.keys.toList()..shuffle();
    _rightItems = widget.pairs.values.toList()..shuffle();
  }

  void _checkMatch() {
    if (_selectedLeft != null && _selectedRight != null) {
      if (widget.pairs[_selectedLeft] == _selectedRight) {
        setState(() {
          _matchedKeys.add(_selectedLeft!);
          _selectedLeft = null;
          _selectedRight = null;
        });

        if (_matchedKeys.length == widget.pairs.length) {
          widget.onComplete(true);
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Not a match, try again!'), duration: Duration(milliseconds: 500)),
        );
        setState(() {
          _selectedLeft = null;
          _selectedRight = null;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: Column(
                children: _leftItems.map((item) {
                  final isMatched = _matchedKeys.contains(item);
                  final isSelected = _selectedLeft == item;
                  return _buildItem(item, isSelected, isMatched, true);
                }).toList(),
              ),
            ),
            const SizedBox(width: 40),
            Expanded(
              child: Column(
                children: _rightItems.map((item) {
                  final isMatched = widget.pairs.entries.any((e) => e.value == item && _matchedKeys.contains(e.key));
                  final isSelected = _selectedRight == item;
                  return _buildItem(item, isSelected, isMatched, false);
                }).toList(),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildItem(String text, bool isSelected, bool isMatched, bool isLeft) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: InkWell(
        onTap: isMatched ? null : () {
          setState(() {
            if (isLeft) {
              _selectedLeft = text;
            } else {
              _selectedRight = text;
            }
          });
          _checkMatch();
        },
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: isMatched
                ? Colors.green.withValues(alpha: 0.1)
                : isSelected
                    ? Theme.of(context).primaryColor.withValues(alpha: 0.1)
                    : Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isMatched
                  ? Colors.green
                  : isSelected
                      ? Theme.of(context).primaryColor
                      : Colors.grey.shade300,
              width: 2,
            ),
          ),
          child: Text(
            text,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
              color: isMatched ? Colors.green.shade700 : Colors.black87,
            ),
          ),
        ),
      ),
    );
  }
}
