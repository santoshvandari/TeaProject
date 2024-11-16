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
      // Handle no cameras available
      print('No cameras available');
      return;
    }
    _controller = CameraController(cameras[0], ResolutionPreset.medium);

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
      appBar: AppBar(title: const Text("Capture Tea Leaf")),
      body: FutureBuilder(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            return CameraPreview(
                _controller); // Show camera preview once initialized
          } else {
            return const Center(
                child:
                    CircularProgressIndicator()); // Show loading spinner while initializing
          }
        },
      ),
      floatingActionButton: Align(
        alignment: Alignment.bottomCenter,
        child: FloatingActionButton(
          onPressed: _takePicture,
          child: const Icon(Icons.camera),
        ),
      ),
    );
  }
}
