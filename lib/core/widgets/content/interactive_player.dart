import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../../di/injection.dart';
import '../../telemetry/telemetry_service.dart';

class InteractivePlayer extends StatefulWidget {
  final String? contentId;
  final String pathOrUrl; // Can be a local file path or a remote URL
  final String? title;

  const InteractivePlayer({
    super.key,
    this.contentId,
    required this.pathOrUrl,
    this.title,
  });

  @override
  State<InteractivePlayer> createState() => _InteractivePlayerState();
}

class _InteractivePlayerState extends State<InteractivePlayer> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))
      ..addJavaScriptChannel(
        'GurukulBridge',
        onMessageReceived: (message) {
          _handleJavascriptMessage(message.message);
        },
      )
      ..setNavigationDelegate(
        NavigationDelegate(
          onProgress: (int progress) {
            debugPrint('Content Loading: $progress%');
          },
          onPageStarted: (String url) {},
          onPageFinished: (String url) {
            debugPrint('Content Loaded: $url');
          },
        ),
      );

    if (widget.pathOrUrl.startsWith('http')) {
      _controller.loadRequest(Uri.parse(widget.pathOrUrl));
    } else {
      _controller.loadRequest(Uri.file(widget.pathOrUrl));
    }
  }

  void _handleJavascriptMessage(String message) {
    if (widget.contentId != null) {
      sl<TelemetryService>().logEvent(
        eid: 'INTERACTIVE_PLAYER_MESSAGE',
        edata: {'contentId': widget.contentId, 'rawMessage': message},
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (widget.title != null) {
      return Scaffold(
        appBar: AppBar(title: Text(widget.title!)),
        body: WebViewWidget(controller: _controller),
      );
    }
    return WebViewWidget(controller: _controller);
  }
}
