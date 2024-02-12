import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as sq
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import KernelPCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.covariance import EllipticEnvelope
import seaborn as sns
import heapq


class price_pred:

    def __init__(self):
        self.car = dict        #User's car parameters
        self.x_val = list      #user's car year and mileage
        self.scaler = None     #Standard scaller
        self.x_sql = None      #raw x data from sql
        self.y_sql = None      #raw y data from sql
        self.x_scaled = None   #scalled x data
        self.x_wo_outliers = None   #scalled x data without outliers
        self.y_wo_outliers = None   #data without outliers
        self.predictor = None       #predictor
        self.y_predicted = None     #estimated value of User's car
        self.sql_code = None        #sql code
        self.X_test = None
        self.Y_test = None
        self.Y_test_predicted = None
        self.mean_square_error = None
        
    @classmethod
    def select_data(self, brand, model, generation, year, mileage, power, fuel, damaged, transmition = None, country_of_origin = None):

        self.car = {
        "Marka pojazdu": [brand],
        "Model pojazdu": [model],
        "Generacja": [generation],
        "Rok produkcji": [year],
        "Przebieg": [mileage],
        "Moc": [power],
        "Rodzaj paliwa": [fuel],
        "Skrzynia biegow": [transmition],
        "Kraj pochodzenia": [country_of_origin],
        "Uszkodzony": [damaged]
        }
        select = ''
        where = ''

        con = sq.connect(f'C:\\Users\\tom19\VScode_Projects\\OTOmoto_project\\SQLite_databases\\BMW')
        cur = con.cursor()

        for i in self.car:
            if self.car[i][0] != None and i in ["Przebieg", "Rok produkcji"]:
                select += f'"{i}",'
        select += f'"Price"'

        where += f""""Model pojazdu" LIKE '{self.car["Model pojazdu"][0]}' AND"""
        where += f""""Generacja" LIKE '%{self.car["Generacja"][0]}%' AND"""
        where += f""""Rodzaj paliwa" LIKE '%{self.car["Rodzaj paliwa"][0]}%' AND"""
        if self.car["Kraj pochodzenia"][0] != None:
            where += f""""Kraj pochodzenia" LIKE '%{self.car["Kraj pochodzenia"][0]}%' AND"""
        if self.car["Skrzynia biegow"][0] != None:
            where += f""""Skrzynia biegow" LIKE '%{self.car["Skrzynia biegow"][0]}%' AND"""
        if self.car["Uszkodzony"][0] != 'Tak':
            where += f""""Uszkodzony" NOT LIKE 'Tak' AND """
        where += f""""Moc" == {self.car["Moc"][0]} AND"""
        where = where[:-3]
        
        self.sql_code = f"""SELECT {select} FROM {brand} 
        WHERE {where}"""

        df = pd.read_sql(self.sql_code, con)

        self.x_sql = df.iloc[:, :-1].values
        self.y_sql = df.iloc[:, -1].values
        return(df)
    
    @classmethod
    def preprocessing(self, residual_std = True):      #add test size variable
        x = self.x_sql
        y = self.y_sql
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
        x= x_train
        y= y_train
        self.scaler = StandardScaler()
        x = self.scaler.fit_transform(x)
        self.X_test = self.scaler.transform(x_test)
        self.Y_test = y_test
        self.x_val = self.scaler.transform(np.array([self.car["Rok produkcji"][0], self.car["Przebieg"][0]]).reshape(-1,2))
        self.x_scalled = x
        self.y_wo_outliers = y
        self.x_wo_outliers = x
        

        if residual_std == True:

            lin_reg = LinearRegression()
            lin_reg.fit(x, y)
            y_pred = lin_reg.predict(x)

            y_test_pred = lin_reg.predict(self.X_test)
        
            residuals = (y - y_pred).reshape(-1,1)
            detector = EllipticEnvelope()
            detector.fit(residuals)
            outliers = detector.predict(residuals) == -1
            self.x_wo_outliers = x[~outliers, :]
            self.y_wo_outliers = y[~outliers]

            residuals = (self.Y_test - y_test_pred).reshape(-1,1)
            detector = EllipticEnvelope()
            detector.fit(residuals)
            outliers = detector.predict(residuals) == -1
            self.X_test = self.X_test[~outliers, :]
            self.Y_test = self.Y_test[~outliers]
    

        return f'preprocessed {len(self.y_sql)} rows'
        
    

    @classmethod
    def prediction(self, mean_sq=True, min_max_mean= False):
        self.predictor = LinearRegression()
        self.predictor.fit(self.x_wo_outliers, self.y_wo_outliers)
        y_pred = self.predictor.predict(self.x_wo_outliers)
        pred_price = self.predictor.predict(self.x_val).round(0)
        self.y_predicted = pred_price
        self.Y_test_predicted = self.predictor.predict(self.X_test)
        
        # min_ = self.car['Przebieg'][0]*0.8
        # max_ = self.car['Przebieg'][0]*1.2
        # max_bound = self.scaler.transform(np.array([self.car['Rok produkcji'][0], max_]).reshape(-1,2))[:,1]
        # min_bound = self.scaler.transform(np.array([self.car['Rok produkcji'][0], min_]).reshape(-1,2))[:,1]
        # car_arr = self.scaler.transform(np.array([self.car['Rok produkcji'][0], self.car['Przebieg'][0]]).reshape(-1,2))

        # right_year = np.array(list(map(lambda x: x != car_arr[:,0], self.x_wo_outliers[:,0]))).reshape(-1,)
        # data1 = self.y_wo_outliers[~right_year]
        # data = self.x_wo_outliers[~right_year,:]
        # between_mileage = np.array(list(map(lambda x: max_bound <= x, data[:,1]))).reshape(-1,)
        # data = data[~between_mileage]
        # data1 = data1[~between_mileage]
        # between_mileage = np.array(list(map(lambda x: min_bound >= x, data[:,1]))).reshape(-1,)
        # data = data[~between_mileage]
        # data1 = data1[~between_mileage]
        # n = int(len(data1)*0.3)
        # mean_max = round(np.mean(heapq.nlargest(n, data1)),0)
        # mean_min = round(np.mean(heapq.nsmallest(n, data1)),0)

        mn_err = mean_absolute_error(y_pred, self.y_wo_outliers).round(0)
        self.mean_square_error = mn_err

        if mean_sq==True:
            print(f'Estimated value of your car is {pred_price[0]} PLN with a margin of {mn_err} PLN')
        
        # if min_max_mean == True:
        #     print(f'Estimated value of your car is {pred_price[0]} PLN, price fluctuates between {mean_min} and {mean_max} PLN')

    @classmethod 
    def quality_indicator(self,):
        indicator = r2_score(self.Y_test, self.Y_test_predicted)
        avg = sum(self.Y_test)/(len(self.Y_test))
        SStot = sum((self.Y_test-avg)**2)
        SSres = sum(((self.Y_test - self.Y_test_predicted))**2-self.mean_square_error**2)
        R_2 = 1-SSres/SStot
        adj_R = 1-(1-indicator)*(len(self.Y_test)-1)/(len(self.Y_test)-self.X_test.shape[1]-1)
        print(R_2)

    @classmethod
    def car_against_others(self):
        year = self.car['Rok produkcji'][0]
        right_year = np.array(list(map(lambda x: x == self.car['Rok produkcji'], self.x_sql[:,0]))).reshape(-1,)
        data = self.x_sql[~right_year, :]
        more_mileage = sum(map(lambda x: x > self.car['Przebieg'], data[:,1]))/len(data[:,1])
        more_mileage = round(more_mileage[0] * 100, 2)
        year = self.car['Rok produkcji']
        mean_mileage = int(round(np.mean(data[:, 1]),0))
        print(f'mean mileage of model form {year[0]} is {mean_mileage} km')
        print(f'{more_mileage}% cars form {year[0]} have more mileage than yours')
        return more_mileage
        
        


    @classmethod
    def visualisation(self):
        lin_reg = LinearRegression()        
        pca = KernelPCA(n_components=1, kernel='linear')
        x_tran = pca.fit_transform(self.x_wo_outliers)
        x_set = pca.transform(self.x_val)
        lin_reg.fit(x_tran, self.y_wo_outliers)
        x_inverse = self.scaler.inverse_transform(self.x_wo_outliers.reshape(-1,2))
        x_val_inverse = self.scaler.inverse_transform(self.x_val.reshape(-1,2))

    

        ax1 = plt.subplot(221)
        ax1.scatter(x_inverse[:, 0], self.y_wo_outliers, color='#F07C25', alpha=0.6)
        ax1.scatter(x_val_inverse[:, 0], self.y_predicted, color='red')
        ax1.set_xlabel("Year", color='#F8510C')
        ax1.set_ylabel("Price", color='#F8510C')
        ax1.grid()

        ax2 = plt.subplot(222)
        ax2.scatter(x_inverse[:, 1], self.y_wo_outliers, color='#F07C25', alpha=0.6)
        ax2.scatter(x_val_inverse[:, 1], self.y_predicted, color='red')
        ax2.set_xlabel("Mileage", color='#F8510C')
        ax2.set_ylabel("Price", color='#F8510C')
        ax2.grid()

        ax3 = plt.subplot(212)
        ax3.scatter(x_tran, self.y_wo_outliers, color='#F07C25', alpha=0.6)
        ax3.scatter(x_set, self.y_predicted, color='red')
        ax3.plot(range(-4,5), lin_reg.predict(np.array(range(-4,5)).reshape(-1,1)), )
        ax3.set_xlabel("Pca transformation", color='#F8510C')
        ax3.set_ylabel("Price", color='#F8510C')
        ax3.grid()

        plt.show()        

    def pdf_raport(direction):
        pass


bmw = price_pred()
# price_pred.select_data(brand = 'BMW', model= "Seria 1", generation = "F20", year=2015,  mileage=150_000, power= 136, fuel='Benzyna', damaged='Nie')
price_pred.select_data(brand = 'Alfa', model= "Giulietta", generation="0",
                        year=2018,  mileage=180_000, power= 170, fuel='Benzyna', damaged='Nie')

price_pred.preprocessing(residual_std= True)
price_pred.prediction(min_max_mean=True)
price_pred.car_against_others()
price_pred.quality_indicator()
price_pred.visualisation()


