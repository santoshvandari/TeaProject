import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class CameraScreen extends StatefulWidget {
  final Function(String) onPhotoCaptured;
  const CameraScreen({required this.onPhotoCaptured, super.key});

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  // Initialize the camera asynchronously
  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    // Ensure that cameras are available before using them
    if (cameras.isEmpty) {
      print('No cameras available'); // Handle no cameras available
      return;
    }
    _controller = CameraController(cameras[0], ResolutionPreset.high);

    // Initialize the controller
    _initializeControllerFuture = _controller.initialize();

    // Set the state after initialization is complete
    setState(() {});
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _takePicture() async {
    try {
      await _initializeControllerFuture; // Ensure controller is initialized
      final image = await _controller.takePicture();
      widget.onPhotoCaptured(image.path); // Pass the image path to the callback
      Navigator.pop(context); // Go back to previous screen
    } catch (e) {
      print(e); // Print any errors
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Camera preview
          FutureBuilder(
            future: _initializeControllerFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                return CameraPreview(_controller);
              } else {
                return const Center(
                  child: CircularProgressIndicator(
                    color: Colors.white,
                  ),
                );
              }
            },
          ),

          // Translucent overlay with app bar
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: const EdgeInsets.symmetric(vertical: 16.0),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.5),
              ),
              child: const Center(
                child: Text(
                  "Capture Tea Leaf",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20.0,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),

          // Capture button at the bottom center
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.only(bottom: 30.0),
              child: FloatingActionButton(
                onPressed: _takePicture,
                backgroundColor: Colors.green,
                child: const Icon(
                  Icons.camera_alt,
                  color: Colors.white,
                  size: 28.0,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
