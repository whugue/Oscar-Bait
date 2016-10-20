

"""
Script:     01-Movie-Scrape.py
Purpose:    Scrape data from boxofficemojo.com and match to data pulled from Open Mobie Database (OMDB) API
Input:      Pages from boxofficemojo.com
			Movie data pulled from OMDB API
Output:    	data/movie_data_raw_YYYY.pickle 
"""

import re
import requests
from bs4 import BeautifulSoup
import omdb
import pickle


def scrape_value(soup, regex):
	return soup.find(text=re.compile(regex)).findNextSibling().text.strip()

def clean_runtime(raw_value):
	if raw_value.upper()!="N/A":
		return int(raw_value.split()[0])*60+int(raw_value.split()[2])
	else:
		return np.nan

def clean_budget(raw_value):
	if raw_value.upper()!="N/A":
		value_list=raw_value.replace("$","").replace(",","").split()
	
		if len(value_list)>1 and value_list[1]=="million": #previously checked, no billions
			clean_value=float(value_list[0])*1000000
		else:
			clean_value=float(value_list[0])

		return clean_value
	else:
		return np.nan

def inflation_adjust(year, raw_value): #Inflation adjusted calulated from BLS inflation calculator: http://www.bls.gov/data/inflation_calculator.htm
	if year==2006:
		adj_value=raw_value*0.969
	elif year==2007:
		adj_value=raw_value*0.942
	elif year==2008:
		adj_value=raw_value*0.907
	elif year==2009:
		adj_value=raw_value*0.910
	elif year==2010:
		adj_value=raw_value*0.896
	elif year==2011:
		adj_value=raw_value*0.868
	elif year==2012:
		adj_value=raw_value*0.851
	elif year==2013:
		adj_value=raw_value*0.838
	elif year==2014:
		adj_value=raw_value*0.825
	elif year==2015:
		adj_value=raw_value*0.824
	else:
		adj_value=raw_value

	return adj_value


def scrape_movie(url):
	soup=BeautifulSoup(requests.session().get(url).text, "lxml")

	#Scrape Movie Title & Release Date
	title=soup.find("title").text
	title=title.split("(")[0].strip()
	release_date=scrape_value(soup, "Release Date:")


	#Convert Release Date to Python Datetime Object and Derive Release Month and Year
	release_date=parse(release_date)
	release_month=release_date.month
	release_year=release_date.year


	#Scrape Genre, Rating, Runtime, and Budget
	genre=scrape_value(soup, "Genre:")
	rating=scrape_value(soup, "Rating:")
	runtime=scrape_value(soup, "Runtime:")
	budget=scrape_value(soup, "Production Budget:")

	#Clean-Up Runtime and Budget
	runtime=clean_runtime(runtime)
	budget=clean_budget(budget)
	budget=inflation_adjust(release_year, budget)


	#Scrape Number of Oscar Noms, Number Oscar Wins, and List of Oscar Nominations
	url=url.replace("/movies/","/oscar/movies/")
	soup=BeautifulSoup(requests.session().get(url).text, "lxml") 
	oscar_links=soup.find_all("a", href=True)
	
	oscar_noms=0
	oscar_wins=0
	oscar_list=[]

	for link in soup.find_all("a", href=True):
		if link["href"].find("oscar/chart/")>0:
			oscar=str(link.contents[0].encode('utf-8'))

			if re.search("View All", oscar.title())==None:
				oscar_noms+=1

				if re.search("(WIN)", oscar.upper())>0:
					oscar_wins+=1

				oscar_list.append(oscar)


	#Pull in Rotten Tomato Ratings & Plot Description from OMDB API
	search_results=omdb.search_movie(title)

	imdb_id=None
	for result in search_results:
		if int(result["year"])==release_year:
			imdb_id=result["imdb_id"]
			break

	if imdb_id != None:	
		omdb_content=omdb.imdbid(imdb_id, tomatoes=True)
		
		metascore=omdb_content["metascore"]
		imdb_rating=omdb_content["imdb_rating"]
		tomato_meter=omdb_content["tomato_meter"]
		tomato_user_meter=omdb_content["tomato_user_meter"]
		plot=omdb_content["plot"]

	else:
		metascore=None
		imdb_rating=None
		tomato_meter=None
		tomato_user_meter=None
		plot=None

	#Store Data for One movie in dictionary
	keys=["title","release_date","release_year","genre","rating","runtime","budget","imdb_id","metascore","imdb_rating","tomato_meter","tomato_user_meter","plot","oscar_noms","oscar_wins"]
	values=[title,release_date,release_year,genre,rating,runtime,budget,imdb_id,metascore,imdb_rating,tomato_meter,tomato_user_meter,plot,oscar_noms,oscar_wins]

	d=dict(zip(keys,values))

	return d

#print scrape_movie("http://www.boxofficemojo.com/movies/?id=mariesstory.htm")

#Scrape Movie and Page Links from Yearly URL Index
def scrape_links(url,lookup):
	soup=BeautifulSoup(requests.session().get(url).text, "lxml")

	links=set()
	for link in soup.find_all("a", href=True):
		if link["href"].find(lookup)>0:
			full_link="http://www.boxofficemojo.com"+link["href"]
			links.add(full_link)

	links=list(links)
	links.sort()

	return links



#Scrape From All Year in Analysis Period
def scrape_years(start_year,stop_year):
	for yr in range(start_year,(stop_year+1)):
		data=[]

		print "Starting Scape for: "+str(yr)

		year_link="http://www.boxofficemojo.com/yearly/chart/?yr="+str(yr)+"&p=.htm"

		movie_links=scrape_links(year_link,"movies/?id=")
		for movie_link in movie_links:
			try:
				row=scrape_movie(movie_link)
				data.append(row)
				print "Scraped: "+row["title"], row["release_year"]
			except:
				print "SCRAPE FAILED: "+movie_link

		page_links=scrape_links(year_link,"page=")
		for page_link in page_links:
			movie_links=scrape_links(page_link,"movies/?id=")

			for movie_link in movie_links:
				try:
					row=scrape_movie(movie_link)
					data.append(row)
					print "Scraped: "+row["title"], row["release_year"]
				except:
					print "SCRAPE FAILED: "+movie_link

		print str(yr)+" Pickle Output:  "+str(len(data))

		#Save data as Pickle
		out_pickle="data/movie_data_raw_"+str(yr)+".pickle"

		with open(out_pickle, "wb") as f:
			pickle.dump(data, f)


#Scrape Analysis Years in Batches
scrape_years(2005,2015)






