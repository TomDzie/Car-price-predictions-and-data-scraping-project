# Scraping data and predicting car prices out of them  
1. [ Description. ](#desc)
2. [ How it works ](#works)
3. [ How it's build ](#build)
4. [ Scraping data. ](#coll)
5. [ Checking requests. ](#prob)
6. [ Price predicting process. ](#usage)
7. [ PCA transformation](#usage)
8. [ Goodness of fit and other informations](#rsqu)
9. [ results](#res)
10. 

<a name="desc"></a>  
## 1. Description  

This project is about estimating users car value on market. Project startet with my interest in BMW 140i.
The point is that the prices where not consistant so it was really hard to estimate its market value. I came up with idea to reagularly scrape car advertising portal and make database out of scraped soup.
I started wit beautifullSoup tutorials and than managed to scrape and save everything I wanted to SQLite database. Every offer came with its own id so every record in DB stayed unique.
I used to collect that data for some time and than I wanted to connect that topic with my Big Data university project. I had and idea to estimate regullar user's car value so it will be easier to post and sell it.
I implemented some machine learning techniques I learned on courses and other projects. This is what came out of it.


<a name="works"></a>  
## 2. How it works  

1. To predict prices we need some data so the first step is collecting a lot of data.
   I used this program to scrape car sales portal every day. Every offer was saved to SQL database. At the end there were around 200 000 records.
   ![image](https://github.com/TomDzie/Car-price-predictions-and-data-scraping-project/assets/117634603/3730604d-d37d-4aa1-908e-f48a89cc4521)

3. 



<a name="build"></a>  
## 2. How its build 

First step of geting the data is chosing the right source and tool. For the source I chose most popular polish most popular car advertising portal,
all data is easly axcessed, there are no anti scraping "walls" or other inconveniences. The tool Im using is BeautifullSoup library in Python,
pretty easy to understand, and it offers all I need right now. Then it was time to code, scraping is basicly extracting data from requested html sheet and cleaning it from unwanted characters and thats what I did.
I went through html by findig right element classes. First I was scraping offers ID and url to their site without going deeper, then I check which offer is already in database If it wasn't, I went into url and scraped all needed info.
Then I replaced all polish letters and sent it to database.  

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
Using specified by user car parameters I generate SQL query and get ready to use data. Than took these steps:    
Spliting for training and testing data, with propotions 4:1, I found this proportion working pretty good, but when dataset was pretty small I tweaked it a little.
Standardization, Data is commonly rescaled to fall between -3 and 3, but actualy its mean is 0 and standard deviation 1. I had to perform standardization because of later PCA reduction which is sensitive for outlining data.   
First Linear Regression, for finding outliners, by performing variance realtive to this regressions and deleting records with variance higher than set.  
Second Linear Regresion this is the regression I use to predict Price
Mean square error, in short this is basicly the mean distance between points and regression. I calculate this for range that predicted value falls between.
