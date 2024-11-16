import 'package:flutter/material.dart';
import 'dart:convert';

import 'package:flutter_html_2/flutter_html_2.dart'; // Import to handle JSON decoding

class ResultScreen extends StatelessWidget {
  final String result;

  const ResultScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    // Decode the JSON response
    final List<dynamic> responseData = result.isNotEmpty
        ? jsonDecode(result) // Decode JSON string
        : [];
    final Map<String, dynamic>? diseaseInfo = responseData.isNotEmpty
        ? responseData[0] as Map<String, dynamic>?
        : null;

    return Scaffold(
      appBar: AppBar(title: const Text("Analysis Result")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: diseaseInfo != null
            ? Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Html(
                    data:
                        diseaseInfo['summary'] ?? "<p>No summary available</p>",
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
