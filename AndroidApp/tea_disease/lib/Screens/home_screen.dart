import 'package:flutter/material.dart';
import 'package:tea_disease/Screens/result_screen.dart';
import 'package:tea_disease/Services/api.dart';
import 'camera_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? result;

  void _onPhotoCaptured(String imagePath) async {
    final response = await ApiService.uploadImage(imagePath);
    setState(() {
      if (response['success']) {
        result = response['data'];
      } else {
        result = response['error'];
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Tea Leaf Analysis")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        CameraScreen(onPhotoCaptured: _onPhotoCaptured),
                  ),
                );
              },
              child: const Text("Capture Tea Leaf"),
            ),
            if (result != null) ...[ResultScreen(result: result!)],
          ],
        ),
      ),
    );
  }
}
