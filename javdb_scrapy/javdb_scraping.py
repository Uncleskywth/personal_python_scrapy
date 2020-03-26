'''import'''
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import bs4
import re
from datetime import datetime
import time

'''函数定义'''
def get_txt_content_clean(contents):
	clean_contents = []
	for content in contents:
		clean_contents.append(re.match("(https.*)(\n)",content).group(1))
	return clean_contents
	
def get_page_contents(page_URL):
	#抓取当前页面的信息,包括磁力链接和链接时间
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	download_magnet,dates = [],[]
	html = Request(page_URL,headers=headers)
	html = urlopen(html)
	bsObj = BeautifulSoup(html,features="lxml")
	page_contents = bsObj.find("div",{"id":"magnets-content"}).findAll("tr")
	for page_content in page_contents:
		time_temporary = page_content.find("td",{"class":"sub-column"}).span.get_text()
		time_temporary = datetime.strptime(time_temporary,'%Y-%m-%d') 
		dates.append(time_temporary)
		download_magnet.append(page_content.find("a",href=re.compile("^(magnet)")).attrs['href'])
	for i in range(len(dates)):
		page_contents[i] = [{"date":dates[i]},{"magnet":download_magnet[i]}]
	#time.sleep(0.3)
	return page_contents

def get_extra_information_on_page(page_URL):
	#抓取当前页面下的其他影片信息
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	Links = []
	html = Request(page_URL,headers=headers)
	html = urlopen(html)
	bsObj = BeautifulSoup(html,features="lxml")
	same_actors_contents = bsObj.findAll("div",{"class":"tile-images tile-small"})[0]
	same_actors_contents = same_actors_contents.findAll("a",{"class":"tile-item"})
	try:
		same_series_contents = bsObj.findAll("div",{"class":"tile-images tile-small"})[1]
		same_series_contents = same_series_contents.findAll("a",{"class":"tile-item"})
	except IndexError:
		for video in same_actors_contents:
			link = "https://javdb4.com" + video.attrs['href']
			title = video.attrs['title']
			Links.append([{"url":link},{"title":title}])
	else:
		for video in same_actors_contents:
			link = "https://javdb4.com" + video.attrs['href']
			title = video.attrs['title']
			Links.append([{"url":link},{"title":title}])
		for video in same_series_contents:
			link = "https://javdb4.com" + video.attrs['href']
			title = video.attrs['title']
			Links.append([{"url":link},{"title":title}])
	return Links
	
def gengerate_category_url(i):
	#输入页面数,生成每个页面中的影片页面的url,并返回
	cate_urls = []
	for j in range(1,i+1):
		cate_urls.append("https://javdb4.com/?page=" + str(j))
	return cate_urls

def get_links_in_category(cate_URL):
	#抓取每一页上的链接\名称\uid
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	contents = []
	urls,titles,uids=[],[],[]
	html = Request(cate_URL,headers=headers)
	html = urlopen(html)
	bsObj = BeautifulSoup(html,features="lxml")
	page_contents = bsObj.findAll("div",{"class":"grid-item column"})
	for page_content in page_contents:
		url = page_content.a
		url = "https://javdb4.com" + url.attrs['href']
		urls.append(url)
		title = page_content.a.attrs['title']
		titles.append(title)
		uid = page_content.find("div",{"class":"uid"}).get_text()
		uids.append(uid)
		contents.append([{"uid":uid},{"title":title},{"url":url}])
	return contents
	
def gather_newpages():
	page_number = input("How many pages do you want to scrapy? \n")
	page_number = int(page_number)
	cate_contents = []
	to_collect_number = 0
	global video_information
	cate_urls = gengerate_category_url(page_number)
	completed_number = 0
	magnet_txt = open('javnew.txt','w')
	for cate_url in cate_urls:
		cate_contents.append(get_links_in_category(cate_url))
	for i in range(len(cate_contents)):
		to_collect_number = to_collect_number + len(cate_contents[i])
	print("Number of pages to collect is " + str(to_collect_number))
	for i in range(len(cate_contents)):
		for content in cate_contents[i]:
			video_url = get_page_contents(content[2]['url'])
			if video_url:
				video_information.append(video_url)
				completed_number = completed_number + 1
				print(str(completed_number) + " pages collected, and total number is " + str(to_collect_number))
				#print(video_url)
				magnet_txt.write(video_url[0][1]['magnet'])
				magnet_txt.write('\n')
			else:
				completed_number = completed_number + 1
				print(str(completed_number) + " pages collected, but this one has no magnet links " + "and total number is " + str(to_collect_number))
				continue
	magnet_txt.close()

def count_all():
	all_urlsfile = open('all_urls_on_javdb.txt','r')
	all_links = all_urlsfile.readlines()
	all_links = get_txt_content_clean(all_links)
	all_urlsfile.close()
	searchedlinks_file = open('searched_urls.txt','r')
	searched_links = searchedlinks_file.readlines()
	searched_links = get_txt_content_clean(searched_links)
	searchedlinks_file.close()
	print('Date input complished!\n')
	total_number = len(all_links)
	start_url = all_links[len(searched_links)]
	#txt = open('')
	#start_url = 'https://javdb4.com/v/4A23R'
	#start_title = '[MIDE-730]大嫌いな夫の上司に巨乳妻は何度も犯●れて'
	#all_information = []
	#all_information.append([{"url":start_url},{"title":start_title}])
	#all_links = []
	#all_links.append(start_url)
	search_status = True
	#searched_links = []
	while search_status:
		search_status = False
		for link in all_links:
			if link not in searched_links:
				search_link = link
				search_status = True
			else:
				continue
		try:
			extra_information = get_extra_information_on_page(search_link)
		except IndexError:
			searched_links.append(search_link)
			print("There is no extra urls on url: " + search_link)
			continue
		number_of_links_to_verify = len(extra_information)
		number_of_new_links = 0
		for information in extra_information:
			url_tested = information[0]["url"]
			if url_tested not in all_links:
				all_links.append(url_tested)
				total_number = total_number+1
				number_of_new_links = number_of_new_links+1
				print("You have found " + str(total_number) + " pages of video on the website! The newest one is " + url_tested)
		print("Above are the new results, the url of the page you are seaching on is :" + search_link)
		print("In this round of search, you have verified " + str(number_of_links_to_verify) + " urls, " + str(number_of_new_links) + " of them are new ones.")
		searched_links.append(search_link)
		time.sleep(0.2)
	print("End of the search, you have found " + str(total_number) + " pages!")
	
def data_update_from_out():
	outputfile = input("Please tell me which is the output file:\n")
	out_file = open(outputfile, "r", encoding='utf-8')
	all_url_file = open("all_urls_on_javdb.txt","a+",encoding='utf-8')
	searched_urls_file = open("searched_urls.txt","a+",encoding='utf-8')
	'''input files'''
	out_data = out_file.readlines()
	#out_data = get_txt_content_clean(out_data)
	urls_from_out,new_searched_urls=[],[]
	all_urls = all_url_file.readlines()
	all_urls = get_txt_content_clean(all_urls)
	searched_urls = searched_urls_file.readlines()
	searched_urls = get_txt_content_clean(searched_urls)
	out_file.close()
	print("The number of collected data is " + str(len(all_urls)))
	print("The number of searched data is " + str(len(searched_urls)))
	'''data store'''
	for line in out_data:
		try:
			url = re.search('The newest one is (https\:\/\/javdb4\.com\/v\/.*)',line).group(1)
			urls_from_out.append(url)
		except AttributeError:
			try:
				url = re.search('you are seaching on is \:(https\:\/\/javdb4\.com\/v\/.*)',line).group(1)
				new_searched_urls.append(url)
			except AttributeError:
				continue
	print("All of the data in output files has been collected!\n")
	'''data extract'''
	all_url_file.writelines('\n')
	for url in urls_from_out:
		all_url_file.writelines(url+'\n')
	for url in new_searched_urls:
		searched_urls_file.writelines(url+'\n')
	'''write files'''
	all_url_file.close()
	searched_urls_file.close()
	print("Files writting completed!\n")
	print("The number of collected data is updated to " + str(len(all_urls)+len(urls_from_out)) + '\n')
	print("The number of searched data is updated to " + str(len(new_searched_urls)+len(searched_urls)) + '\n')

def get_preview(page_URL):
	#抓取当前页面的预览图片和视频,使用时注意不要频繁发送申请到服务器
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	html = Request(page_URL,headers=headers)
	html = urlopen(html)
	bsObj = BeautifulSoup(html,features="lxml")
	preview_pics = []
	uid = bsObj.find("a",{"class":"button copy-to-clipboard"}).attrs["data-clipboard-text"]
	preview_pics.append(bsObj.find("a",{"href":"#preview-video"}).img.attrs['src'])
	preview_video = "https:" + bsObj.find("source",{"type":"video/mp4"}).attrs['src']
	try:
		urlretrieve(preview_video,"preview_videos/" + uid + "pre.mp4")
	except ValueError:
		print("The preview video can't be download!")
	for loading in bsObj.findAll("img",{"src":re.compile("https\:\/\/pics\.dmm\.co\.jp\/digital\/video.*")}):
		preview_pics.append(loading.attrs['src'])
	i = 0
	for link in preview_pics:
		i = i+1
		try:
			urlretrieve(link,"preview_pics/" + uid + "_" + str(i) + ".jpg")
		except ValueError:
			continue
	print("Preview pics and video of " + uid + "have been download.\n")

video_information = []
signal = input('My lord, tell me what you wish: \n1) get some new magnets for me\n2) count all of the items on javdb\n3) update collected data\n')
signal = int(signal)
if signal==1:
	gather_newpages()
elif signal==2:
	count_all()
elif signal==3:
	data_update_from_out()
'''firefox请求头(备用

GET /side-toolbar/1.6/images/fanhuidingbucopy.png HTTP/1.1
Host: g.csdnimg.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
Accept: image/webp,*/*
Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://blog.csdn.net/qq_33326449/article/details/52156518
DNT: 1
Connection: keep-alive
If-Modified-Since: Tue, 24 Dec 2019 10:45:58 GMT
If-None-Match: "5e01ec66-124"
Cache-Control: max-age=0
'''
