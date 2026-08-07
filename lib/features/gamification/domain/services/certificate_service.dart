import 'dart:io';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'package:path_provider/path_provider.dart';

class CertificateService {
  Future<void> generateAndPreview({
    required String studentName,
    required String courseName,
    required DateTime completionDate,
  }) async {
    final pdf = pw.Document();

    pdf.addPage(
      pw.Page(
        pageFormat: PdfPageFormat.a4.landscape,
        build: (pw.Context context) {
          return pw.Center(
            child: pw.Container(
              padding: const pw.EdgeInsets.all(40),
              decoration: pw.BoxDecoration(
                border: pw.Border.all(color: PdfColors.blue, width: 5),
              ),
              child: pw.Column(
                mainAxisAlignment: pw.MainAxisAlignment.center,
                children: [
                  pw.Text('CERTIFICATE OF COMPLETION', style: pw.TextStyle(fontSize: 40, fontWeight: pw.FontWeight.bold, color: PdfColors.blue900)),
                  pw.SizedBox(height: 20),
                  pw.Text('This is to certify that', style: const pw.TextStyle(fontSize: 20)),
                  pw.SizedBox(height: 10),
                  pw.Text(studentName, style: pw.TextStyle(fontSize: 30, fontWeight: pw.FontWeight.bold)),
                  pw.SizedBox(height: 10),
                  pw.Text('has successfully completed the course', style: const pw.TextStyle(fontSize: 20)),
                  pw.SizedBox(height: 10),
                  pw.Text(courseName, style: pw.TextStyle(fontSize: 26, fontWeight: pw.FontWeight.bold, color: PdfColors.blue800)),
                  pw.SizedBox(height: 40),
                  pw.Row(
                    mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                    children: [
                      pw.Column(
                        children: [
                          pw.Text(completionDate.toString().split(' ')[0]),
                          pw.Divider(thickness: 1),
                          pw.Text('Date'),
                        ],
                      ),
                      pw.Column(
                        children: [
                          pw.Text('Gurukul AI', style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                          pw.Divider(thickness: 1),
                          pw.Text('Authorized Signature'),
                        ],
                      ),
                    ],
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );

    await Printing.layoutPdf(onLayout: (PdfPageFormat format) async => pdf.save());
  }
}
