import sys
import os
import time
import schedule
import requests
import subprocess

TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
PRIVATE_IP = os.environ['PRIVATE_IP']
TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)
BASE = os.environ['BASE']

def get_temperature():
    try:
        output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8')
        result = output.split('=')[1].strip().replace("'C", "")
        return float(result)
    except FileNotFoundError:
        raise ImportError('\'vcgencmd\' does not exist in path')

def send_message(temperature):
    message = '- Temperature: %s°C\n- Server: %s' % (temperature,PRIVATE_IP)
    try: 
        payload = {
                "text": message.encode("utf-8"),
                "chat_id": CHAT_ID
        }
        requests.post(TELEGRAM_URL, payload)
    except Exception as e:
        raise e

def polling():
    temp = get_temperature()
    result = 'elapsed_time: %.0f, temperature: %s\n' % ((time.time() - start_time),temp)
    print(result, end='') 

    if temp > int(BASE):
        send_message(temp)

if __name__ == '__main__':
    start_time = time.time()
    schedule.every(60).seconds.do(polling)
    while True:
        schedule.run_pending()
        time.sleep(1)
