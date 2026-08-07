import 'dart:io';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:chewie/chewie.dart';
import 'package:flutter_pdfview/flutter_pdfview.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../../../../core/widgets/content/interactive_player.dart';

enum ContentType { pdf, video, html, h5p }

class ContentPlayerScreen extends StatefulWidget {
  final String contentId;
  final String title;
  final String url;
  final ContentType type;
  final bool isOffline;

  const ContentPlayerScreen({
    super.key,
    required this.contentId,
    required this.title,
    required this.url,
    required this.type,
    this.isOffline = false,
  });

  @override
  State<ContentPlayerScreen> createState() => _ContentPlayerScreenState();
}

class _ContentPlayerScreenState extends State<ContentPlayerScreen> {
  VideoPlayerController? _videoController;
  ChewieController? _chewieController;
  WebViewController? _webController;

  @override
  void initState() {
    super.initState();
    if (widget.type == ContentType.video) {
      _initVideo();
    } else if (widget.type == ContentType.html || widget.type == ContentType.h5p) {
      _initWebView();
    }
  }

  void _initVideo() {
    _videoController = widget.isOffline
        ? VideoPlayerController.file(File(widget.url))
        : VideoPlayerController.networkUrl(Uri.parse(widget.url));

    _chewieController = ChewieController(
      videoPlayerController: _videoController!,
      autoPlay: true,
      looping: false,
    );
  }

  void _initWebView() {
    _webController = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse(widget.url));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: _buildPlayer(),
    );
  }

  Widget _buildPlayer() {
    switch (widget.type) {
      case ContentType.video:
        return _chewieController != null
            ? Chewie(controller: _chewieController!)
            : const Center(child: CircularProgressIndicator());
      case ContentType.pdf:
        return PDFView(
          filePath: widget.isOffline ? widget.url : null,
          // Note: In a real app, network PDF would be downloaded first or use a different plugin
        );
      case ContentType.html:
      case ContentType.h5p:
        if (widget.isOffline) {
          return InteractivePlayer(
            contentId: widget.contentId,
            pathOrUrl: widget.url,
          );
        }
        return WebViewWidget(controller: _webController!);
      default:
        return const Center(child: Text('Unsupported Content Type'));
    }
  }

  @override
  void dispose() {
    _videoController?.dispose();
    _chewieController?.dispose();
    super.dispose();
  }
}
