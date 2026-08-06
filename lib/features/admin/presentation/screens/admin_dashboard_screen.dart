import 'package:flutter/material.dart';

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
          _buildAdminCard(context, 'User Management', Icons.people, Colors.blue),
          _buildAdminCard(context, 'Content Manager', Icons.library_books, Colors.green),
          _buildAdminCard(context, 'System Reports', Icons.analytics, Colors.orange),
          _buildAdminCard(context, 'Notifications', Icons.notifications, Colors.red),
          _buildAdminCard(context, 'App Config', Icons.settings, Colors.grey),
          _buildAdminCard(context, 'Audit Logs', Icons.list_alt, Colors.brown),
        ],
      ),
    );
  }

  Widget _buildAdminCard(BuildContext context, String title, IconData icon, Color color) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: () {},
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
