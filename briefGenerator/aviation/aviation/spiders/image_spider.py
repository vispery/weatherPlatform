from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)
driver.get("http://aviation.nmc.cn/")
time.sleep(2)
hover_element = driver.find_element_by_id('radarImage')
ActionChains(driver).move_to_element(hover_element).perform()
driver.find_element_by_xpath('//*[@id="inputRadarImage"]/div').click()
mapdiv = driver.find_element_by_id('map')
mapdiv.screenshot('airportmap.png')  # 元素截图
driver.quit()
