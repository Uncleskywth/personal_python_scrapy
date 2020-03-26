from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from urllib.request import urlretrieve
from urllib import request
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
def download_podcast(url, path):
	req = request.Request(url, headers=headers)
	data = request.urlopen(req).read()
	with open(path, 'wb') as f:
		f.write(data)
		f.close()
	
page_urls,episodes,episode_urls,download_urls = [],[],[],[]
for i in range(1,2):
	page_urls.append("https://www.surplusvalue.club/episodes/page/" + str(i))
for page_url in page_urls:
	html = urlopen(page_url)
	bsObj = BeautifulSoup(html,"lxml")
	h3s = bsObj.findAll("h3")
	for h3 in h3s:
		href = h3.find("a")
		if href:
			episode_urls.append("https://www.surplusvalue.club" + href.attrs['href'])
		else:
			continue
print("Urls of episodes have been collected!")
#print(episode_urls)
#episode_url = "https://www.surplusvalue.club/newsatcrisis"
for episode_url in episode_urls:
	episode_url_html = urlopen(episode_url)
	episode_bsObj = BeautifulSoup(episode_url_html,"lxml")
	download = episode_bsObj.findAll("a",href=re.compile(".*mp3"))[1].attrs['href']
	episode_name = episode_bsObj.find("div",{"class":"hero-info"}).h1.get_text()
	#print(episode_name)
	episode_name = re.sub('：*·*(\?)*《*》*“*”*？*','',episode_name)
	episodes.append({"name":episode_name,"download_url":download})
print("Information of episodes has been collected!")
for episode in episodes:
	try:
		download_podcast(episode['download_url'],episode['name'] + ".mp3")
		print(episode['name'] + "has been downloaded!")
	except Exception as e:
		print(episode['name'] + "ERROR")
#【049】News at Crisis：危机新闻与新闻危机
