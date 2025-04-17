@extends('layouts.app')
@section('title')
    Dashboard - KrishiConnect
@endsection
@section('breadcrumbs')
    Dashboard
@endsection
@section('content')
  
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            background-color: #f9f9f9;
        }

        .card {
            border: none;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .chart-container {
            position: relative;
            height: 300px;
        }
    </style>

<div class="container-fluid py-4">

    <div class="row g-4 mb-4">
        <div class="col-md-3">
            <div class="card p-3 text-center">
                <p class="text-muted">Total Crop Yield</p>
                <h4>6,621,280 kg</h4>
                <canvas id="cropLine" height="60"></canvas>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card p-3 text-center">
                <p class="text-muted">Water Consumption</p>
                <h4>1,530,270 L</h4>
                <canvas id="waterLine" height="60"></canvas>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card p-3 text-center">
                <p class="text-muted">Soil Health Score</p>
                <h4>75.3%</h4>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card p-3 text-center">
                <p class="text-muted">Irrigation Efficiency</p>
                <h4>88.4%</h4>
            </div>
        </div>
    </div>

    <div class="row g-4 mb-4 text-center">
        <div class="col-md-3">
            <div class="card p-3">
                <p class="text-muted">Soil Moisture</p>
                <canvas id="gauge1"></canvas>
                <p class="fw-bold mt-2">18.6%</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card p-3">
                <p class="text-muted">Avg Rainfall</p>
                <canvas id="gauge2"></canvas>
                <p class="fw-bold mt-2">10 Days</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card p-3">
                <p class="text-muted">Pesticide Used</p>
                <canvas id="gauge3"></canvas>
                <p class="fw-bold mt-2">7 Ltr</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card p-3">
                <p class="text-muted">Next Harvest</p>
                <canvas id="gauge4"></canvas>
                <p class="fw-bold mt-2">28 Days</p>
            </div>
        </div>
    </div>

    <div class="row g-4">
        <div class="col-lg-6">
            <div class="card p-3">
                <h6 class="mb-3 text-muted">Crop Yield vs Rainfall</h6>
                <div class="chart-container">
                    <canvas id="lineChart"></canvas>
                </div>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card p-3">
                <h6 class="mb-3 text-muted">Revenue from Crops</h6>
                <div class="chart-container">
                    <canvas id="barChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // Mini Line Charts
    new Chart(document.getElementById("cropLine"), {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr"],
            datasets: [{
                data: [100, 200, 150, 300],
                borderColor: "#198754",
                tension: 0.4
            }]
        },
        options: {
            plugins: {legend: {display: false}},
            scales: {x: {display: false}, y: {display: false}},
            elements: {point: {radius: 0}}
        }
    });

    new Chart(document.getElementById("waterLine"), {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr"],
            datasets: [{
                data: [150, 120, 180, 160],
                borderColor: "#0d6efd",
                tension: 0.4
            }]
        },
        options: {
            plugins: {legend: {display: false}},
            scales: {x: {display: false}, y: {display: false}},
            elements: {point: {radius: 0}}
        }
    });

    // Gauge-like Doughnut Charts
    const gaugeOptions = {
        cutout: '80%',
        rotation: -90,
        circumference: 180,
        plugins: {legend: {display: false}, tooltip: {enabled: false}}
    };

    new Chart(document.getElementById("gauge1"), {
        type: 'doughnut',
        data: {
            labels: ['Used', 'Left'],
            datasets: [{
                data: [18.6, 100 - 18.6],
                backgroundColor: ['#198754', '#e9ecef']
            }]
        },
        options: gaugeOptions
    });

    new Chart(document.getElementById("gauge2"), {
        type: 'doughnut',
        data: {
            labels: ['Used', 'Left'],
            datasets: [{
                data: [10, 90],
                backgroundColor: ['#0d6efd', '#e9ecef']
            }]
        },
        options: gaugeOptions
    });

    new Chart(document.getElementById("gauge3"), {
        type: 'doughnut',
        data: {
            labels: ['Used', 'Left'],
            datasets: [{
                data: [7, 93],
                backgroundColor: ['#ffc107', '#e9ecef']
            }]
        },
        options: gaugeOptions
    });

    new Chart(document.getElementById("gauge4"), {
        type: 'doughnut',
        data: {
            labels: ['Used', 'Left'],
            datasets: [{
                data: [28, 72],
                backgroundColor: ['#dc3545', '#e9ecef']
            }]
        },
        options: gaugeOptions
    });

    // Main Line Chart
    new Chart(document.getElementById("lineChart"), {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
            datasets: [
                {
                    label: 'Crop Yield',
                    data: [150, 180, 170, 210, 220, 240, 300, 280, 250, 230],
                    borderColor: "#198754",
                    tension: 0.4
                },
                {
                    label: 'Rainfall',
                    data: [60, 90, 100, 130, 120, 110, 150, 140, 100, 80],
                    borderColor: "#0dcaf0",
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Bar Chart
    new Chart(document.getElementById("barChart"), {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            datasets: [{
                label: 'Revenue (NPR)',
                data: [10000, 15000, 12000, 18000, 22000, 25000, 27000, 29000],
                backgroundColor: '#198754'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
</script>
</body>
</html>

@endsection
