    while True:  
        # Read door sensor state  
        door_state = GPIO.input(DOOR_SENSOR_PIN)  
          
        # If door is pried open (i.e., sensor is triggered)  
        if door_state == False:  
            print("Door pried open! Activating buzzer...")  
            GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on buzzer  
            time.sleep(5)  # Buzzer sounds for 5 seconds  
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off buzzer  
        else:  
            print("Door is secure.")  
          
        time.sleep(0.5)  # Check door state every 0.5 seconds  
  
except KeyboardInterrupt:  
    GPIO.cleanup()  
import RPi.GPIO as GPIO  
import time  
  
# Set up GPIO pins for door sensor and buzzer  
DOOR_SENSOR_PIN = 17  
BUZZER_PIN = 23  
  
# Set up GPIO mode  
GPIO.setmode(GPIO.BCM)  
  
# Set up door sensor as input and buzzer as output  
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(BUZZER_PIN, GPIO.OUT)  
  
try:  