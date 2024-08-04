from picamera2 import Picamera2, Preview
import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo
import cv2

# Empty queue to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

# Callback function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def main():
    servo.init()
    dc_motor.init()

    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    # Set up Picamera2
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)},
                                                      lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()

    lcd = LCD.lcd()
    lcd.lcd_clear()

    idle_timer = time.time()
    idle_mode = False

    lcd.lcd_display_string("1) Order drinks", 1)
    lcd.lcd_display_string("2) Collect drinks", 2)

    while True:
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            idle_timer = time.time()  # Reset idle timer
            idle_mode = False
            lcd.backlight(1)  # Turn on backlight

            if keyvalue == '1':  # Physical
                lcd.lcd_clear()
                lcd.lcd_display_string("Enter drink code", 1)
                drink_code = ""
                while True:
                    if not shared_keypad_queue.empty():
                        digit = shared_keypad_queue.get()
                        if digit == '*':  # Confirmation key
                            print(f"Drink code entered: {drink_code}")
                            lcd.lcd_clear()
                            break
                        elif digit == '#':  # Return to main menu
                            lcd.lcd_clear()
                            lcd.lcd_display_string("1) Order drinks", 1)
                            lcd.lcd_display_string("2) Collect drinks", 2)
                            break
                        drink_code += str(digit)
                        lcd.lcd_display_string(drink_code, 2)

            elif keyvalue == '2':  # Remote
                lcd.lcd_clear()
                lcd.lcd_display_string("Scan QR Code", 1)
                while True:
                    # Capture an image using Picamera2
                    img = picam2.capture_array()

                    # Convert to grayscale for QR code detection
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    # QR code detection
                    detector = cv2.QRCodeDetector()
                    data, bbox, _ = detector.detectAndDecode(gray_img)
        
                    # if there is a bounding box, draw one, along with the data
                    if bbox is not None:
                        for i in range(len(bbox)):
                            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 255), thickness=2)
                        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        if data:
                            print(f"QR Code data: {data}")
                            lcd.lcd_display_string("Dispensing drink", 1)
                            time.sleep(2)  # Simulate processing time
                            lcd.lcd_clear()
                            lcd.lcd_display_string("Ready for", 1)
                            lcd.lcd_display_string("collection", 2)
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
                            lcd.lcd_clear() 
                            lcd.lcd_display_string("1) Order drinks", 1)
                            lcd.lcd_display_string("2) Collect drinks", 2)
                            break

        else:
            if time.time() - idle_timer >= 30:
                lcd.lcd_clear()
                lcd.lcd_display_string("Enter any key", 1)
                lcd.lcd_display_string("Machine in idle", 2)
                lcd.backlight(0)  # Turn off backlight
                idle_mode = True
                while idle_mode:
                    if not shared_keypad_queue.empty():
                        _ = shared_keypad_queue.get()
                        idle_timer = time.time()  # Reset idle timer
                        idle_mode = False
                        lcd.backlight(1)  # Turn on backlight
                        lcd.lcd_clear()
                        lcd.lcd_display_string("1) Order drinks", 1)
                        lcd.lcd_display_string("2) Collect drinks", 2)
                    time.sleep(1)
        time.sleep(0.1)  # Wait for 100ms before checking again

if __name__ == "__main__":
    main()
