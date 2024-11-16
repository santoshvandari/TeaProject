import 'dart:convert'; // For JSON decoding
import 'package:http/http.dart' as http;

class ApiService {
  static const String apiUrl = 'http://192.168.18.10:8000/predict/';

  static Future<Map<String, dynamic>> uploadImage(String imagePath) async {
    try {
      // Create a multipart request
      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));

      // Add the image file to the request
      request.files.add(await http.MultipartFile.fromPath(
        'file', // Ensure field name matches the API
        imagePath,
        filename: imagePath.split('/').last, // Extract file name
      ));

      // Send the request
      var response = await request.send();

      // Parse the response
      if (response.statusCode == 200) {
        final responseData = await response.stream.bytesToString();
        final jsonResponse = jsonDecode(responseData);

        return {
          'success': true,
          'data': jsonResponse,
        };
      } else {
        return {
          'success': false,
          'error':
              'Failed to process image. Status code: ${response.statusCode}',
        };
      }
    } catch (e) {
      return {
        'success': false,
        'error': 'An error occurred: $e',
      };
    }
  }
}
