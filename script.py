from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_videos(channel):
	# adapted from https://stackoverflow.com/a/74585946
	options = webdriver.ChromeOptions()
	options.add_experimental_option("detach", True)
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-notifications")
	options.add_argument("--disable-Advertisement")
	options.add_argument("--disable-popup-blocking")
	options.add_argument("start-maximized")
	driver= webdriver.Chrome(options=options)

	driver.get('https://www.youtube.com/@%s/videos' % channel)
	time.sleep(3)

	#item = []
	prev_height = driver.execute_script("return document.documentElement.scrollHeight")

	while True:
		driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
		time.sleep(1)
		curr = driver.execute_script("return document.documentElement.scrollHeight")

		if curr == prev_height:
			break
		prev_height = curr

	data = []
	try:
		for e in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
			title = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('title')
			vurl = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('href')
			data.append({
				'video_url':vurl,
				'title':title
			})
	except:
		pass
		
	return data
	
pattern = re.compile(r'(\d{4}(\.\d{2}(\.\d{2})?)?)')
def compare(title):
	match = pattern.search(title)
	if match:
		return match.group()
	return title

if __name__ == '__main__':
	if len(sys.argv) == 2:
		channel = sys.argv[1]
		videos = get_videos(channel)
	
		videos.sort(key=lambda dict: compare(dict['title']))
	
		for vid in videos:
			print(vid['title'])
		
	else:
		print('Usage: py script.py <channel>')
	
