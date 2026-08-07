import 'package:flutter/material.dart';
import 'dart:math' as math;

class FractionsSimulation extends StatefulWidget {
  const FractionsSimulation({super.key});

  @override
  State<FractionsSimulation> createState() => _FractionsSimulationState();
}

class _FractionsSimulationState extends State<FractionsSimulation> {
  int _parts = 4;
  int _selected = 1;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Text('Interactive Fractions', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 20),
        SizedBox(
          height: 200,
          width: 200,
          child: CustomPaint(
            painter: FractionPainter(parts: _parts, selected: _selected),
          ),
        ),
        const SizedBox(height: 40),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Column(
              children: [
                Text('Total Parts: $_parts'),
                Slider(
                  value: _parts.toDouble(),
                  min: 1,
                  max: 12,
                  divisions: 11,
                  onChanged: (v) => setState(() {
                    _parts = v.round();
                    if (_selected > _parts) _selected = _parts;
                  }),
                ),
              ],
            ),
            const SizedBox(width: 20),
            Column(
              children: [
                Text('Selected: $_selected'),
                Slider(
                  value: _selected.toDouble(),
                  min: 0,
                  max: _parts.toDouble(),
                  divisions: _parts,
                  onChanged: (v) => setState(() => _selected = v.round()),
                ),
              ],
            ),
          ],
        ),
        const SizedBox(height: 20),
        Text('Result: $_selected / $_parts', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.blue)),
      ],
    );
  }
}

class FractionPainter extends CustomPainter {
  final int parts;
  final int selected;

  FractionPainter({required this.parts, required this.selected});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;
    final paint = Paint()
      ..color = Colors.grey.shade300
      ..style = PaintingStyle.fill;

    canvas.drawCircle(center, radius, paint);

    if (parts > 0) {
      final selectedPaint = Paint()
        ..color = Colors.blue
        ..style = PaintingStyle.fill;

      final angle = (2 * math.pi) / parts;

      for (int i = 0; i < selected; i++) {
        canvas.drawArc(
          Rect.fromCircle(center: center, radius: radius),
          i * angle - math.pi / 2,
          angle,
          true,
          selectedPaint,
        );
      }

      final linePaint = Paint()
        ..color = Colors.white
        ..strokeWidth = 2;

      for (int i = 0; i < parts; i++) {
        final x = center.dx + radius * math.cos(i * angle - math.pi / 2);
        final y = center.dy + radius * math.sin(i * angle - math.pi / 2);
        canvas.drawLine(center, Offset(x, y), linePaint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
