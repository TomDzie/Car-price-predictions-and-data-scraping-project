# Scraping data and predicting car prices out of them  
1. [ Description. ](#desc)
2. [ Scraping data. ](#coll)
3. [ Checking requests. ](#prob)
4. [ Price predicting process. ](#usage)

<a name="desc"></a>  
## 1. Description  

This project is about estimating users car value on market. Project startet with my interest in BMW 140i which is pretty unsulal car these days.
The point is that the prices where not consistant so it was really hard to estimate its market value. I came up with idea to reagularly scrape car advertising portal and make database out of scraped soup.
I started wit beautifullSoup tutorials and than managed to scrape and save everything I wanted to SQLite database. Every offer came with its own id so every record in DB stayed unique.
I used to collect that data for some time and than I wanted to connect that topic with my Big Data university project. I had and idea to estimate regullar user's car value so it will be easier to post and sell it.
I implemented some machine learning techniques I learned on courses and other projects and this is what came out of it.  

<a name="coll"></a>  
## 2. Scraping data  

First step of geting the data is chosing the right source and tool. For the source I chose most popular polish most popular car advertising portal,
all data is easly axcessed, there are no anti scraping "walls" or other inconveniences. The tool Im using is BeautifullSoup library in Python,
pretty easy to understand, and it offers all I need right now. Then it was time to code, scraping is basicly extracting data from requested html sheet and cleaning it from unwanted characters and thats what I did.
I went through html by findig right element classes. First I was scraping offers ID and url to their site without going deeper, then I check which offer is already in database If it wasn't, I went into url and scraped all needed info.
Then I replaced all polish letters and sent it to database.  

<a name="prob"></a>  
## 3. Checking requests   
This is where I encountered first problems, the first one was redirecting to other site, this is something this site use to do with specyfic offers so if page redirects I abandon it, as easy as that.
Other problem is loading unexpected html, I mean different than i used to see, reason for that is they might have changed page just alittle or its just a bug. I handled this by checking if there is class that allways used to be there.  

<a name="prob"></a>  
## 3. Price predicting process   

