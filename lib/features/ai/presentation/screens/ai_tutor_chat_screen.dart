import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../data/ai_tutor_service.dart';
import '../../domain/services/voice_service.dart';
import '../../../curriculum/domain/models/concept_node.dart';
import '../../../curriculum/domain/models/mastery.dart';

class AiTutorChatScreen extends StatefulWidget {
  final ConceptNode concept;
  final Mastery mastery;
  final String? initialQuery;

  const AiTutorChatScreen({
    super.key,
    required this.concept,
    required this.mastery,
    this.initialQuery,
  });

  @override
  State<AiTutorChatScreen> createState() => _AiTutorChatScreenState();
}

class _AiTutorChatScreenState extends State<AiTutorChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  bool _isLoading = false;
  bool _isListening = false;
  bool _voiceEnabled = false;

  @override
  void initState() {
    super.initState();
    _messages.add({
      'role': 'assistant',
      'content': 'Hi! I am your Gurukul AI tutor. I see we are learning about "${widget.concept.topic}". How can I help you today?',
    });
    _initVoice();

    if (widget.initialQuery != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _controller.text = widget.initialQuery!;
        _sendMessage();
      });
    }
  }

  Future<void> _initVoice() async {
    await sl<VoiceService>().init();
  }

  Future<void> _toggleListening() async {
    final voiceService = sl<VoiceService>();
    if (_isListening) {
      await voiceService.stopListening();
      setState(() => _isListening = false);
    } else {
      setState(() => _isListening = true);
      await voiceService.startListening((text) {
        setState(() {
          _controller.text = text;
        });
      });
    }
  }

  Future<void> _sendMessage() async {
    final query = _controller.text.trim();
    if (query.isEmpty) return;

    if (_isListening) {
      await _toggleListening();
    }

    setState(() {
      _messages.add({'role': 'user', 'content': query});
      _isLoading = true;
      _controller.clear();
    });

    try {
      final response = await sl<AiTutorService>().getHelp(
        userQuery: query,
        concept: widget.concept,
        mastery: widget.mastery,
      );

      setState(() {
        _messages.add({'role': 'assistant', 'content': response});
        _isLoading = false;
      });

      if (_voiceEnabled) {
        sl<VoiceService>().speak(response);
      }
    } catch (e) {
      setState(() {
        _messages.add({'role': 'assistant', 'content': 'Sorry, I encountered an error. Please try again.'});
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gurukul AI Tutor'),
        actions: [
          IconButton(
            icon: Icon(_voiceEnabled ? Icons.volume_up : Icons.volume_off),
            onPressed: () => setState(() => _voiceEnabled = !_voiceEnabled),
          )
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isUser = message['role'] == 'user';
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? Theme.of(context).primaryColor : Colors.grey[200],
                      borderRadius: BorderRadius.circular(12).copyWith(
                        bottomRight: isUser ? Radius.zero : null,
                        bottomLeft: !isUser ? Radius.zero : null,
                      ),
                    ),
                    child: Text(
                      message['content']!,
                      style: TextStyle(color: isUser ? Colors.white : Colors.black87),
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isLoading) const Padding(
            padding: EdgeInsets.all(8.0),
            child: CircularProgressIndicator(),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                IconButton(
                  onPressed: _toggleListening,
                  icon: Icon(_isListening ? Icons.mic : Icons.mic_none),
                  color: _isListening ? Colors.red : Theme.of(context).primaryColor,
                ),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Ask me anything...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                IconButton(
                  onPressed: _sendMessage,
                  icon: const Icon(Icons.send),
                  color: Theme.of(context).primaryColor,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    sl<VoiceService>().stopSpeaking();
    super.dispose();
  }
}
