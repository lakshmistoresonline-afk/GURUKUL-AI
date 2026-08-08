import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/di/injection.dart';
import '../../curriculum/domain/models/concept_node.dart';
import '../models/acquisition_file.dart';
import '../models/import_queue_item.dart';
import '../models/import_status.dart';
import '../repositories/content_acquisition_repository.dart';
import '../services/chapter_builder_service.dart';
import '../services/pdf_processor_service.dart';
import '../services/repository_scanner_service.dart';
import '../services/asset_processor_service.dart';
import '../services/ai_pipeline_service.dart';
import '../services/validation_engine.dart';
import '../services/manifest_service.dart';
import '../services/search_engine_service.dart';
import '../models/validation_report.dart';

/// Events for the AcquisitionBloc
abstract class AcquisitionEvent {}

class LoadQueue extends AcquisitionEvent {}

class StartScan extends AcquisitionEvent {}

class AddToQueue extends AcquisitionEvent {
  final AcquisitionFile file;
  AddToQueue(this.file);
}

class ProcessQueue extends AcquisitionEvent {}

class ProcessSingleItem extends AcquisitionEvent {
  final String id;
  ProcessSingleItem(this.id);
}

class RunValidation extends AcquisitionEvent {}

class UploadFile extends AcquisitionEvent {
  final int classLevel;
  final String subject;
  UploadFile({required this.classLevel, required this.subject});
}

/// State for the AcquisitionBloc
class AcquisitionState {
  final List<ImportQueueItem> queue;
  final List<AcquisitionFile> scannedFiles;
  final ValidationReport? lastValidationReport;
  final bool isScanning;
  final bool isProcessing;
  final bool isValidating;
  final String? error;
  final DateTime? processingStartTime;

  AcquisitionState({
    this.queue = const [],
    this.scannedFiles = const [],
    this.lastValidationReport,
    this.isScanning = false,
    this.isProcessing = false,
    this.isValidating = false,
    this.error,
    this.processingStartTime,
  });

  AcquisitionState copyWith({
    List<ImportQueueItem>? queue,
    List<AcquisitionFile>? scannedFiles,
    ValidationReport? lastValidationReport,
    bool? isScanning,
    bool? isProcessing,
    bool? isValidating,
    String? error,
    DateTime? processingStartTime,
  }) {
    return AcquisitionState(
      queue: queue ?? this.queue,
      scannedFiles: scannedFiles ?? this.scannedFiles,
      lastValidationReport: lastValidationReport ?? this.lastValidationReport,
      isScanning: isScanning ?? this.isScanning,
      isProcessing: isProcessing ?? this.isProcessing,
      isValidating: isValidating ?? this.isValidating,
      error: error,
      processingStartTime: processingStartTime ?? this.processingStartTime,
    );
  }
}

class AcquisitionBloc extends Bloc<AcquisitionEvent, AcquisitionState> {
  final ContentAcquisitionRepository _repository = sl<ContentAcquisitionRepository>();
  final RepositoryScannerService _scannerService = sl<RepositoryScannerService>();
  final PDFProcessorService _pdfProcessor = sl<PDFProcessorService>();
  final ChapterBuilderService _chapterBuilder = sl<ChapterBuilderService>();
  final AssetProcessorService _assetProcessor = sl<AssetProcessorService>();
  final AIPipelineService _aiPipeline = sl<AIPipelineService>();
  final ValidationEngine _validationEngine = sl<ValidationEngine>();
  final ManifestService _manifestService = sl<ManifestService>();
  final SearchEngineService _searchEngineService = sl<SearchEngineService>();

  StreamSubscription? _queueSubscription;

  AcquisitionBloc() : super(AcquisitionState()) {
    on<LoadQueue>(_onLoadQueue);
    on<StartScan>(_onStartScan);
    on<AddToQueue>(_onAddToQueue);
    on<ProcessQueue>(_onProcessQueue);
    on<ProcessSingleItem>(_onProcessSingleItem);
    on<RunValidation>(_onRunValidation);
    on<UploadFile>(_onUploadFile);

    _queueSubscription = _repository.watchQueue().listen((items) {
      add(LoadQueue());
    });

    add(LoadQueue());
  }

  Future<void> _onLoadQueue(LoadQueue event, Emitter<AcquisitionState> emit) async {
    final items = _repository.getAllItems();
    emit(state.copyWith(queue: items));
  }

  Future<void> _onStartScan(StartScan event, Emitter<AcquisitionState> emit) async {
    emit(state.copyWith(isScanning: true, error: null));
    try {
      final files = await _scannerService.scan();
      // Automatic Addition to Queue for new or changed files (Incremental Import)
      final existingItems = _repository.getAllItems();
      for (final file in files) {
        final existing = existingItems.where((i) => i.file.path == file.path).firstOrNull;
        if (existing == null || existing.file.checksum != file.checksum) {
          await _repository.addToQueue(file);
        }
      }
      emit(state.copyWith(scannedFiles: files, isScanning: false));
    } catch (e) {
      emit(state.copyWith(isScanning: false, error: 'Scan failed: $e'));
    }
  }

  Future<void> _onAddToQueue(AddToQueue event, Emitter<AcquisitionState> emit) async {
    try {
      await _repository.addToQueue(event.file);
    } catch (e) {
      emit(state.copyWith(error: 'Failed to add to queue: $e'));
    }
  }

  Future<void> _onProcessQueue(ProcessQueue event, Emitter<AcquisitionState> emit) async {
    if (state.isProcessing) return;
    emit(state.copyWith(isProcessing: true, error: null, processingStartTime: DateTime.now()));

    try {
      final pendingItems = _repository.getPendingItems();
      final List<ConceptNode> allProcessedNodes = [];

      for (final item in pendingItems) {
        if (item.status == ImportStatus.completed || item.status == ImportStatus.cancelled) continue;

        try {
          await _repository.updateStatus(item.id, ImportStatus.processing);

          // 1. Extraction
          await _repository.updateProgress(item.id, 0.2, stage: 'Extracting content...');
          final extraction = await _pdfProcessor.process(item);

          // 2. Asset Processing
          await _repository.updateProgress(item.id, 0.4, stage: 'Processing assets...');
          await _assetProcessor.processAssets(item.id, extraction);

          // 3. Chapter Building
          await _repository.updateProgress(item.id, 0.6, stage: 'Building chapters...');
          final chapters = await _chapterBuilder.buildChapters(item.file, extraction);

          // 4. AI Pipeline (with Incremental Logic)
          await _repository.updateProgress(item.id, 0.8, stage: 'Running AI enrichment...');
          for (var chapter in chapters) {
            final enriched = await _aiPipeline.process(
              chapter,
              checksum: item.file.checksum
            );
            allProcessedNodes.add(enriched);
          }

          await _repository.updateProgress(item.id, 1.0, stage: 'Complete');
          await _repository.updateStatus(item.id, ImportStatus.completed);
        } catch (e) {
          await _repository.updateStatus(item.id, ImportStatus.failed);
          debugPrint('AcquisitionBloc: Failed item ${item.id} - $e');
        }
      }

      // Finalize Manifest and Search Index
      if (allProcessedNodes.isNotEmpty) {
        await _manifestService.generateManifest(state.scannedFiles);
        await _searchEngineService.buildIndex(allProcessedNodes);
      }
    } catch (e) {
      emit(state.copyWith(error: 'Batch processing failed: $e'));
    } finally {
      emit(state.copyWith(isProcessing: false));
    }
  }

  Future<void> _onProcessSingleItem(ProcessSingleItem event, Emitter<AcquisitionState> emit) async {
    final item = _repository.getAllItems().where((i) => i.id == event.id).firstOrNull;
    if (item == null || item.status == ImportStatus.completed) return;

    try {
      await _repository.updateStatus(item.id, ImportStatus.processing);

      // 1. Extraction
      await _repository.updateProgress(item.id, 0.2, stage: 'Extracting content...');
      final extraction = await _pdfProcessor.process(item);

      // 2. Asset Processing
      await _repository.updateProgress(item.id, 0.4, stage: 'Processing assets...');
      await _assetProcessor.processAssets(item.id, extraction);

      // 3. Chapter Building
      await _repository.updateProgress(item.id, 0.6, stage: 'Building chapters...');
      final chapters = await _chapterBuilder.buildChapters(item.file, extraction);

      // 4. AI Pipeline (with Incremental Logic)
      await _repository.updateProgress(item.id, 0.8, stage: 'Running AI enrichment...');
      final List<ConceptNode> processedNodes = [];
      for (var chapter in chapters) {
        final enriched = await _aiPipeline.process(
          chapter,
          checksum: item.file.checksum
        );
        processedNodes.add(enriched);
      }

      // 5. Indexing
      if (processedNodes.isNotEmpty) {
        await _searchEngineService.buildIndex(processedNodes);
      }

      await _repository.updateProgress(item.id, 1.0, stage: 'Complete');
      await _repository.updateStatus(item.id, ImportStatus.completed);

      // Update manifest
      await _manifestService.generateManifest(state.scannedFiles);

    } catch (e) {
      await _repository.updateStatus(item.id, ImportStatus.failed, error: e.toString());
      debugPrint('AcquisitionBloc: Failed item ${item.id} - $e');
    }
  }

  Future<void> _onUploadFile(UploadFile event, Emitter<AcquisitionState> emit) async {
    // This requires file_picker dependency which is already in pubspec
    // Logic:
    // 1. Pick file
    // 2. Copy to datasets/ncert_source/class_XX/subject/
    // 3. Create AcquisitionFile object
    // 4. Add to queue
    // 5. Trigger scan to refresh UI

    // Note: Since this is Bloc, we typically wouldn't put UI logic here,
    // but we can handle the file system operations.
  }

  Future<void> _onRunValidation(RunValidation event, Emitter<AcquisitionState> emit) async {
    emit(state.copyWith(isValidating: true));
    try {
      final report = await _validationEngine.validateRepository();
      emit(state.copyWith(lastValidationReport: report, isValidating: false));
    } catch (e) {
      emit(state.copyWith(isValidating: false, error: 'Validation failed: $e'));
    }
  }

  @override
  Future<void> close() {
    _queueSubscription?.cancel();
    return super.close();
  }
}
