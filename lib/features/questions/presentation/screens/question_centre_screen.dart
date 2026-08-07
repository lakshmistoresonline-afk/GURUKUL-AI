import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class QuestionCentreScreen extends StatelessWidget {
  final String subject;
  const QuestionCentreScreen({super.key, required this.subject});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: Text('$subject Question Centre', style: DesignSystem.h2.copyWith(fontSize: 20)),
        backgroundColor: DesignSystem.background,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DesignSystem.spacingMd),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildHighFidelityHeader(),
            const SizedBox(height: DesignSystem.spacingLg),
            Text('ACTIVE QUESTION BANKS', style: DesignSystem.label),
            const SizedBox(height: DesignSystem.spacingMd),
            _buildQuestionBankItem('Previous Year Questions (PYQ)', '125 Questions', Icons.history_edu, Colors.blue),
            _buildQuestionBankItem('Exemplar Problems', '85 Questions', Icons.star_outline, Colors.orange),
            _buildQuestionBankItem('HOTS (High Order Thinking Skills)', '40 Questions', Icons.psychology, Colors.purple),
            _buildQuestionBankItem('Diagnostic Quiz', '20 Questions', Icons.fact_check_outlined, Colors.green),
            const SizedBox(height: DesignSystem.spacingXl),
            _buildComingSoonSection(),
          ],
        ),
      ),
    );
  }

  Widget _buildHighFidelityHeader() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingLg),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Colors.indigo, Colors.blue]),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
        boxShadow: DesignSystem.shadowMd,
      ),
      child: Row(
        children: [
          const Icon(Icons.help_center_rounded, color: Colors.white, size: 48),
          const SizedBox(width: DesignSystem.spacingMd),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Practice makes perfect!', style: DesignSystem.h2.copyWith(color: Colors.white, fontSize: 18)),
                const SizedBox(height: 4),
                Text('Access thousands of NCERT-aligned questions with AI-powered step-by-step solutions.',
                  style: DesignSystem.bodySmall.copyWith(color: Colors.white.withOpacity(0.9))),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuestionBankItem(String title, String count, IconData icon, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: ListTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
          child: Icon(icon, color: color),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(count),
        trailing: const Icon(Icons.chevron_right),
        onTap: () {},
      ),
    );
  }

  Widget _buildComingSoonSection() {
    return Center(
      child: Column(
        children: [
          const Icon(Icons.construction_rounded, size: 48, color: DesignSystem.textTertiary),
          const SizedBox(height: 8),
          Text('AI Adaptive Practice', style: DesignSystem.title),
          const SizedBox(height: 4),
          const Text('Coming Soon: Real-time difficulty adjustment based on your performance.',
            textAlign: TextAlign.center,
            style: TextStyle(color: DesignSystem.textTertiary, fontSize: 12)),
        ],
      ),
    );
  }
}
