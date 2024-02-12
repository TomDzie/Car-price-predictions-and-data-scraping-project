# Data scraping and car price prediction  
1. [ Description. ](#desc)
2. [ How it works ](#works)
3. [ How it's build ](#build)

<a name="desc"></a>  
## 1. Description  

This project is about estimating users car value on market. Project startet with my interest in BMW 140i.
The point is that the prices where not consistant so it was really hard to estimate its market value. I came up with idea to reagularly scrape car advertising portal and make database out of scraped soup.
I started scraping with beautifullSoup everything was recorded regularly to SQLite database. Every offer came with its own id so every record in DB stayed unique.
I used to collect that data for some time and than I wanted to connect that topic with my Big Data university project. I had and idea to estimate regullar user's car value so it will be easier to post and sell it.
I implemented some machine learning techniques I learned on courses and other projects. This is what came out of it.


<a name="works"></a>  
## 2. How it works  

1. To predict prices we need some data so the first step is collecting a lot of data.  
   I used this program to scrape car sales portal every day. Every offer was saved to SQL database. At the end there were around 200 000 records. Collecting real data was time consuming and little bit tricky because everytime website change little bit my code must also change.
   ![image](https://github.com/TomDzie/Car-price-predictions-and-data-scraping-project/assets/117634603/3730604d-d37d-4aa1-908e-f48a89cc4521)

2. Selecting right data
   Next step is selecting unrelated parameters for further predictions and other actions.
   The program takes into account 9 parameters, some of them just to select the right model of car, and other to predict price

3. Preprocessing, quality indicators and prediction.
   Next selected data is preprocessed and price predistion is made

4.Users perspective
user types:  
![image](https://github.com/TomDzie/Car-price-predictions-and-data-scraping-project/assets/117634603/6fc1d241-54c3-434c-90fe-1b5a1837c5a8)   

Output:  
![image](https://github.com/TomDzie/Car-price-predictions-and-data-scraping-project/assets/117634603/9608a53c-22d5-417e-8b0a-7f9a54677cda)

![image](https://github.com/TomDzie/Car-price-predictions-and-data-scraping-project/assets/117634603/cca1b8af-72cb-49ee-9558-e17e3cc47b34)





<a name="build"></a>  
## 2. How it's build  

![image](https://github.com/TomDzie/Car-price-predictions-and-data-scraping-project/assets/117634603/e820ef2e-29e9-4f6c-a2a1-39418276b374)  

I start determining the price of the vehicle by regularly collecting data from the OtoMoto.pl advertising portal, where, using the Beautifull Soup library, I use the data scraping technique, i.e. data extraction from the website's HTML code. I save the pre-formatted data along with the ID to the SQLite database so that no records are repeated in the database. Then, based on the parameters entered by the user, I select the appropriate data and create the so-called data frame, in the next step I move on to data processing, where I first divide the data into test and training sets, standardize the data and then reject outlier data. I do this using preliminary linear regression, based on which data with variance greater than allowable is rejected. In the next stage, I fit a linear regression model to the ready training data and, using the mean square error from the training data, I calculate the possible price deviation from the more accurate prediction, i.e. the above-mentioned price ranges, and then I can now predict the value of the user's vehicle. Then, on the test data, I calculate the model fit measures, using a slightly modified R^2 measure for the data, where the square of the mean square error is subtracted from the squares of the distance between the regression and the actual value. Finally, I calculate the average mileage of the car for a given year, the percentage of cars with higher mileage and create graphs of the relationship between mileage, year and price, and in one of them I reduce mileage and year to one dimension using the PCA method to compare the data with the price on a 2D graph. This way, the user receives all the necessary information and data visualizations.

