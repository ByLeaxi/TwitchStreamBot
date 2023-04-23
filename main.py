# Codder ByLeaxi =)
import random
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Process, Value

def show_banner():
    print(r'''
      ____        _                     _ 
     |  _ \      | |                   (_)
     | |_) |_   _| |     ___  __ ___  ___ 
     |  _ <| | | | |    / _ \/ _` \ \/ / |
     | |_) | |_| | |___|  __/ (_| |>  <| |
     |____/ \__, |______\___|\__,_/_/\_\_|
             __/ |                        
            |___/                         

            Twitch Stream Bot =)
    ''')

def run(proxy, process_num, url, wait_time):
    options = Options()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.http', proxy.split(':')[0])
    options.set_preference('network.proxy.http_port', int(proxy.split(':')[1]))
    options.set_preference('network.proxy.ssl', proxy.split(':')[0])
    options.set_preference('network.proxy.ssl_port', int(proxy.split(':')[1]))
    browser = webdriver.Firefox(options=options)

    print(f'İşlem {process_num}: Seçilen Proxy: {proxy}')
    browser.get('https://www.twitch.tv/login')
    time.sleep(5)
    browser.get(url)
    browser.set_window_size(250, 250)
    time.sleep(15)
    print(f'İşlem {process_num}: İzleniyor')
    try:
        kalite = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div/div/div/div/div[2]/div[6]/div/div/div/div/label/div'))
        )
        kalite.click()
    except TimeoutException:
        pass
    finally:
        time.sleep(wait_time)

    browser.quit()
    print(f'İşlem {process_num}: Tamamlandı. Proxy: {proxy}')

if __name__ == '__main__':
    show_banner()
    
    with open('pr.txt', 'r') as f:
        proxies = f.read().splitlines()
    used_proxies = set()

    with open('config.json', 'r') as f:
        config = json.load(f)

    url = config['url']
    num_processes = config['num_processes']
    min_wait_time = config['min_wait_time']
    max_wait_time = config['max_wait_time']
    os.system(f"title Codder ByLeaxi - Link : {url} ")
    
    processes = []
    for i in range(num_processes):
        while True:
            proxy = random.choice(proxies)
            if proxy not in used_proxies:
                used_proxies.add(proxy)
                break
        wait_time = random.randint(min_wait_time, max_wait_time)
        process = Process(target=run, args=(proxy, i+1, url, wait_time))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
