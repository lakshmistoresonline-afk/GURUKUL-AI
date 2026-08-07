import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../data/ai_tutor_service.dart';
import '../../domain/services/voice_service.dart';
import '../../../curriculum/domain/models/concept_node.dart';
import '../../../curriculum/domain/models/mastery.dart';

class AiTutorChatScreen extends StatefulWidget {
  final ConceptNode? concept;
  final Mastery? mastery;
  final String? initialQuery;

  const AiTutorChatScreen({
    super.key,
    this.concept,
    this.mastery,
    this.initialQuery,
  });

  @override
  State<AiTutorChatScreen> createState() => _AiTutorChatScreenState();
}

class _AiTutorChatScreenState extends State<AiTutorChatScreen> with SingleTickerProviderStateMixin {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Map<String, String>> _messages = [];
  bool _isLoading = false;
  bool _isListening = false;
  bool _voiceEnabled = false;

  late AnimationController _assistantAnimationController;

  final List<String> _suggestedQuestions = [
    "Explain this simply",
    "Give me an example",
    "Quick quiz!",
    "Why is this important?",
  ];

  @override
  void initState() {
    super.initState();
    _assistantAnimationController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    final greeting = widget.concept != null
        ? 'Hi! I am your Gurukul AI tutor. I see we are learning about "${widget.concept!.topic}". How can I help you today?'
        : 'Hi! I am your Gurukul AI tutor. I can help you with your Class ${widget.concept?.classLevel ?? 5} & 6 subjects. Ask me anything!';

    _messages.add({
      'role': 'assistant',
      'content': greeting,
    });
    _initVoice();

    if (widget.initialQuery != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _controller.text = widget.initialQuery!;
        _sendMessage();
      });
    }
  }

  @override
  void dispose() {
    _assistantAnimationController.dispose();
    _scrollController.dispose();
    _controller.dispose();
    sl<VoiceService>().stopSpeaking();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
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

  Future<void> _sendMessage([String? text]) async {
    final query = text ?? _controller.text.trim();
    if (query.isEmpty) return;

    if (_isListening) {
      await _toggleListening();
    }

    setState(() {
      _messages.add({'role': 'user', 'content': query});
      _isLoading = true;
      _controller.clear();
    });
    _scrollToBottom();

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
      _scrollToBottom();

      if (_voiceEnabled) {
        sl<VoiceService>().speak(response);
      }
    } catch (e) {
      setState(() {
        _messages.add({
          'role': 'assistant',
          'content': 'Sorry, I encountered an error. Please try again.'
        });
        _isLoading = false;
      });
      _scrollToBottom();
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Row(
          children: [
            ScaleTransition(
              scale: Tween(begin: 1.0, end: 1.1).animate(_assistantAnimationController),
              child: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: colorScheme.primary.withValues(alpha: 0.1),
                  shape: BoxShape.circle,
                ),
                child: Icon(Icons.smart_toy, color: colorScheme.primary, size: 20),
              ),
            ),
            const SizedBox(width: 12),
            const Text('Gurukul AI Tutor'),
          ],
        ),
        actions: [
          IconButton(
            icon: Icon(_voiceEnabled ? Icons.volume_up : Icons.volume_off),
            onPressed: () => setState(() => _voiceEnabled = !_voiceEnabled),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isUser = message['role'] == 'user';
                return _ChatBubble(message: message['content']!, isUser: isUser);
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 8),
              child: _TypingIndicator(),
            ),
          _buildInputArea(),
        ],
      ),
    );
  }

  Widget _buildInputArea() {
    final colorScheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            offset: const Offset(0, -4),
            blurRadius: 10,
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (_messages.length == 1) // Only show suggestions at start or when empty
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: _suggestedQuestions.map((q) => Padding(
                  padding: const EdgeInsets.only(right: 8, bottom: 12),
                  child: ActionChip(
                    label: Text(q),
                    onPressed: () => _sendMessage(q),
                    backgroundColor: colorScheme.primary.withValues(alpha: 0.05),
                    side: BorderSide(color: colorScheme.primary.withValues(alpha: 0.1)),
                  ),
                )).toList(),
              ),
            ),
          Row(
            children: [
              IconButton(
                onPressed: _toggleListening,
                icon: Icon(_isListening ? Icons.mic : Icons.mic_none),
                style: IconButton.styleFrom(
                  backgroundColor: _isListening ? Colors.red.shade50 : colorScheme.primary.withValues(alpha: 0.05),
                  foregroundColor: _isListening ? Colors.red : colorScheme.primary,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: TextField(
                  controller: _controller,
                  decoration: InputDecoration(
                    hintText: 'Ask me anything...',
                    filled: true,
                    fillColor: Colors.grey.shade100,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(24),
                      borderSide: BorderSide.none,
                    ),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  ),
                  onSubmitted: (_) => _sendMessage(),
                ),
              ),
              const SizedBox(width: 8),
              IconButton(
                onPressed: () => _sendMessage(),
                icon: const Icon(Icons.send),
                style: IconButton.styleFrom(
                  backgroundColor: colorScheme.primary,
                  foregroundColor: Colors.white,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ChatBubble extends StatelessWidget {
  final String message;
  final bool isUser;

  const _ChatBubble({required this.message, required this.isUser});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
        decoration: BoxDecoration(
          color: isUser ? colorScheme.primary : Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(20),
            topRight: const Radius.circular(20),
            bottomLeft: Radius.circular(isUser ? 20 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 20),
          ),
          boxShadow: [
            if (!isUser)
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.05),
                offset: const Offset(0, 2),
                blurRadius: 5,
              ),
          ],
        ),
        child: Text(
          message,
          style: TextStyle(
            color: isUser ? Colors.white : Colors.black87,
            fontSize: 15,
            height: 1.4,
          ),
        ),
      ),
    );
  }
}

class _TypingIndicator extends StatelessWidget {
  const _TypingIndicator();

  @override
  Widget build(BuildContext context) {
    return const Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          width: 20,
          height: 20,
          child: CircularProgressIndicator(strokeWidth: 2),
        ),
        SizedBox(width: 12),
        Text('Gurukul AI is thinking...', style: TextStyle(fontSize: 12, color: Colors.grey)),
      ],
    );
  }
}
