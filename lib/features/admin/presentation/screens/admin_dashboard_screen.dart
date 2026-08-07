import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/features/content_acquisition/screens/acquisition_dashboard_screen.dart';

class AdminDashboardScreen extends StatelessWidget {
  const AdminDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Admin Console'),
      ),
      body: GridView.count(
        padding: const EdgeInsets.all(16),
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        children: [
          _buildAdminCard(context, 'Content Acquisition', Icons.cloud_download, Colors.purple, () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const AcquisitionDashboardScreen()),
            );
          }),
          _buildAdminCard(context, 'User Management', Icons.people, Colors.blue, () {}),
          _buildAdminCard(context, 'Content Manager', Icons.library_books, Colors.green, () {}),
          _buildAdminCard(context, 'System Reports', Icons.analytics, Colors.orange, () {}),
          _buildAdminCard(context, 'Notifications', Icons.notifications, Colors.red, () {}),
          _buildAdminCard(context, 'App Config', Icons.settings, Colors.grey, () {}),
        ],
      ),
    );
  }

  Widget _buildAdminCard(BuildContext context, String title, IconData icon, Color color, VoidCallback onTap) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: color),
            const SizedBox(height: 12),
            Text(title, style: Theme.of(context).textTheme.titleMedium),
          ],
        ),
      ),
    );
  }
}
