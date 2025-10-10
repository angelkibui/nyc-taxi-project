// Sample data - Replace with actual API calls to your backend
const sampleTrips = [
    {
        id: 1,
        pickup_time: "2023-05-15 08:30:00",
        dropoff_time: "2023-05-15 08:45:00",
        trip_distance: 2.5,
        fare_amount: 12.50,
        tip_amount: 2.50,
        total_amount: 15.00,
        payment_type: "credit",
        pickup_lat: 40.7614,
        pickup_lng: -73.9776,
        dropoff_lat: 40.7505,
        dropoff_lng: -73.9934
    },
    {
        id: 2,
        pickup_time: "2023-05-15 12:15:00",
        dropoff_time: "2023-05-15 12:40:00",
        trip_distance: 4.2,
        fare_amount: 18.75,
        tip_amount: 3.75,
        total_amount: 22.50,
        payment_type: "cash",
        pickup_lat: 40.6892,
        pickup_lng: -74.0445,
        dropoff_lat: 40.7589,
        dropoff_lng: -73.9851
    },
    {
        id: 3,
        pickup_time: "2023-05-15 18:45:00",
        dropoff_time: "2023-05-15 19:15:00",
        trip_distance: 5.8,
        fare_amount: 24.30,
        tip_amount: 4.86,
        total_amount: 29.16,
        payment_type: "credit",
        pickup_lat: 40.7282,
        pickup_lng: -73.9942,
        dropoff_lat: 40.6413,
        dropoff_lng: -73.7781
    },
];

// Generate more sample data for demonstration
function generateSampleData(count) {
    const paymentTypes = ["credit", "cash"];
    const data = [];
    
    for (let i = 0; i < count; i++) {
        const hour = Math.floor(Math.random() * 24);
        const minute = Math.floor(Math.random() * 60);
        const pickupTime = `2023-05-${String(Math.floor(Math.random() * 30) + 1).padStart(2, '0')} ${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}:00`;
        
        const duration = Math.floor(Math.random() * 60) + 5; // 5-65 minutes
        const dropoffTime = new Date(new Date(pickupTime).getTime() + duration * 60000);
        
        const tripDistance = (Math.random() * 20 + 0.5).toFixed(2); // 0.5-20.5 miles
        const fareAmount = (parseFloat(tripDistance) * 2.5 + Math.random() * 10).toFixed(2);
        const tipAmount = (parseFloat(fareAmount) * 0.2).toFixed(2);
        const totalAmount = (parseFloat(fareAmount) + parseFloat(tipAmount)).toFixed(2);
        
        data.push({
            id: i + 1,
            pickup_time: pickupTime,
            dropoff_time: dropoffTime.toISOString().slice(0, 19).replace('T', ' '),
            trip_distance: parseFloat(tripDistance),
            fare_amount: parseFloat(fareAmount),
            tip_amount: parseFloat(tipAmount),
            total_amount: parseFloat(totalAmount),
            payment_type: paymentTypes[Math.floor(Math.random() * paymentTypes.length)],
            pickup_lat: 40.7 + Math.random() * 0.2,
            pickup_lng: -74.0 + Math.random() * 0.2,
            dropoff_lat: 40.7 + Math.random() * 0.2,
            dropoff_lng: -74.0 + Math.random() * 0.2
        });
    }
    
    return data;
}

// Use generated sample data (100 trips)
const tripData = generateSampleData(100);