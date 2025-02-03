<?php
// mailinglist.php

// Set error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Set headers to handle CORS and JSON response
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Function to sanitize input data
function sanitize_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

// Function to validate email
function is_valid_email($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL);
}

// Function to validate Singapore phone number
function is_valid_singapore_phone($phone) {
    return preg_match("/^(\+65|65)?[89]\d{7}$/", $phone);
}

// Initialize response array
$response = array(
    'success' => false,
    'message' => ''
);

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    try {
        // Collect and sanitize form data
        $name = isset($_POST['name']) ? sanitize_input($_POST['name']) : '';
        $email = isset($_POST['email']) ? sanitize_input($_POST['email']) : '';
        $phone = isset($_POST['phone']) ? sanitize_input($_POST['phone']) : '';
        $message = isset($_POST['message']) ? sanitize_input($_POST['message']) : '';

        // Validate inputs
        $errors = array();

        // Validate name (2-50 characters, letters and spaces only)
        if (empty($name) || !preg_match("/^[a-zA-Z\s]{2,50}$/", $name)) {
            $errors[] = "Invalid name format";
        }

        // Validate email
        if (empty($email) || !is_valid_email($email)) {
            $errors[] = "Invalid email format";
        }

        // Validate Singapore phone number
        if (empty($phone) || !is_valid_singapore_phone($phone)) {
            $errors[] = "Please key in a valid Singapore phone number";
        }

        // Validate message (minimum 10 characters)
        if (empty($message) || strlen($message) < 10) {
            $errors[] = "Message must be at least 10 characters long";
        }

        // If no validation errors, process the form
        if (empty($errors)) {
            // Prepare email content
            $to = "priscillaloi2020@gmail.com"; //my actual email address
            $subject = "New Contact Form Submission - Wild West Diner";
            
            // Create HTML email content
            $email_content = "<html><body>";
            $email_content .= "<h2>New Contact Form Submission</h2>";
            $email_content .= "<p><strong>Name:</strong> " . htmlspecialchars($name) . "</p>";
            $email_content .= "<p><strong>Email:</strong> " . htmlspecialchars($email) . "</p>";
            $email_content .= "<p><strong>Phone:</strong> " . htmlspecialchars($phone) . "</p>";
            $email_content .= "<p><strong>Message:</strong><br>" . nl2br(htmlspecialchars($message)) . "</p>";
            $email_content .= "</body></html>";
            
            // Email headers
            $headers = array(
                'MIME-Version: 1.0',
                'Content-type: text/html; charset=UTF-8',
                'From: ' . $email,
                'Reply-To: ' . $email,
                'X-Mailer: PHP/' . phpversion()
            );

            // Try to send email
            if (mail($to, $subject, $email_content, implode("\r\n", $headers))) {
                // Optional: Log successful submissions
                $log_message = date('Y-m-d H:i:s') . " - New contact form submission from: " . $email . "\n";
                file_put_contents('contact_log.txt', $log_message, FILE_APPEND);
                $response['success'] = true;
                $response['message'] = "Thank you for your message. We'll get back to you soon!";
            } else {
                throw new Exception("Failed to send email");
            }
        } else {
            $response['message'] = "Validation errors: " . implode(", ", $errors);
        }
    } catch (Exception $e) {
        // Log the error
        error_log("Contact form error: " . $e->getMessage());
        $response['message'] = "Sorry, there was an error processing your message. Please try again later.";
    }
} else {
    $response['message'] = "Invalid request method";
}

// Return JSON response
echo json_encode($response);
?>