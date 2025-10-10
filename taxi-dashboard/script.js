// Global variables
let currentData = tripData;
let currentPage = 1;
const itemsPerPage = 10;

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
});

function initializeDashboard() {
    updateMetrics();
    renderCharts();
    renderTable();
}

function setupEventListeners() {
    // Filter events
    document.getElementById('apply-filters').addEventListener('click', applyFilters);
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
    document.getElementById('trip-distance').addEventListener('input', function() {
        document.getElementById('distance-value').textContent = this.value;
    });
    
    // Table events
    document.getElementById('search-table').addEventListener('input', renderTable);
    document.getElementById('sort-by').addEventListener('change', renderTable);
    document.getElementById('prev-page').addEventListener('click', previousPage);
    document.getElementById('next-page').addEventListener('click', nextPage);
}

// Update key metrics
function updateMetrics() {
    const totalTrips = currentData.length;
    const avgFare = currentData.length > 0 
        ? currentData.reduce((sum, trip) => sum + trip.fare_amount, 0) / currentData.length 
        : 0;
    const avgDistance = currentData.length > 0 
        ? currentData.reduce((sum, trip) => sum + trip.trip_distance, 0) / currentData.length 
        : 0;
    const avgDuration = currentData.length > 0 
        ? currentData.reduce((sum, trip) => {
            const duration = (new Date(trip.dropoff_time) - new Date(trip.pickup_time)) / (1000 * 60);
            return sum + duration;
        }, 0) / currentData.length 
        : 0;

    document.getElementById('total-trips').textContent = totalTrips.toLocaleString();
    document.getElementById('avg-fare').textContent = `$${avgFare.toFixed(2)}`;
    document.getElementById('avg-distance').textContent = `${avgDistance.toFixed(2)} miles`;
    document.getElementById('avg-duration').textContent = `${avgDuration.toFixed(0)} min`;
}

// Render all charts
function renderCharts() {
    renderHourlyChart();
    renderFareDistanceChart();
    renderPaymentChart();
    renderSpeedChart();
}

// Chart 1: Trip Distribution by Hour
function renderHourlyChart() {
    const hourlyData = Array(24).fill(0);
    
    currentData.forEach(trip => {
        const hour = new Date(trip.pickup_time).getHours();
        hourlyData[hour]++;
    });
    
    const ctx = document.getElementById('hourly-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.hourlyChart) {
        window.hourlyChart.destroy();
    }
    
    window.hourlyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({length: 24}, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Number of Trips',
                data: hourlyData,
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Trips by Hour of Day'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Trips'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });
}

// Chart 2: Fare vs. Distance
function renderFareDistanceChart() {
    const ctx = document.getElementById('fare-distance-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.fareDistanceChart) {
        window.fareDistanceChart.destroy();
    }
    
    window.fareDistanceChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Fare vs. Distance',
                data: currentData.map(trip => ({
                    x: trip.trip_distance,
                    y: trip.fare_amount
                })),
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Fare Amount vs. Trip Distance'
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Fare Amount ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Trip Distance (miles)'
                    }
                }
            }
        }
    });
}

// Chart 3: Payment Method Distribution
function renderPaymentChart() {
    const paymentCounts = {
        credit: 0,
        cash: 0
    };
    
    currentData.forEach(trip => {
        paymentCounts[trip.payment_type]++;
    });
    
    const ctx = document.getElementById('payment-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.paymentChart) {
        window.paymentChart.destroy();
    }
    
    window.paymentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Credit Card', 'Cash'],
            datasets: [{
                data: [paymentCounts.credit, paymentCounts.cash],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Payment Method Distribution'
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Chart 4: Average Speed by Hour
function renderSpeedChart() {
    const hourlySpeed = Array(24).fill(0);
    const hourlyCount = Array(24).fill(0);
    
    currentData.forEach(trip => {
        const hour = new Date(trip.pickup_time).getHours();
        const duration = (new Date(trip.dropoff_time) - new Date(trip.pickup_time)) / (1000 * 60 * 60); // in hours
        const speed = trip.trip_distance / duration;
        
        if (isFinite(speed) && speed < 100) { // Filter out unrealistic speeds
            hourlySpeed[hour] += speed;
            hourlyCount[hour]++;
        }
    });
    
    const avgHourlySpeed = hourlySpeed.map((sum, i) => 
        hourlyCount[i] > 0 ? sum / hourlyCount[i] : 0
    );
    
    const ctx = document.getElementById('speed-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.speedChart) {
        window.speedChart.destroy();
    }
    
    window.speedChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 24}, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Average Speed (mph)',
                data: avgHourlySpeed,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Average Speed by Hour of Day'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Average Speed (mph)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });
}

// Render data table
function renderTable() {
    const tableBody = document.getElementById('trips-table-body');
    const searchTerm = document.getElementById('search-table').value.toLowerCase();
    const sortBy = document.getElementById('sort-by').value;
    
    // Filter and sort data
    let filteredData = currentData.filter(trip => 
        trip.pickup_time.toLowerCase().includes(searchTerm) ||
        trip.fare_amount.toString().includes(searchTerm) ||
        trip.trip_distance.toString().includes(searchTerm) ||
        trip.payment_type.toLowerCase().includes(searchTerm)
    );
    
    filteredData.sort((a, b) => {
        if (sortBy === 'pickup_time') {
            return new Date(a.pickup_time) - new Date(b.pickup_time);
        } else {
            return a[sortBy] - b[sortBy];
        }
    });
    
    // Calculate pagination
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, filteredData.length);
    const pageData = filteredData.slice(startIndex, endIndex);
    
    // Clear table
    tableBody.innerHTML = '';
    
    // Populate table
    pageData.forEach(trip => {
        const duration = Math.round((new Date(trip.dropoff_time) - new Date(trip.pickup_time)) / (1000 * 60));
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${formatDateTime(trip.pickup_time)}</td>
            <td>${trip.trip_distance.toFixed(2)}</td>
            <td>${duration}</td>
            <td>$${trip.fare_amount.toFixed(2)}</td>
            <td>${trip.payment_type === 'credit' ? 'Credit Card' : 'Cash'}</td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Update pagination info
    document.getElementById('page-info').textContent = `Page ${currentPage} of ${totalPages}`;
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage === totalPages || totalPages === 0;
}

// Helper function to format date/time
function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

// Pagination functions
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
    }
}

function nextPage() {
    const totalPages = Math.ceil(currentData.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderTable();
    }
}

// Filter functions
function applyFilters() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const maxDistance = parseFloat(document.getElementById('trip-distance').value);
    const paymentType = document.getElementById('payment-type').value;
    
    currentData = tripData.filter(trip => {
        const tripDate = trip.pickup_time.split(' ')[0];
        const distanceMatch = trip.trip_distance <= maxDistance;
        const dateMatch = (!startDate || tripDate >= startDate) && (!endDate || tripDate <= endDate);
        const paymentMatch = paymentType === 'all' || trip.payment_type === paymentType;
        
        return distanceMatch && dateMatch && paymentMatch;
    });
    
    currentPage = 1;
    updateMetrics();
    renderCharts();
    renderTable();
}

function resetFilters() {
    document.getElementById('start-date').value = '';
    document.getElementById('end-date').value = '';
    document.getElementById('trip-distance').value = 50;
    document.getElementById('distance-value').textContent = '50';
    document.getElementById('payment-type').value = 'all';
    
    currentData = tripData;
    currentPage = 1;
    updateMetrics();
    renderCharts();
    renderTable();
}

// Function to fetch data from your backend API (to be implemented)
async function fetchDataFromBackend() {
    try {
        // Replace with your actual API endpoint
        const response = await fetch('http://localhost:5000/api/trips');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data from backend:', error);
        return tripData; // Fallback to sample data
    }
}