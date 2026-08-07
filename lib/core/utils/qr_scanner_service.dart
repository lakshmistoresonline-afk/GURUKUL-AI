import 'package:google_mlkit_barcode_scanning/google_mlkit_barcode_scanning.dart';
import 'package:image_picker/image_picker.dart';

class QrScannerService {
  final BarcodeScanner _barcodeScanner = BarcodeScanner();

  Future<String?> scanFromImage() async {
    final picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.camera);

    if (image == null) return null;

    final inputImage = InputImage.fromFilePath(image.path);
    final List<Barcode> barcodes = await _barcodeScanner.processImage(inputImage);

    for (Barcode barcode in barcodes) {
      if (barcode.displayValue != null) {
        return barcode.displayValue;
      }
    }
    return null;
  }

  void dispose() {
    _barcodeScanner.close();
  }
}
