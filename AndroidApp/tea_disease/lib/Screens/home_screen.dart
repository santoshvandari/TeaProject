import 'package:flutter/material.dart';
import 'package:tea_disease/Screens/camera_screen.dart';
import 'package:tea_disease/Screens/result_screen.dart';
import 'package:tea_disease/Services/api.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _isLoading = false;

  // Method to handle photo capture and API response
  void _onPhotoCaptured(String imagePath) async {
    setState(() {
      _isLoading = true;
    });

    try {
      final response = await ApiService.uploadImage(imagePath);
      if (response['predictions'] != null) {
        // Handle the predictions and pass the data to ResultScreen
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ResultScreen(
              result: response['predictions'], // Pass the prediction data
            ),
          ),
        );
      } else {
        // Show an error message if the response does not contain predictions
        _showErrorSnackbar("No predictions received.");
      }
    } catch (error) {
      // Handle unexpected errors (e.g., network issues)
      _showErrorSnackbar("An unexpected error occurred: $error");
    } finally {
      // Hide the loading indicator after processing is done
      setState(() {
        _isLoading = false;
      });
    }
  }

  // Method to show a snackbar with an error message
  void _showErrorSnackbar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF4CAF50), Color(0xFF81C784)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Center(
          child: _isLoading
              ? const CircularProgressIndicator(
                  color: Colors.white,
                )
              : Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // App heading
                    const Text(
                      "Tea Leaf Analysis",
                      style: TextStyle(
                        fontSize: 32.0,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 16.0),

                    // Capture button
                    ElevatedButton(
                      onPressed: () {
                        // Navigate to the CameraScreen for capturing an image
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => CameraScreen(
                              onPhotoCaptured: _onPhotoCaptured,
                            ),
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(
                          horizontal: 40.0,
                          vertical: 12.0,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(20.0),
                        ),
                      ),
                      child: const Text(
                        "Capture Tea Leaf",
                        style: TextStyle(
                          color: Color(0xFF4CAF50),
                          fontSize: 18.0,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
        ),
      ),
    );
  }
}
