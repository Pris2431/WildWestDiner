<?php
// Database configuration
$dbHost = 'localhost';
$dbUsername = 'your_username';
$dbPassword = 'your_password';
$dbName = 'wildwestdiner';

// Create database connection
$conn = new mysqli($dbHost, $dbUsername, $dbPassword, $dbName);

// Check connection
if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => 'Database connection failed']));
}

// Create contact_messages table if it doesn't exist
$sql = "CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)";

if (!$conn->query($sql)) {
    error_log("Error creating contact_messages table: " . $conn->error);
    die(json_encode(['success' => false, 'message' => 'Server configuration error']));
}

// Process contact form
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $response = array();
    
    try {
        // Validate required fields
        $required_fields = ['name', 'email', 'phone', 'message'];
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
        $message = $conn->real_escape_string($_POST['message']);

        // Insert message
        $sql = "INSERT INTO contact_messages (name, email, phone, message) VALUES (?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssss", $name, $email, $phone, $message);
        
        if ($stmt->execute()) {
            // Send notification email to admin
            $to = "admin@wildwestdiner.com";
            $subject = "New Contact Form Submission";
            $email_message = "New message from website contact form:\n\n";
            $email_message .= "Name: $name\n";
            $email_message .= "Email: $email\n";
            $email_message .= "Phone: $phone\n";
            $email_message .= "Message:\n$message";
            
            $headers = "From: notifications@wildwestdiner.com";
            
            mail($to, $subject, $email_message, $headers);
            
            // Send auto-reply to customer
            $customer_subject = "Thank you for contacting Wild West Diner";
            $customer_message = "Dear $name,\n\n";
            $customer_message .= "Thank you for contacting Wild West Diner. We have received your message and will respond shortly.\n\n";
            $customer_message .= "Best regards,\nWild West Diner Team";
            
            mail($email, $customer_subject, $customer_message, $headers);
            
            $response = ['success' => true, 'message' => 'Message sent successfully'];
        } else {
            throw new Exception("Error sending message");
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