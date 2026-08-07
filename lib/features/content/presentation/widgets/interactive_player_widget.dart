import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../../../../core/di/injection.dart';
import '../../../../core/telemetry/telemetry_service.dart';

class InteractivePlayerWidget extends StatefulWidget {
  final String contentId;
  final String indexPath; // Full path to the index.html or starting file

  const InteractivePlayerWidget({
    super.key,
    required this.contentId,
    required this.indexPath,
  });

  @override
  State<InteractivePlayerWidget> createState() => _InteractivePlayerWidgetState();
}

class _InteractivePlayerWidgetState extends State<InteractivePlayerWidget> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..addJavaScriptChannel(
        'GurukulBridge',
        onMessageReceived: (message) {
          _handleJavascriptMessage(message.message);
        },
      )
      ..loadRequest(Uri.file(widget.indexPath));
  }

  void _handleJavascriptMessage(String message) {
    // Expected message format: {"eid": "INTERACT", "edata": {...}}
    // This allows H5P/ECML content to send telemetry back to Flutter
    sl<TelemetryService>().logEvent(
      eid: 'INTERACTIVE_PLAYER_MESSAGE',
      edata: {'contentId': widget.contentId, 'rawMessage': message},
    );
  }

  @override
  Widget build(BuildContext context) {
    return WebViewWidget(controller: _controller);
  }
}
