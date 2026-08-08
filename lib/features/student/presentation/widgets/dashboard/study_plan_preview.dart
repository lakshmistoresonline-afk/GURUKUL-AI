import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class StudyPlanPreview extends StatelessWidget {
  const StudyPlanPreview({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('TODAY\'S STUDY PLAN', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: DesignSystem.textSecondary)),
            TextButton(onPressed: () {}, child: const Text('View All')),
          ],
        ),
        const SizedBox(height: DesignSystem.spacingSm),
        _buildPlanItem('9:00 AM', 'Mathematics', 'The Fish Tale: Large Numbers', true),
        _buildPlanItem('11:30 AM', 'EVS', 'Super Senses: Animal Ears', false),
        _buildPlanItem('4:00 PM', 'English', 'Ice-cream Man: Rhyming Words', false),
      ],
    );
  }

  Widget _buildPlanItem(String time, String subject, String topic, bool done) {
    return Padding(
      padding: const EdgeInsets.only(bottom: DesignSystem.spacingSm),
      child: Row(
        children: [
          SizedBox(
            width: 70,
            child: Text(time, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600)),
          ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(DesignSystem.spacingMd),
              decoration: BoxDecoration(
                color: done ? Colors.green.shade50 : DesignSystem.surface,
                borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                border: Border.all(color: done ? Colors.green.shade100 : Colors.grey.shade200),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(subject, style: const TextStyle(fontWeight: FontWeight.bold)),
                        Text(topic, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                      ],
                    ),
                  ),
                  if (done)
                    const Icon(Icons.check_circle, color: Colors.green, size: 20)
                  else
                    const Icon(Icons.radio_button_unchecked, color: Colors.grey, size: 20),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
