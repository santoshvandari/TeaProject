import 'package:flutter/material.dart';
import 'package:flutter_html_2/flutter_html_2.dart';

class ResultScreen extends StatelessWidget {
  final List<dynamic> result; // Accept List of predictions directly

  const ResultScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic>? diseaseInfo =
        result.isNotEmpty ? result[0] : null;

    debugPrint("Disease Info: $diseaseInfo");

    final String? imagePath = diseaseInfo?['predicted_image'];

    return Scaffold(
      appBar: AppBar(
        title: const Text("Analysis Result"),
        backgroundColor: Colors.teal,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: diseaseInfo != null
            ? Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Card for Disease Information
                  Card(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16.0),
                    ),
                    elevation: 4.0,
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Display the disease name
                          Text(
                            diseaseInfo['class'] ?? "Unknown Disease",
                            style: const TextStyle(
                              fontSize: 26.0,
                              fontWeight: FontWeight.bold,
                              color: Colors.teal,
                            ),
                          ),
                          const SizedBox(height: 8.0),

                          // Display the predicted image with rounded corners
                          if (imagePath != null)
                            ClipRRect(
                              borderRadius: BorderRadius.circular(16.0),
                              child: imagePath.startsWith('http')
                                  ? Image.network(
                                      imagePath,
                                      width: double.infinity,
                                      height: 400.0,
                                      fit: BoxFit.contain,
                                    )
                                  : const Text("No Image Found"),
                            ),
                          const SizedBox(height: 16.0),

                          // Display the confidence score
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              const Text(
                                "Confidence:",
                                style: TextStyle(
                                  fontSize: 18.0,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                              Text(
                                "${((diseaseInfo['confidence'] ?? 0.0) * 100).toStringAsFixed(2)}%",
                                style: const TextStyle(
                                  fontSize: 18.0,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.teal,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16.0),

                  // Card for Disease Summary
                  Card(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16.0),
                    ),
                    elevation: 4.0,
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            "Disease Summary",
                            style: TextStyle(
                              fontSize: 22.0,
                              fontWeight: FontWeight.bold,
                              color: Colors.teal,
                            ),
                          ),
                          const SizedBox(height: 8.0),
                          Html(
                            data: diseaseInfo['summary'] ??
                                "<p>No summary available</p>",
                            style: {
                              "p": Style(
                                fontSize: FontSize(16.0),
                                lineHeight: LineHeight.number(1.5),
                              ),
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              )
            : const Center(
                child: Text(
                  "No data available",
                  style: TextStyle(
                    fontSize: 18.0,
                    color: Colors.grey,
                  ),
                ),
              ),
      ),
    );
  }
}
