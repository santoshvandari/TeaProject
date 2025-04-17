@extends('layouts.app')

@section('title', 'Scan Plant - KrishiConnect')

@section('breadcrumbs', 'Scan Plant')

@section('content')
<div class="container-fluid d-flex justify-content-center align-items-center" style="max-height: 80vh; overflow: scroll;">
    <div class="main-container" style="transform: scale(0.8); transform-origin: top center; width: 100%; height: 100%;">
        <form id="scanForm" enctype="multipart/form-data" class="p-4">
            <div class="row g-3">
                <!-- Camera Capture -->
                <div class="col-md-6">
                    <div class="text-center">
                        <video id="cameraPreview" class="border rounded w-100" autoplay playsinline style="height: 400px; object-fit: cover;"></video>
                        
                        <img id="capturedImagePreview" src="" alt="Captured Image" class="img-fluid mt-3 rounded" style="display: none; max-height: 400px;" />

                        <button type="button" id="captureButton" class="btn btn-success mt-3 w-100 fw-bold">Capture</button>
                        <button type="button" id="retakeButton" class="btn btn-dark mt-3 w-100 fw-bold" style="display: none;">Retake</button>

                        <canvas id="capturedCanvas" style="display: none;"></canvas>
                    </div>
                </div>

                <div class="col-md-1 d-flex align-items-center justify-content-center">
                    <h4>OR</h4>
                </div>

                <!-- File Upload and Drag & Drop -->
                <div class="col-md-5">
                    <div class="text-center">
                        <div id="dropZone" class="border p-4 bg-white rounded d-flex flex-column align-items-center justify-content-center" 
                            style="border: 2px dashed #007bff; height: 200px; cursor: pointer; transition: all 0.3s ease;">
                            <p class="text-muted mb-0">Click to upload or drag & drop an image</p>
                        </div>
                        <input type="file" id="fileInput" name="image" accept="image/*" style="display: none;" required>

                        <img id="filePreview" src="" alt="Uploaded Preview" class="img-fluid mt-3 rounded" style="display: none; max-height: 400px;" />
                    </div>
                </div>
            </div>

            <button type="submit" id="submitButton" class="btn btn-primary mt-4 fw-bold w-100" style="display: none;">Submit</button>
        </form>

        <div id="apiResponse" class="mt-5">
            <div id="responseContent" class="p-4 border rounded text-center" style="min-height: 100px;">
                <p class="text-muted mb-0"></p>
                <!-- Adding the loading spinner -->
                <div id="loadingSpinner" class="spinner-border text-info" role="status" style="display: none;">
                    <span class="visually-hidden">Processing...</span>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const cameraPreview = document.getElementById('cameraPreview');
const captureButton = document.getElementById('captureButton');
const retakeButton = document.getElementById('retakeButton');
const capturedCanvas = document.getElementById('capturedCanvas');
const capturedImagePreview = document.getElementById('capturedImagePreview');
const filePreview = document.getElementById('filePreview');
const scanForm = document.getElementById('scanForm');
const submitButton = document.getElementById('submitButton');
const responseContent = document.getElementById('responseContent');
const loadingSpinner = document.getElementById('loadingSpinner');

let isImageSelected = false;

function enableSubmitButton() {
    if (isImageSelected) {
        submitButton.style.display = 'block';
    }
}

function resetCameraView() {
    capturedImagePreview.style.display = 'none';
    cameraPreview.style.display = 'block';
    captureButton.style.display = 'block';
    retakeButton.style.display = 'none';
}

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            cameraPreview.srcObject = stream;
        })
        .catch((err) => {
            console.error('Camera access denied:', err);
            alert('Unable to access the camera. Please check your permissions.');
        });
}

captureButton.addEventListener('click', () => {
    const context = capturedCanvas.getContext('2d');
    capturedCanvas.width = cameraPreview.videoWidth;
    capturedCanvas.height = cameraPreview.videoHeight;
    context.drawImage(cameraPreview, 0, 0, capturedCanvas.width, capturedCanvas.height);

    capturedCanvas.toBlob((blob) => {
        const file = new File([blob], 'captured-image.jpg', { type: 'image/jpeg' });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        isImageSelected = true;
        enableSubmitButton();

        const imageURL = URL.createObjectURL(blob);
        capturedImagePreview.src = imageURL;
        capturedImagePreview.style.display = 'block';
        cameraPreview.style.display = 'none';
        captureButton.style.display = 'none';
        retakeButton.style.display = 'block';
        filePreview.style.display = 'none';
    });

});

retakeButton.addEventListener('click', () => {
    resetCameraView();
    fileInput.value = '';
    isImageSelected = false;
    submitButton.style.display = 'none';
});

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#0056b3';
    dropZone.style.transform = 'scale(1.05)';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#007bff';
    dropZone.style.transform = 'scale(1)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#007bff';
    dropZone.style.transform = 'scale(1)';
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith('image/')) {
        fileInput.files = files;
        previewFile(files[0]);
    } else {
        alert('Please upload a valid image file.');
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        previewFile(fileInput.files[0]);
    }
});

function previewFile(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        filePreview.src = e.target.result;
        filePreview.style.display = 'block';
        capturedImagePreview.style.display = 'none';
        cameraPreview.style.display = 'block';
        captureButton.style.display = 'block';
        retakeButton.style.display = 'none';
        isImageSelected = true;
        enableSubmitButton();
    };
    reader.readAsDataURL(file);
}

scanForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Smooth scroll to the response section
    document.getElementById('apiResponse').scrollIntoView({ behavior: 'smooth' });

    responseContent.innerHTML = '<p class="text-info">Processing...</p>';
    loadingSpinner.style.display = 'inline-block'; // Show the spinner

    const file = fileInput.files[0];
    if (!file) {
        responseContent.innerHTML = '<p class="text-danger">No image selected.</p>';
        loadingSpinner.style.display = 'none'; // Hide the spinner
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:8001/predict/', {
            method: 'POST',
            body: formData,
        });

        const contentType = response.headers.get('content-type');
        let result;

        if (contentType && contentType.includes('application/json')) {
            result = await response.json();
        } else {
            result = await response.text();
            result = { message: result };
        }
        
        if (response.ok) {
            const { summary, predicted_image } = result[0];  // Accessing the first result from the array
            responseContent.innerHTML = `
                <p class="text-success fw-bold">${summary}</p>
                <img src="../API/${predicted_image}" alt="Predicted Image" class="img-fluid mt-3">
            `;
        } else {
            responseContent.innerHTML = `<p class="text-danger fw-bold">${result.message || 'Something went wrong.'}</p>`;
        }
    } catch (error) {
        console.error('API Error:', error);
        responseContent.innerHTML = `<p class="text-danger">Error connecting to prediction API.</p>`;
    } finally {
        loadingSpinner.style.display = 'none'; // Hide the spinner once processing is complete
    }
});
</script>
@endsection
