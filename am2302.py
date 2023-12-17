import Adafruit_DHT
import sqlite3
import logging
from datetime import datetime

# Config logger
logging.basicConfig(
    filename='sensor_log.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def insert_data(temperature, humidity):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO readings (date, temperature, humidity)
        VALUES (?, ?, ?)
    ''', (current_date, temperature, humidity))
    connection.commit()

sensor = Adafruit_DHT.AM2302  # DHT AM2302 sensor
pin = 4  # GPIO pin number

connection = sqlite3.connect('db.sqlite3')

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# Create a table if it doesn't exist to store the data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL
    )
''')

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f'{log_date} - Temp={temperature:0.1f}*C  Humidity={humidity:0.1f}%'
    logger.info(log_msg)
    
    temperature_str = f"{temperature:0.1f}"
    humidity_str = f"{humidity:0.1f}"
    insert_data(temperature_str, humidity_str)
else:
    error_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_msg = f'{error_date} - Failed to get reading. Try again!'
    logger.error(error_msg)

connection.close()
