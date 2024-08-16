import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo
from hal import hal_rfid_reader as rfid_reader
from hal import hal_keypad as keypad
from hal import hal_buzzer as buzzer

# Drink options mapping
drink_names = {
    1: "Cola",
    2: "Sprite",
    3: "Pepsi",
    4: "A&W",
    5: "Fanta",
    6: "F&N",
    7: "Milo",
    8: "Tea",
    9: "Water"
}

# Queue for handling keypad inputs
shared_keypad_queue = queue.Queue()

# Callback function for keypad press events
def key_pressed(key):
    shared_keypad_queue.put(key)

# Display the main menu on the LCD
def display_main_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1)Order drinks", 1)
    lcd.lcd_display_string("2)Collect drinks", 2)

def main():
    # Initialize all components
    buzzer.init()
    reader = rfid_reader.init()
    servo.init()
    dc_motor.init()
    keypad.init(key_pressed)

    # Start the keypad input thread
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
            idle_timer = time.time()  # Reset idle timer on any key press
            idle_mode = False
            lcd.backlight(1)  # Ensure backlight is on

            if keyvalue == 1:  # Option to order drinks
                lcd.lcd_clear()
                lcd.lcd_display_string("Enter drink code", 1)
                drink_code = ""
                while True:
                    if not shared_keypad_queue.empty():
                        digit = shared_keypad_queue.get()
                        if digit == '*':  # Confirm input
                            break
                        elif digit == '#':  # Cancel and return to main menu
                            display_main_menu(lcd)
                            break
                        drink_code += str(digit)
                        lcd.lcd_display_string(drink_code, 2)

                if digit == '*':
                    print(f"Drink code entered: {drink_code}")

                    # Convert drink_code to an integer and look up the drink name
                    drink_id = int(drink_code)
                    drink_name = drink_names.get(drink_id, "Unknown")

                    lcd.lcd_clear()
                    lcd.lcd_display_string(f"Option: {drink_name}", 1)  # Fixed this line
                    lcd.lcd_display_string("Tap RFID Card", 2)

                    # Wait for valid RFID card
                    id = None
                    while id is None or id == "None":
                        id = reader.read_id_no_block()
                        time.sleep(0.1)  # Small delay to avoid busy-waiting

                    if id != "None":
    
                        lcd.lcd_clear()
                        lcd.lcd_display_string(f"Dispensing", 1)
                        lcd.lcd_display_string(f"{drink_name}", 2)
                        time.sleep(3)  # Simulate dispensing time
    
                        # Clear the first line explicitly before displaying "Ready for"
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Ready for      ", 1)  # Added padding to clear previous text
                        lcd.lcd_display_string("Collection", 2)
                        time.sleep(5)
                        buzzer.beep(0.5, 0.5, 1)

                        # Operate the servo motor in three steps
                        servo.set_servo_position(20)
                        time.sleep(1)
                        servo.set_servo_position(80)
                        time.sleep(1)
                        servo.set_servo_position(120)
                        time.sleep(1)

                        # Start and stop the motor to complete the dispensing action
                        dc_motor.set_motor_speed(70)
                        time.sleep(4)
                        dc_motor.set_motor_speed(0)
                        time.sleep(2)

                        # Return to the main menu after dispensing
                        display_main_menu(lcd)
                        idle_timer = time.time()  # Reset idle timer
                    else:
                        # Handle invalid RFID input
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Invalid RFID", 1)
                        time.sleep(2)
                        display_main_menu(lcd)

        # Check for idle mode after 30 seconds of inactivity
        if time.time() - idle_timer >= 30:
            lcd.lcd_clear()
            lcd.lcd_display_string("Enter any key", 1)
            lcd.lcd_display_string("Machine in idle", 2)
            time.sleep(10)
            lcd.backlight(0)  # Turn off backlight to save power
            idle_mode = True

            # Exit idle mode on any key press
            while idle_mode:
                if not shared_keypad_queue.empty():
                    _ = shared_keypad_queue.get()
                    idle_timer = time.time()  # Reset idle timer
                    idle_mode = False
                    lcd.backlight(1)  # Turn on backlight
                    display_main_menu(lcd)
                time.sleep(1)

        time.sleep(0.1)  # Brief delay to control the loop's polling rate

if __name__ == "__main__":
    main()