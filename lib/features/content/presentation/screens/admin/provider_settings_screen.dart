import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/features/content/domain/providers/content_provider_manager.dart';
import 'package:project_gurukul_ai/features/content/domain/providers/content_provider.dart';

class ProviderSettingsScreen extends StatefulWidget {
  const ProviderSettingsScreen({super.key});

  @override
  State<ProviderSettingsScreen> createState() => _ProviderSettingsScreenState();
}

class _ProviderSettingsScreenState extends State<ProviderSettingsScreen> {
  @override
  Widget build(BuildContext context) {
    final manager = sl<ContentProviderManager>();
    final providers = manager.allProviders;

    return Scaffold(
      appBar: AppBar(title: const Text('Content Provider Settings')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: providers.length,
        itemBuilder: (context, index) {
          final p = providers[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SwitchListTile(
                    title: Text(p.name, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text('License: ${p.licenseInfo}'),
                    value: manager.isProviderEnabled(p.id),
                    onChanged: (v) => setState(() => manager.setProviderEnabled(p.id, v)),
                  ),
                  _buildStatusRow(p),
                ],
              ),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        label: const Text('Refresh Metadata'),
        icon: const Icon(Icons.refresh),
      ),
    );
  }

  Widget _buildStatusRow(ContentProvider p) {
    return FutureBuilder<ProviderStatus>(
      future: p.checkHealth(),
      builder: (context, snapshot) {
        final status = snapshot.data ?? ProviderStatus.inactive;
        Color color = Colors.grey;
        String text = 'Checking...';

        switch (status) {
          case ProviderStatus.active:
            color = Colors.green;
            text = 'Online';
            break;
          case ProviderStatus.inactive:
            color = Colors.red;
            text = 'Offline';
            break;
          case ProviderStatus.authenticationRequired:
            color = Colors.orange;
            text = 'Auth Required';
            break;
          case ProviderStatus.healthCheckFailed:
            color = Colors.deepOrange;
            text = 'Health Check Failed';
            break;
        }

        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Row(
            children: [
              Container(width: 12, height: 12, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
              const SizedBox(width: 8),
              Text(text, style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.bold)),
              const Spacer(),
              if (p.isOfflineSupported)
                const Chip(label: Text('Offline Ready', style: TextStyle(fontSize: 10)), visualDensity: VisualDensity.compact),
            ],
          ),
        );
      },
    );
  }
}
