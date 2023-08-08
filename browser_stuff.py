from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def init_browser(): # look for a better way to do this since I am essentially loading 3 browsers
    # start by defining the options
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/87.0.4280.88 Safari/537.36 ")
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    # pass the defined options and service objects to initialize the web driver
    web_driver = Chrome(options=options, service=chrome_service)
    return web_driver

def get_soup(web_driver, url_string):
    web_driver.get(url_string)
    web_driver.implicitly_wait(5) # forced 5 sec wait time per page load.
    soup = BeautifulSoup(web_driver.page_source, features="lxml")
    return soup