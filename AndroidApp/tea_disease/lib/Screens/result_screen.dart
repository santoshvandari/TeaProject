import 'package:flutter/material.dart';
import 'package:flutter_html_2/flutter_html_2.dart';

class ResultScreen extends StatelessWidget {
  final List<dynamic> result; // Accept List of predictions directly

  const ResultScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    // You don't need to jsonDecode here anymore since the data is already parsed
    final Map<String, dynamic>? diseaseInfo =
        result.isNotEmpty ? result[0] : null;

    debugPrint("Disease Info: $diseaseInfo");

    return Scaffold(
      appBar: AppBar(title: const Text("Analysis Result")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: diseaseInfo != null
            ? Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    diseaseInfo['class'] ?? "Unknown Disease",
                    style: const TextStyle(
                      fontSize: 24.0,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8.0),
                  Html(
                    data:
                        diseaseInfo['summary'] ?? "<p>No summary available</p>",
                  ),
                  const SizedBox(height: 16.0),
                  Text(
                    "Confidence: ${(diseaseInfo['confidence'] ?? 0.0) * 100}%",
                    style: const TextStyle(
                      fontSize: 20.0,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              )
            : const Center(
                child: Text("No data available"),
              ),
      ),
    );
  }
}
