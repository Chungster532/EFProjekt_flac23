import multiprocessing
import threading
import requests
import time

def spam():
    for i in range(100):
        threading.Thread(target=spam2).start()

def spam2():
    
    while True:
        requests.get('http://192.168.1.109:5000')
        print('request')

if __name__ == '__main__':
    for i in range(10):
        time.sleep(1)
        multiprocessing.Process(target=spam).start()