import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:flutter_html_2/flutter_html_2.dart'; // Import to handle HTML content

class ResultScreen extends StatelessWidget {
  final String result;

  const ResultScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    // Decode the JSON response
    final List<dynamic> responseData = result.isNotEmpty
        ? jsonDecode(result) // Decode JSON string
        : [];

    // If the response contains predictions, extract the first prediction (if available)
    final Map<String, dynamic>? diseaseInfo = responseData.isNotEmpty
        ? responseData[0] as Map<String, dynamic>?
        : null;

    debugPrint("Disease Info: $diseaseInfo");

    return Scaffold(
      appBar: AppBar(title: const Text("Analysis Result")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: diseaseInfo != null
            ? Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Display Disease Class (Name)
                  Text(
                    diseaseInfo['class'] ??
                        "Unknown Disease", // Disease class (e.g., name of disease)
                    style: const TextStyle(
                      fontSize: 24.0,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8.0),

                  // Display Disease Summary
                  Html(
                    data: diseaseInfo['summary'] ??
                        "<p>No summary available</p>", // Disease summary (HTML formatted)
                  ),
                  const SizedBox(height: 16.0),

                  // Display Confidence Score
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
                child: Text(
                    "No data available"), // Display when no disease info is available
              ),
      ),
    );
  }
}
