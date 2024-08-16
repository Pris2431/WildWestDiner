import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo
from hal import hal_keypad as keypad
from hal import hal_buzzer as buzzer

# Empty queue to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

# Define drink names
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

# Callback function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def display_main_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1)Order drinks", 1)
    lcd.lcd_display_string("2)Collect drinks", 2)

def drink_restock(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("Select drink", 1)
    lcd.lcd_display_string("to restock", 2)

    while True:
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()

            # Ensure keyvalue is between 1 and 9
            if isinstance(keyvalue, int) and 1 <= keyvalue <= 9:
                drink_num = keyvalue
                lcd.lcd_clear()
                lcd.lcd_display_string(f"How many {drink_names[drink_num]}", 1)
                lcd.lcd_display_string("to restock?", 2)

                # Wait for user to input the number of drinks to restock
                stock_value = ""
                while True:
                    if not shared_keypad_queue.empty():
                        digit = shared_keypad_queue.get()
                        if isinstance(digit, int):  # Ensure digit is an integer
                            stock_value += str(digit)
                            lcd.lcd_display_string(f"Restock {stock_value} {drink_names[drink_num]}", 1)
                            lcd.lcd_display_string("Confirm with *", 2)
                        elif digit == '*':
                            lcd.lcd_clear()
                            lcd.lcd_display_string("Restocking", 1)
                            lcd.lcd_display_string(f"{stock_value} {drink_names[drink_num]}", 2)
                            time.sleep(2)
                            buzzer.beep(0.5, 0.5, 1)  # Beep once after restocking
                            return  # Exit after confirming the restock
                        elif digit == '#':
                            lcd.lcd_clear()
                            lcd.lcd_display_string("Cancelled", 1)
                            lcd.lcd_display_string("Operation", 2)
                            time.sleep(2)
                            return  # Exit after cancelling

def enter_idle_mode(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("Enter any key", 1)
    lcd.lcd_display_string("Machine in idle", 2)
    time.sleep(10)
    lcd.backlight(0)  # Turn off backlight

    # Wait for key press to exit idle mode
    while True:
        if not shared_keypad_queue.empty():
            _ = shared_keypad_queue.get()
            lcd.backlight(1)  # Turn on backlight
            display_main_menu(lcd)
            return  # Exit idle mode
        time.sleep(1)

def main():
    # Initialize components
    buzzer.init()
    servo.init()
    dc_motor.init()
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    
    lcd = LCD.lcd()
    lcd.lcd_clear()

    idle_timer = time.time()

    display_main_menu(lcd)

    entered_code = ""

    while True:
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            idle_timer = time.time()  
            entered_code += str(keyvalue)
            if entered_code == '6857*':
                lcd.lcd_clear()
                lcd.lcd_display_string("Maintenance", 1)
                lcd.lcd_display_string("Restock", 2)
                time.sleep(1)
                drink_restock(lcd)
                lcd.lcd_clear()
                display_main_menu(lcd)  
                entered_code = ""  

            elif len(entered_code) > len('6857*'):
                entered_code = ""

        if time.time() - idle_timer >= 30:
            enter_idle_mode(lcd)
            idle_timer = time.time() 
            entered_code = "" 

        time.sleep(0.1) 

if __name__ == "__main__":
    main()
