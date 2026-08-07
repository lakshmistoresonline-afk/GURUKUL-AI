import 'package:flutter/material.dart';
import '../widgets/fractions_simulation.dart';

class VirtualLabScreen extends StatelessWidget {
  const VirtualLabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gurukul Virtual Lab')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text('Interactive Simulations', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          _buildLabCard(
            context,
            'Fractions Explorer',
            'Visualize parts of a whole with a circle model.',
            Icons.pie_chart,
            Colors.blue,
            const FractionsSimulation(),
          ),
          _buildLabCard(
            context,
            'Solar System',
            'Watch the planets rotate around the Sun.',
            Icons.wb_sunny,
            Colors.orange,
            const Center(child: Text('Solar System Simulation Coming Soon')),
          ),
          _buildLabCard(
            context,
            'Electric Circuit',
            'Connect bulbs and batteries to see how current flows.',
            Icons.electrical_services,
            Colors.yellow.shade800,
            const Center(child: Text('Electric Circuit Simulation Coming Soon')),
          ),
        ],
      ),
    );
  }

  Widget _buildLabCard(BuildContext context, String title, String desc, IconData icon, Color color, Widget simulation) {
    return Card(
      margin: const EdgeInsets.only(bottom: 20),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.1), child: Icon(icon, color: color)),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(desc),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => Scaffold(
                appBar: AppBar(title: Text(title)),
                body: Padding(padding: const EdgeInsets.all(20), child: simulation),
              ),
            ),
          );
        },
      ),
    );
  }
}
