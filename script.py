from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
import sys
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_videos(channel):
	# adapted from https://stackoverflow.com/a/74585946
	options = webdriver.ChromeOptions()
	options.add_argument("--log-level=3")
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
	
def compare(title, pattern):
	match = pattern.search(title)
	if match:
		return match.group()
	return title

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--channel', '-c', help='channel name', type=str, required=True)
	parser.add_argument('--outfile', '-o', help='output file', type=str)
	parser.add_argument('--sort', '-s', help='regex for sorting', type=str)
	args = parser.parse_args()
	
	print("Getting videos from ", args.channel)
	videos = get_videos(args.channel)

	if args.sort:
		print("Sorting results")
		pattern = re.compile(args.sort)
		videos.sort(key=lambda dict: compare(dict['title'], pattern))

	print("Results")
	outfile = open(args.outfile, 'w') if args.outfile else None

	for vid in videos:
		print(vid['title'], file=outfile)
		
	if outfile:
		outfile.close()
	
