import 'package:flutter/material.dart';

class TapRevealActivity extends StatefulWidget {
  final List<Map<String, String>> items; // [{'title': '...', 'content': '...'}]

  const TapRevealActivity({super.key, required this.items});

  @override
  State<TapRevealActivity> createState() => _TapRevealActivityState();
}

class _TapRevealActivityState extends State<TapRevealActivity> {
  final Set<int> _revealedIndices = {};

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: 1.0,
      ),
      itemCount: widget.items.length,
      itemBuilder: (context, index) {
        final item = widget.items[index];
        final isRevealed = _revealedIndices.contains(index);

        return InkWell(
          onTap: () => setState(() => _revealedIndices.add(index)),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: isRevealed ? Colors.white : Theme.of(context).primaryColor,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: Theme.of(context).primaryColor.withOpacity(0.2)),
              boxShadow: [
                BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4)),
              ],
            ),
            child: Center(
              child: isRevealed
                  ? Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(item['title']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        const SizedBox(height: 8),
                        Text(item['content']!, textAlign: TextAlign.center, style: const TextStyle(fontSize: 14)),
                      ],
                    )
                  : const Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.touch_app, color: Colors.white, size: 40),
                        SizedBox(height: 12),
                        Text('Tap to Reveal', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      ],
                    ),
            ),
          ),
        );
      },
    );
  }
}
