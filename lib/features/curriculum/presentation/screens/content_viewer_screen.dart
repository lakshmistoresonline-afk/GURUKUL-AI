import 'package:flutter/material.dart';
import 'package:flutter_pdfview/flutter_pdfview.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../../../../core/widgets/content/interactive_player.dart';
import '../../../../core/di/injection.dart';
import '../../../../core/telemetry/telemetry_service.dart';

enum ContentType { pdf, html, video }

class ContentViewerScreen extends StatefulWidget {
  final String contentId;
  final String title;
  final String url;
  final ContentType type;

  const ContentViewerScreen({
    super.key,
    required this.contentId,
    required this.title,
    required this.url,
    required this.type,
  });

  @override
  State<ContentViewerScreen> createState() => _ContentViewerScreenState();
}

class _ContentViewerScreenState extends State<ContentViewerScreen> {
  late WebViewController _webController;
  final DateTime _startTime = DateTime.now();

  @override
  void initState() {
    super.initState();
    sl<TelemetryService>().logStart(type: widget.type.name, id: widget.contentId);

    if (widget.type == ContentType.html) {
      _webController = WebViewController()
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..loadRequest(Uri.parse(widget.url));
    }
  }

  @override
  void dispose() {
    final duration = DateTime.now().difference(_startTime);
    sl<TelemetryService>().logEnd(
      type: widget.type.name,
      id: widget.contentId,
      summary: {'duration': duration.inSeconds},
    );
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: _buildContent(),
    );
  }

  Widget _buildContent() {
    switch (widget.type) {
      case ContentType.pdf:
        return PDFView(
          filePath: widget.url, // In real app, download to local path first
          enableSwipe: true,
          swipeHorizontal: true,
          autoSpacing: false,
          pageFling: false,
          onRender: (pages) => debugPrint('PDF Rendered with $pages pages'),
          onError: (error) => debugPrint('PDF Error: $error'),
          onPageError: (page, error) => debugPrint('PDF Page Error on $page: $error'),
        );
      case ContentType.html:
        return InteractivePlayer(
          contentId: widget.contentId,
          pathOrUrl: widget.url,
        );
      default:
        return const Center(child: Text('Unsupported content type'));
    }
  }
}
