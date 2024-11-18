import 'package:flutter/material.dart';
import 'package:tea_disease/Screens/home_screen.dart';

void main() {
  runApp(const DiseaseApp());
}

class DiseaseApp extends StatelessWidget {
  const DiseaseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tea Disease Detection',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: HomeScreen(),
    );
  }
}
