import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class InteractiveContentPlayer extends StatefulWidget {
  final String htmlUrl;
  final String title;

  const InteractiveContentPlayer({super.key, required this.htmlUrl, required this.title});

  @override
  State<InteractiveContentPlayer> createState() => _InteractiveContentPlayerState();
}

class _InteractiveContentPlayerState extends State<InteractiveContentPlayer> {
  late WebViewController _controller;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))
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
      )
      ..loadRequest(Uri.parse(widget.htmlUrl));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: WebViewWidget(controller: _controller),
    );
  }
}
