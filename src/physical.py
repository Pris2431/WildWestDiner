import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo
from hal import hal_rfid_reader as rfid_reader
from hal import hal_keypad as keypad
from hal import hal_buzzer as buzzer

# Empty queue to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

# Callback function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def display_main_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1)Order drinks", 1)
    lcd.lcd_display_string("2)Collect drinks", 2)

def main():
    # Initialize components
    buzzer.init()
    reader = rfid_reader.init()
    servo.init()
    dc_motor.init()

    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    
    lcd = LCD.lcd()
    lcd.lcd_clear()

    idle_timer = time.time()
    idle_mode = False

    display_main_menu(lcd)

    while True:
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
                            display_main_menu(lcd)
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
                    while id is None or id == "None":
                        id = reader.read_id_no_block()
                        time.sleep(0.1)  # Small delay to prevent busy-waiting

                    if id != "None":
                        # Valid RFID detected, proceed with dispensing
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Dispensing", 1)
                        time.sleep(3)  # Simulate dispensing time
                        
                        # Display collection message
                        lcd.lcd_display_string("Ready for ", 1)
                        lcd.lcd_display_string("Collection", 2)
                        time.sleep(5)
                        buzzer.beep(0.5, 0.5, 3)
                        # Servo and motor action for dispensing
                        servo.set_servo_position(20)
                        time.sleep(1)
                        servo.set_servo_position(80)
                        time.sleep(1)
                        servo.set_servo_position(120)
                        time.sleep(1)
                        
                        
                        # Start the motor to complete dispensing
                        dc_motor.set_motor_speed(70)
                        time.sleep(4)
                        dc_motor.set_motor_speed(0)
                        time.sleep(2)
                        

                        # Return to main menu
                        display_main_menu(lcd)
                        idle_timer = time.time()  # Reset idle timer after returning to menu
                    else:
                        # Handle invalid RFID scenario
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Invalid RFID", 1)
                        time.sleep(2)
                        display_main_menu(lcd)

        # Check for idle state
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
                    display_main_menu(lcd)
                time.sleep(1)
        time.sleep(0.1)  # Wait for 100ms before checking again

if __name__ == "__main__":
    main()
