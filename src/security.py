import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_servo as servo
from hal import hal_keypad as keypad
from hal import hal_buzzer as buzzer
from hal import hal_input_switch as slide_switch

shared_keypad_queue = queue.Queue()

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

def main():
    buzzer.init()
    servo.init()
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    
    lcd = LCD.lcd()
    lcd.lcd_clear()

    slide_switch.init()

    display_main_menu(lcd)

    while True:
        if slide_switch.read_slide_switch() == 1:  
            handle_security_breach(lcd, buzzer)
            idle_timer = time.time()  
            continue  

        if not shared_keypad_queue.empty():
            keyvalue = shared_keypad_queue.get()
            idle_timer = time.time() 
            idle_mode = False
            lcd.backlight(1) 

if __name__ == "__main__":
    main()