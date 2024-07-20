import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad

# Empty queue to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

# Callback function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def main():
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    
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

            if keyvalue == 1:  # Physical
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
                            lcd.lcd_display_string("1) Order drinks", 1)
                            lcd.lcd_display_string("2) Collect drinks", 2)
                            break
                        drink_code += str(digit)
                        lcd.lcd_display_string(drink_code, 2)
                # Process the drink_code here
                if digit == '*':
                    print(f"Drink code entered: {drink_code}")
                    lcd.lcd_clear()

            elif keyvalue == 2:  # Remote
                lcd.lcd_clear()
                lcd.lcd_display_string("Scan QR Code", 1)
                # Implement remote drink collection logic here
                time.sleep(5)  # Simulate processing time
                lcd.lcd_clear()

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
                        lcd.lcd_display_string("1) Order drinks", 1)
                        lcd.lcd_display_string("2) Collect drinks", 2)
                    time.sleep(1)
        time.sleep(0.1)  # Wait for 100ms before checking again

if __name__ == "__main__":
    main()
