# Smart Vending Machine Project for DevOps for AIoT
This repository is for a smart vending machine for Project for ET0735, DevOps for AIoT, Semester 1 2024.

## Project Overview
<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_05_Group2/assets/145007633/26785512-8b75-4385-a1d2-187b447be92d" alt="vending machine UI" width="300" height="400">

The Smart Drink Vending Machine project aims to design and implement an advanced vending machine system that enhances user convenience, security, and operational efficiency. This project integrates modern technologies to provide a seamless experience for both users and service personnel.

## Features

<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_05_Group2/assets/145007633/2f869fc4-44cd-4f6c-9374-58c4b6c227c8" alt="vending machine UI" width="300">


### User Interaction and Payment System
- *User Interface*: Numeric keypad and LCD screen for selecting drinks.
- *Remote Purchasing*: Smartphone application and external website for managing drink selections.
- *Payment Methods*: RFID card readers, QR codes, barcodes, and NFC for versatile payment options.

### Product Dispensation and Collection
- *QR/Barcode System*: Generates and verifies QR codes or barcodes for collecting purchased drinks.
- *Seamless Interaction*: Efficient dispensation of selected drinks.

### Security Features
- *Burglar Detection*: Monitors and detects attempts to forcefully open the vending machine.
- *Alarm System*: Activates a buzzer upon detection of tampering or unauthorized access.

### Maintenance and Service Access
- *Access Management*: Service technicians and suppliers use a valid user code to disable alarms and open the machine for maintenance and restocking.

### System Integration and Hardware Requirements
- *Hardware Components*: Includes RFID readers, QR/barcode scanners, keypads, LCD screens, NFC readers, and security sensors.
- *Compatibility and Communication*: Ensures smooth interaction between hardware components and the Raspberry Pi.

## Software Architecture

The Smart Vending Machine project utilizes Python for the vending machine program on the Raspberry Pi, Shell Script for launching and restarting Python programs, and JavaScript/TypeScript for the web-based interface and WebSocket server. This setup enables real-time communication between the vending machine and the website.

## Physical Hardware required from Rpi

- *16x2 LCD Display*: User interface for item details and status messages.
- *Buzzer*: Alerts for successful transactions and break-ins.
- *Keypad*: User input and access authorization.
- *Camera*: Scans QR codes and captures images during break-ins.
- *Servo*: Dispensing mechanism.
- *RFID Reader*: Secure payment transactions.


## Additional Features

- *Alarm System*: Triggers during break-ins.
- *Email Alerts*: Sends alerts with images for break-ins.
- *Maintainence Access*: Allows engineers to maintain and restock the vending machine without triggering alarms.


## Role allocation:
- Priscilla (Leader):  Full stack web development (front end: html, js, CSS, figma + backend Django)
- Yohann: Maintenance
- Keliang: Physical Code, Remote Code, Maintenance Code Security Code, Combined Code
- Kayshavv: figma design, Inventory excel sheet (Credit card details, Quantity of drinks)
