import 'dart:async';
import 'dart:convert'; // For JSON decoding
import 'package:http/http.dart' as http;

class ApiService {
  // The FastAPI URL for disease prediction
  static const String apiUrl =
      'http://192.168.18.10:8000/predict/'; // Replace with your server's IP address

  // Function to upload image and get the disease predictions
  static Future<Map<String, dynamic>> uploadImage(String imagePath) async {
    try {
      // Create a multipart request
      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));

      // Add the image file to the request
      request.files.add(await http.MultipartFile.fromPath(
        'file', // The field name in the API
        imagePath,
        filename:
            imagePath.split('/').last, // Extract the file name from the path
      ));

      // Send the request and wait for the response
      var response = await request.send().timeout(
        Duration(seconds: 300), // Set the timeout duration to 90 seconds
        onTimeout: () {
          // Handle timeout scenario
          throw TimeoutException("The connection has timed out.");
        },
      );

      // Parse the response if the status code is 200 (OK)
      if (response.statusCode == 200) {
        final responseData = await response.stream.bytesToString();
        final jsonResponse = jsonDecode(responseData);

        // Check if the response contains the predictions
        if (jsonResponse is List) {
          return {
            'success': true,
            'predictions': jsonResponse, // List of predictions
          };
        } else {
          return {
            'success': false,
            'message': jsonResponse['message'] ?? "No predictions available."
          };
        }
      } else {
        return {
          'success': false,
          'error':
              'Failed to process image. Status code: ${response.statusCode}'
        };
      }
    } catch (e) {
      // Handle any exceptions or errors
      return {
        'success': false,
        'error': 'An error occurred: $e',
      };
    }
  }
}
