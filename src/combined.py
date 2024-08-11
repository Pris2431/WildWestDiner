import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from picamera2 import Picamera2
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo
from hal import hal_rfid_reader as rfid_reader
from pyzbar.pyzbar import decode
from PIL import Image

# Empty queue to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

# Callback function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def scan_qr_code(picamera2):
    while True:
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            if keyvalue == '#':  # Return to main menu
                return None
        picamera2.capture_file("/tmp/qr_image.jpg")
        img = Image.open("/tmp/qr_image.jpg")
        qr_codes = decode(img)
        if qr_codes:
            return qr_codes[0].data.decode("utf-8")
        time.sleep(0.1)

def main():
    reader = rfid_reader.init()
    servo.init()
    dc_motor.init()
    
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    
    lcd = LCD.lcd()
    lcd.lcd_clear()

    picam2 = Picamera2()
    picam2.start()

    idle_timer = time.time()
    idle_mode = False

    while True:
        lcd.lcd_display_string("1)Order drinks", 1)
        lcd.lcd_display_string("2)Collect drinks", 2)

        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            idle_timer = time.time()  # Reset idle timer
            idle_mode = False
            lcd.backlight(1)  # Turn on backlight

            if keyvalue == 1:  # Physical order
                lcd.lcd_clear()
                lcd.lcd_display_string("Enter drink code", 1)
                drink_code = ""
                while True:
                    if not shared_keypad_queue.empty():
                        digit = shared_keypad_queue.get()
                        if digit == '*':  # Confirmation key
                            break
                        elif digit == '#':  # Return to main menu
                            lcd.lcd_clear()
                            lcd.lcd_display_string("1)Order drinks", 1)
                            lcd.lcd_display_string("2)Collect drinks", 2)
                            break
                        drink_code += str(digit)
                        lcd.lcd_display_string(drink_code, 2)
                
                # Process the drink_code here
                if digit == '*':
                    print(f"Drink code entered: {drink_code}")
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Tap RFID Card", 1)

                    # Wait for RFID input
                    id = None
                    while id == None or id == "None":
                        id = reader.read_id_no_block()
                        time.sleep(0.1)

                    if id != "None":
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Dispensing", 1)
                        time.sleep(5)
                        lcd.lcd_display_string("Ready for ", 1)
                        lcd.lcd_display_string("Collection", 2)
                        time.sleep(5)
                        # Servo and motor action
                        servo.set_servo_position(20)
                        time.sleep(1)
                        servo.set_servo_position(80)
                        time.sleep(1)
                        servo.set_servo_position(120)
                        time.sleep(1)
                        dc_motor.set_motor_speed(50)
                        time.sleep(4)
                        dc_motor.set_motor_speed(0)
                        time.sleep(2)
                    else:
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Invalid RFID", 1)
                        time.sleep(2)
                        lcd.lcd_clear()
                        lcd.lcd_display_string("1)Order drinks", 1)
                        lcd.lcd_display_string("2)Collect drinks", 2)

            elif keyvalue == 2:  # Remote collection via QR code
                lcd.lcd_clear()
                lcd.lcd_display_string("Scan QR Code", 1)
                while True:
                    if not shared_keypad_queue.empty():
                        digit = shared_keypad_queue.get()
                        if digit == '#':  # Return to main menu
                            lcd.lcd_clear()
                            lcd.lcd_display_string("1)Order drinks", 1)
                            lcd.lcd_display_string("2)Collect drinks", 2)
                            break
                    qr_code = scan_qr_code(picam2)
                    if qr_code is None:  # User cancelled scanning
                        lcd.lcd_clear()
                        lcd.lcd_display_string("1)Order drinks", 1)
                        lcd.lcd_display_string("2)Collect drinks", 2)
                        break
                    elif qr_code:  # Assuming any QR code is valid for this example
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Dispensing", 1)
                        time.sleep(5)
                        lcd.lcd_display_string("Ready for ", 1)
                        lcd.lcd_display_string("Collection", 2)
                        time.sleep(5)
                        # Servo and motor action
                        servo.set_servo_position(20)
                        time.sleep(1)  
                        servo.set_servo_position(80)
                        time.sleep(1)     
                        servo.set_servo_position(120)
                        time.sleep(1)            
                        dc_motor.set_motor_speed(50)
                        time.sleep(4)   
                        dc_motor.set_motor_speed(0)
                        time.sleep(2)
        else:
            if time.time() - idle_timer >= 30:
                lcd.lcd_clear()
                lcd.lcd_display_string("Enter any key", 1)
                lcd.lcd_display_string("Machine in idle", 2)
                time.sleep(10)
                lcd.backlight(0)  # Turn off backlight
                idle_mode = True
                while idle_mode:
                    if not shared_keypad_queue.empty():
                        _ = shared_keypad_queue.get()
                        idle_timer = time.time()  # Reset idle timer
                        idle_mode = False
                        lcd.backlight(1)  # Turn on backlight
                        lcd.lcd_clear()
                        lcd.lcd_display_string("1)Order drinks", 1)
                        lcd.lcd_display_string("2)Collect drinks", 2)
                    time.sleep(1)
        time.sleep(0.1)  # Wait for 100ms before checking again

if _name_ == "_main_":
    main()