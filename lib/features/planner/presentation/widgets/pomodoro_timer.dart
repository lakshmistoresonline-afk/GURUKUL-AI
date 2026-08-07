import 'dart:async';
import 'package:flutter/material.dart';

class PomodoroTimer extends StatefulWidget {
  const PomodoroTimer({super.key});

  @override
  State<PomodoroTimer> createState() => _PomodoroTimerState();
}

class _PomodoroTimerState extends State<PomodoroTimer> {
  static const int _workTime = 25 * 60;
  static const int _breakTime = 5 * 60;

  int _secondsRemaining = _workTime;
  bool _isActive = false;
  bool _isWorkMode = true;
  Timer? _timer;

  void _toggleTimer() {
    if (_isActive) {
      _timer?.cancel();
    } else {
      _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
        setState(() {
          if (_secondsRemaining > 0) {
            _secondsRemaining--;
          } else {
            _timer?.cancel();
            _isActive = false;
            _secondsRemaining = _isWorkMode ? _breakTime : _workTime;
            _isWorkMode = !_isWorkMode;
            // Notify user
          }
        });
      });
    }
    setState(() => _isActive = !_isActive);
  }

  void _resetTimer() {
    _timer?.cancel();
    setState(() {
      _isActive = false;
      _isWorkMode = true;
      _secondsRemaining = _workTime;
    });
  }

  String _formatTime(int seconds) {
    final int minutes = seconds ~/ 60;
    final int remainingSeconds = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${remainingSeconds.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Text(_isWorkMode ? 'Focus Session' : 'Short Break', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            Text(
              _formatTime(_secondsRemaining),
              style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold, letterSpacing: 2),
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton.filledTonal(
                  onPressed: _resetTimer,
                  icon: const Icon(Icons.refresh),
                ),
                const SizedBox(width: 16),
                FloatingActionButton(
                  onPressed: _toggleTimer,
                  child: Icon(_isActive ? Icons.pause : Icons.play_arrow),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}
