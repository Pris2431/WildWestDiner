<?php
// Database configuration
$dbHost = 'localhost';
$dbUsername = 'local host';
$dbPassword = 'root';
$dbName = 'wildwestdiner';

// Create database connection
$conn = new mysqli($dbHost, $dbUsername, $dbPassword, $dbName);

// Check connection
if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => 'Database connection failed']));
}

// Create reservations table if it doesn't exist
$sql = "CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    guests VARCHAR(10) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)";

if (!$conn->query($sql)) {
    error_log("Error creating reservations table: " . $conn->error);
    die(json_encode(['success' => false, 'message' => 'Server configuration error']));
}

// Process reservation form
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $response = array();
    
    try {
        // Validate required fields
        $required_fields = ['name', 'email', 'phone', 'date', 'time', 'guests'];
        foreach ($required_fields as $field) {
            if (!isset($_POST[$field]) || empty($_POST[$field])) {
                throw new Exception("All required fields must be filled out");
            }
        }

        // Validate email
        if (!filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)) {
            throw new Exception("Invalid email format");
        }

        // Sanitize and escape input
        $name = $conn->real_escape_string($_POST['name']);
        $email = $conn->real_escape_string($_POST['email']);
        $phone = $conn->real_escape_string($_POST['phone']);
        $date = $conn->real_escape_string($_POST['date']);
        $time = $conn->real_escape_string($_POST['time']);
        $guests = $conn->real_escape_string($_POST['guests']);
        $notes = isset($_POST['notes']) ? $conn->real_escape_string($_POST['notes']) : '';

        // Check if the requested date and time slot is available
        $check_sql = "SELECT COUNT(*) as count FROM reservations 
                     WHERE reservation_date = ? AND reservation_time = ?";
        $stmt = $conn->prepare($check_sql);
        $stmt->bind_param("ss", $date, $time);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        
        if ($row['count'] >= 10) { // Assuming max 10 reservations per time slot
            throw new Exception("This time slot is fully booked. Please select another time.");
        }

        // Insert reservation
        $sql = "INSERT INTO reservations (name, email, phone, reservation_date, reservation_time, guests, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("sssssss", $name, $email, $phone, $date, $time, $guests, $notes);
        
        if ($stmt->execute()) {
            // Send confirmation email
            $to = $email;
            $subject = "Reservation Confirmation - Wild West Diner";
            $message = "Dear $name,\n\n";
            $message .= "Thank you for your reservation at Wild West Diner.\n\n";
            $message .= "Reservation Details:\n";
            $message .= "Date: $date\n";
            $message .= "Time: $time\n";
            $message .= "Number of Guests: $guests\n";
            $message .= "Special Requests: $notes\n\n";
            $message .= "If you need to modify or cancel your reservation, please contact us at (555) 123-4567.\n\n";
            $message .= "Best regards,\nWild West Diner Team";
            
            $headers = "From: reservations@wildwestdiner.com";
            
            mail($to, $subject, $message, $headers);
            
            $response = ['success' => true, 'message' => 'Reservation confirmed successfully'];
        } else {
            throw new Exception("Error processing reservation");
        }
        
    } catch (Exception $e) {
        $response = ['success' => false, 'message' => $e->getMessage()];
    }
    
    // Send JSON response
    header('Content-Type: application/json');
    echo json_encode($response);
}

$conn->close();
?>