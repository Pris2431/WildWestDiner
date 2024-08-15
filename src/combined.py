import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_servo as servo
from hal import hal_keypad as keypad
from hal import hal_buzzer as buzzer
from hal import hal_input_switch as slide_switch
from hal import hal_dc_motor as dc_motor
from hal import hal_rfid_reader as rfid_reader

# Shared queue for keypad input
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

def key_pressed(key):
    shared_keypad_queue.put(key)

def display_main_menu(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("1)Order drinks", 1)
    lcd.lcd_display_string("2)Collect drinks", 2)

def handle_security_breach(lcd, buzzer):
    lcd.lcd_clear()
    lcd.lcd_display_string("Security Breach", 1)
    buzzer.beep(0.5, 0.5, 2)
    servo.set_servo_position(20)
    time.sleep(1)
    servo.set_servo_position(80)
    time.sleep(1)
    servo.set_servo_position(120)
    time.sleep(1)

    entered_code = ""
    while True:
        if not shared_keypad_queue.empty():
            digit = shared_keypad_queue.get()
            if digit == '*':
                if entered_code == "387":
                    buzzer.beep(0, 0, 0)
                    lcd.lcd_clear()
                    display_main_menu(lcd)
                    return
                else:
                    entered_code = ""
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Invalid Code", 1)
                    time.sleep(2)
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Enter Code", 1)
            else:
                entered_code += str(digit)
                lcd.lcd_display_string(entered_code, 2)
                time.sleep(0.5)

def drink_restock(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("Select drink", 1)
    lcd.lcd_display_string("to restock", 2)

    while True:
        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            if isinstance(keyvalue, int) and 1 <= keyvalue <= 9:
                drink_num = keyvalue
                lcd.lcd_clear()
                lcd.lcd_display_string(f"How many {drink_names[drink_num]}", 1)
                lcd.lcd_display_string("to restock?", 2)

                stock_value = ""
                while True:
                    if not shared_keypad_queue.empty():
                        digit = shared_keypad_queue.get()
                        if isinstance(digit, int):
                            stock_value += str(digit)
                            lcd.lcd_display_string(f"Restock {stock_value} {drink_names[drink_num]}", 1)
                            lcd.lcd_display_string("Confirm with *", 2)
                        elif digit == '*':
                            lcd.lcd_clear()
                            lcd.lcd_display_string("Restocking", 1)
                            lcd.lcd_display_string(f"{stock_value} {drink_names[drink_num]}", 2)
                            time.sleep(2)
                            buzzer.beep(0.5, 0.5, 1)
                            return
                        elif digit == '#':
                            lcd.lcd_clear()
                            lcd.lcd_display_string("Cancelled", 1)
                            lcd.lcd_display_string("Operation", 2)
                            time.sleep(2)
                            return

def enter_idle_mode(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("Enter any key", 1)
    lcd.lcd_display_string("Machine in idle", 2)
    time.sleep(10)
    lcd.backlight(0)

    while True:
        if not shared_keypad_queue.empty():
            _ = shared_keypad_queue.get()
            lcd.backlight(1)
            display_main_menu(lcd)
            return
        time.sleep(1)

def main():
    buzzer.init()
    servo.init()
    dc_motor.init()
    reader = rfid_reader.init()
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    
    lcd = LCD.lcd()
    lcd.lcd_clear()

    slide_switch.init()
    idle_timer = time.time()
    entered_code = ""

    display_main_menu(lcd)

    while True:
        if slide_switch.read_slide_switch() == 1:
            handle_security_breach(lcd, buzzer)
            idle_timer = time.time()
            continue

        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            idle_timer = time.time()
            lcd.backlight(1)

            if keyvalue == 1:
                lcd.lcd_clear()
                lcd.lcd_display_string("Enter drink code", 1)
                drink_code = ""
                while True:
                    if not shared_keypad_queue.empty():
                        digit = shared_keypad_queue.get()
                        if digit == '*':
                            break
                        elif digit == '#':
                            display_main_menu(lcd)
                            break
                        drink_code += str(digit)
                        lcd.lcd_display_string(drink_code, 2)

                if digit == '*':
                    drink_id = int(drink_code)
                    drink_name = drink_names.get(drink_id, "Unknown")

                    lcd.lcd_clear()
                    lcd.lcd_display_string(f"Option: {drink_name}", 1)
                    lcd.lcd_display_string("Tap RFID Card", 2)

                    id = None
                    while id is None or id == "None":
                        id = reader.read_id_no_block()
                        time.sleep(0.1)

                    if id != "None":
                        lcd.lcd_clear()
                        lcd.lcd_display_string(f"Dispensing", 1)
                        lcd.lcd_display_string(f"{drink_name}", 2)
                        time.sleep(3)
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Ready for      ", 1)
                        lcd.lcd_display_string("Collection", 2)
                        time.sleep(5)
                        buzzer.beep(0.5, 0.5, 1)

                        servo.set_servo_position(20)
                        time.sleep(1)
                        servo.set_servo_position(80)
                        time.sleep(1)
                        servo.set_servo_position(120)
                        time.sleep(1)

                        dc_motor.set_motor_speed(70)
                        time.sleep(4)
                        dc_motor.set_motor_speed(0)
                        time.sleep(2)

                        display_main_menu(lcd)
                        idle_timer = time.time()
                    else:
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Invalid RFID", 1)
                        time.sleep(2)
                        display_main_menu(lcd)

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
