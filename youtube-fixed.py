#!/usr/bin/python3

import bs4
from bs4 import BeautifulSoup as bs
import requests
import time
import matplotlib.pyplot as plt
import re

x,t,s,v,l,d =[1,2,3,4,5],["vid1","vid2","vid3","vid4","vid5"],[],[],[],[]
def graphVideos(fname):
	response = input("Enter Number to Graph Values\n [1] Views, [2] Subscribers, [3] Likes, [4] Dislikes, [5] Close Script: ")

	choice = ""
	if response == "1":
		choice = "Views"
	elif response == "2":
		choice = "Subscribers"
	elif response == "3":
		choice = "Likes"
	elif response == "4":
		choice = "Dislikes"
	elif response == "5":
		exit()


	if choice != "":
		plt.title(choice+" Plot")
		plt.ylabel("Number of "+choice)
		plt.xlabel("Video Number")
		plt.xticks(x,t)
		if response == "1":
			plt.plot(x,v)
		if response == "2":
			plt.plot(x,s)
		if response == "3":
			plt.plot(x,l)
		if response == "4":
			plt.plot(x,d)
		plt.get_fignums()
		plt.show()
		graphVideos(fname)

	else:
		print("Number doesnt match given choices")
		graphVideos(fname)



filename = input("Name the output file: ")
f=open("./"+filename,'w')
response = input("Search Youtube for: ")

youtubeurl = "https://www.youtube.com"
url = "https://www.youtube.com/results?search_query="

response.replace(" ","+")
req = requests.get(url+response)
soup=bs(req.text,'html.parser')
vids = soup.findAll("div",{"class":"yt-lockup-content"})
itm = 0
count = 0
while count < 5:   #get first five videos
	if 'rel' in vids[itm].a.attrs: #check if video and not user
		vidurl=vids[itm].a['href'] #get video url

		try:		#test to make sure the format is type video and not channel or advertisement. Also accounts for request overload
			vidre=requests.get("https://www.youtube.com"+vidurl)
			count=count+1
		except:
			print("Problem with request to server...")
			print("Let me sleep for 5 seconds")
			time.sleep(5)
			itm=itm+1
			continue

		vidsoup=bs(vidre.text,'html.parser')#get html to video
		divuser = vidsoup.find("div",{"class":"yt-user-info"})
		user= divuser.a.text			#get username
		userpage= divuser.a["href"]
		req1 = requests.get(youtubeurl+userpage)
		soup1=bs(req1.text,'html.parser') #open youtube channel to get exact number of subscribers

		subscriberdiv = soup1.find("div",{"class":"primary-header-actions"}) #find items in header
		subscriberspan = subscriberdiv.findAll("span")
		tmpsubscribers = subscriberspan[7].text #find the seventh span which contains subscriber count
		subscribers = re.sub('[^0-9]','', tmpsubscribers)
		try:
			s.append(int(subscribers))
		except:
			s.append(0)

		spantitle = vidsoup.find("span",{"class":"watch-title"}) #find the video title
		title = spantitle["title"]

		divviews = vidsoup.find("div",{"class":"watch-view-count"})#find video views
		tmpviews=divviews.text
		views = re.sub('[^0-9]','', tmpviews)
		try:
			v.append(int(views))
		except:
			v.append(0)

		spanlikes = vidsoup.find("button",{"title":"I like this"})#get video likes
		tmplikes = spanlikes.text
		likes = re.sub('[^0-9]','', tmplikes)
		try:
			l.append(int(likes))
		except:
			l.append(0)


		spandislikes = vidsoup.find("button",{"title":"I dislike this"})#get video dislikes
		tmpdislikes = spandislikes.text
		dislikes = re.sub('[^0-9]','', tmpdislikes)
		try:
			d.append(int(dislikes))
		except:
			d.append(0)

		strongdate = vidsoup.find("strong",{"class":"watch-time-text"})#get video date
		date = strongdate.text

		divdescription = vidsoup.find("div",{"id":"watch-description-text"})#get video descritpion
		lst = list(divdescription.descendants)
		description = ""
		for i in range(1,len(lst)):
			if type(lst[i]) is not bs4.element.Tag:
				description= description+lst[i]+"\n"

		f.write("Video "+str(count)+": Title: "+title+" \n")		#print the information to a file
		f.write("Channel: "+user+" \n")
		f.write("Subscribers: "+subscribers+" \n")
		f.write("Views: "+views +" \n")
		f.write("Likes: "+likes + " \n")
		f.write("Dislikes: "+dislikes+'\n')
		f.write("Date Published: "+date+" \n")
		f.write("Description: "+description+" \n")

	itm=itm+1

f.flush()
graphVideos(filename)
