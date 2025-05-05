from db import exec_dict, connect_db
import adafruit_dht
import board
import time
import RPi.GPIO as GPIO

# sensor, 3,3v pin 4
DHT_PIN = board.D4
sensor = adafruit_dht.DHT22(DHT_PIN)

# led, pin 17
RED_LED_PIN = 0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)


while True:
    try:
        temp = sensor.temperature
        humi = sensor.humidity
        print(f'temperatur: {temp}')
        print(f'humidiy: {humi}')

        query = f"INSERT INTO mesurments (temperature, humidity) VALUES ({temp}, {humi});"
        with connect_db() as cur:
            cur.executescript(query)
        print("writing sucessful")
        GPIO.output(17,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(17,GPIO.LOW)
            
    except RuntimeError as error:
        print(f"Erreur capteur : {error}")
        continue
    except Exception as error:
        print(f"Exception : {error}")
        sensor.exit ()
        raise error
    time.sleep (3) #30 seconds sleep
