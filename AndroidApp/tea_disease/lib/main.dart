import 'package:flutter/material.dart';
import 'package:tea_disease/Screens/home_screen.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<void> main() async {
  // Load the .env file
  await dotenv.load();

  runApp(const DiseaseApp());
}

class DiseaseApp extends StatelessWidget {
  const DiseaseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tea Disease Detection',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: HomeScreen(),
    );
  }
}
