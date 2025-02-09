<?php
// Database credentials
$servername = "localhost";      // usually "localhost" for a local server
$username   = "root";           // default XAMPP username is "root"
$password   = "";               // default XAMPP password is empty
$dbname     = "inventory";  // replace with your actual database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully to the database!";
?>
