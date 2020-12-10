# -*- coding: utf-8 -*-
# Problem Set 5: Modeling Temperature Change
# Name: Gyalpo M. Dongo Aguirre
# Collaborators:
# Time: 5:00

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2000)
TESTING_INTERVAL = range(2000, 2017)

##########################
#    Begin helper code   #
##########################

def standard_error_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]


class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_daily_temps(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_temp_on_date(self, city, month, day, year):
        """
        Get the temperature for the given city at the specified date.

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified date and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

##########################
#    End helper code     #
##########################

    def get_yearly_averages(self, cities, years):
        """
        For each year in the given range of years, computes the average of the
        annual temperatures in the given cities.

        Args:
            cities: a list of the names of cities to include in the average
                annual temperature calculation
            years: a list of years to evaluate the average annual temperatures at

        Returns:
            a 1-d numpy array of floats with length = len(years). Each element in
            this array corresponds to the average annual temperature over the given
            cities for a given year.
        """

        # NOTE: TO BE IMPLEMENTED IN PART 4B OF THE PSET
        annual_average = []
        for year in years:
            temps = []
            for city in cities:
                temps.append(self.get_daily_temps(city, year))
            temps = np.append(temps[0],temps[1:])
            annual_average.append(temps.mean())
        return np.array(annual_average)            
def linear_regression(x, y):
    """
    Calculates a linear regression model for the set of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points

    Returns:
        (m, b): A tuple containing the slope and y-intercept of the regression line,
                both of which are floats.
    """
    
    m = (((x-x.mean())*(y-y.mean())).sum())/((x - x.mean())**2).sum()
    b = y.mean() - m*x.mean()
    return (m,b)
def squared_error(x, y, m, b):
    '''
    Calculates the squared error of the linear regression model given the set
    of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        m: The slope of the regression line
        b: The y-intercept of the regression line


    Returns:
        a float for the total squared error of the regression evaluated on the
        data set
    '''
    est_y = m*x + b
    return ((y-est_y)**2).sum()
def generate_models(x, y, degrees):
    """
    Generates a list of polynomial regression models with degrees specified by
    degrees for the given set of data points

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degrees: a list of integers that correspond to the degree of each polynomial
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d numpy array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for deg in degrees:
        model = np.polyfit(x,y,deg)
        models.append(model)
    return models
def evaluate_models(x, y, models, display_graphs=False):
    """
    For each regression model, compute the R-squared value for this model and
    if display_graphs is True, plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (i.e. the model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        Degree of your regression model,
        R-squared of your model evaluated on the given data points,
        and standard error/slope (if this model is linear).

    R-squared and standard error/slope should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the R-squared value for each model
    """
    r_list = []
    counter = 0
    for model in models:
        counter +=1
        est_y = np.polyval(model,x)
        r_squared = round(r2_score(y,est_y),4)
        r_list.append(r_squared)
        degree = len(model) - 1
        #Degree is this because e.g. a model of a quadratic has a,b and c
        #as coefficients, so its length is 3, therefore its order is 3-1 = 2
        if display_graphs:
            plt.figure(counter)
            plt.plot(x,y,'bo', label = 'Data')
            plt.plot(x,est_y,'r',linestyle='solid',label = "Best fit")
            plt.xlabel('Years')
            plt.ylabel('Degrees Celsius')
            plt.legend(loc = 'best')
            if degree == 1:
                se_over_slope = round(standard_error_over_slope(x,y,est_y,model),4)
                plt.title("Degree of regression model: " + str(degree) + "\n" + "R-squared of model: " + str(r_squared) + "\n" + "Standard error over slope: " + str(se_over_slope))
            else:
                plt.title("Degree of regression model: " + str(degree) + "\n" + "R-squared of model: " + str(r_squared))
            plt.show()
    return r_list

def find_extreme_trend(x, y, length, positive_slope):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j, m) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope m, with the sign specified by positive_slope and j-i = length.

        In the case of a tie, it returns the first interval. For example,
        if the intervals (2,5) and (8,11) both have slope 3.1, (2,5,3.1) should be returned.

        If no intervals matching the length and sign specified by positive_slope
        exist in the dataset then return None
    """
    slopes = {}
    for i in range(len(x)):
        if i == len(x) - length + 1:
            break
        else:
            m = linear_regression(x[i:i+length],y[i:i+length])[0]
            slopes[(i,i+length)] = m
    possible_slopes = {}
    for slope in slopes:
        if positive_slope:
            if slopes[slope] > 0:
                possible_slopes[slope] = slopes[slope]
        else:
            if slopes[slope] < 0:
                possible_slopes[slope] = slopes[slope]
    if len(possible_slopes) > 0:
        max_interval = max(possible_slopes, key=lambda y: abs(possible_slopes[y]))
        possible_intervals = [max_interval]
        for slope in possible_slopes:
            if abs(possible_slopes[max_interval] - possible_slopes[slope]) <= 1e-8:
                possible_intervals.append(slope)
        possible_intervals = sorted(list(set(possible_intervals)))
        max_interval = possible_intervals[0]
        result = list(max_interval)
        result.append(possible_slopes[max_interval])
        return tuple(result)
    else:
        return None
    




def find_all_extreme_trends(x, y):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        
    Returns:
        a list of tuples of the form (i,j,m) such that the application of linear
        regression to the data in x[i:j], y[i:j] produces the most extreme
        positive OR negative slope m, and j-i=length. 

        The returned list should have len(x) - 1 tuples, with each tuple representing the
        most extreme slope and associated interval for all interval lengths 2 through len(x).
        If there is no positive or negative slope in a given interval length L (m=0 for all
        intervals of length L), the tuple should be of the form (0,L,None).

        The returned list should be ordered by increasing interval length. For example, the first 
        tuple should be for interval length 2, the second should be for interval length 3, and so on.

        If len(x) < 2, return an empty list
    """
    if len(x) < 2:
        return []
    else:
        trends = []
        for length in range(2,len(x) + 1):
            pos_trend = find_extreme_trend(x,y,length,True)
            neg_trend = find_extreme_trend(x,y,length,False)
            if neg_trend == None:
                trends.append(pos_trend)
            elif pos_trend == None:
                trends.append(neg_trend)
            else:
                if abs(abs(neg_trend[2])- pos_trend[2]) <= 1e-8:
                    if pos_trend[0] > neg_trend[0]:
                        trends.append(neg_trend)
                    else:
                        trends.append(pos_trend)
                elif abs(neg_trend[2]) > pos_trend[2]:
                    trends.append(neg_trend)
                else:
                    trends.append(pos_trend)
        return trends

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    sum_squared = ((y - estimated)**2).sum()
    return (sum_squared/len(y))**0.5


def evaluate_models_testing(x, y, models, display_graphs=False):
    """
    For each regression model, compute the RMSE for this model and if
    display_graphs is True, plot the test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    RMSE should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N test data sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N test data sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the RMSE value for each model
    """
    rmse_list = []
    counter = 0
    for model in models:
        counter +=1
        est_y = np.polyval(model,x)
        root_mse = round(rmse(y,est_y),4)
        rmse_list.append(root_mse)
        degree = len(model) - 1
        if display_graphs:
            plt.figure(counter)
            plt.plot(x,y,'bo', label = 'Data')
            plt.plot(x,est_y,'r',linestyle='solid',label = "Best fit")
            plt.xlabel('Years')
            plt.ylabel('Degrees Celsius')
            plt.legend(loc = 'best')
            plt.title("Degree of regression model: " + str(degree) + "\n" + "Rmse of model: " + str(root_mse))
            plt.show()
    return rmse_list



if __name__ == '__main__':
    pass
    ##################################################################################
    # Problem 4A: DAILY TEMPERATURE
    dataset = Dataset('data.csv')
    x = np.array(range(1961,2017))
    y_daily = []
    for year in x:
        y_daily.append(dataset.get_temp_on_date('SAN FRANCISCO',12,25,year))
    y_daily = np.array(y_daily)
    degrees = [1]
    models_daily = generate_models(x,y_daily,degrees)
    four_a = evaluate_models(x,y_daily,models_daily,display_graphs = False)
    

    # ##################################################################################
    # # Problem 4B: ANNUAL TEMPERATURE
    y_yearly = dataset.get_yearly_averages(['SAN FRANCISCO'], x)
    models_yearly = generate_models(x,y_yearly,degrees)
    four_b = evaluate_models(x,y_yearly,models_yearly,display_graphs = False)
    ##################################################################################
    # Problem 5B: INCREASING TRENDS
    y_tampa = dataset.get_yearly_averages(['TAMPA'], x)
    interval_pos = find_extreme_trend(x,y_tampa,30,True)
    model_tampa_b = generate_models(x[interval_pos[0]:interval_pos[1]+1],y_tampa[interval_pos[0]:interval_pos[1]+1],degrees)
    five_b = evaluate_models(x[interval_pos[0]:interval_pos[1]+1],y_tampa[interval_pos[0]:interval_pos[1]+1],model_tampa_b,display_graphs = False)
    
    ##################################################################################
    # Problem 5C: DECREASING TRENDS
    interval_neg = find_extreme_trend(x,y_tampa,15,False)
    model_tampa_c = generate_models(x[interval_neg[0]:interval_neg[1]+1],y_tampa[interval_neg[0]:interval_neg[1]+1],degrees)
    five_c = evaluate_models(x[interval_neg[0]:interval_neg[1]+1],y_tampa[interval_neg[0]:interval_neg[1]+1],model_tampa_c,display_graphs = False)
    
    ##################################################################################
    # Problem 5D: ALL EXTREME TRENDS
    five_d = find_all_extreme_trends(x, y_tampa)
    ##################################################################################
    # Problem 6B: PREDICTING
    training_set = dataset.get_yearly_averages(CITIES,TRAINING_INTERVAL)
    degrees_train_test = [2,10]
    training_models = generate_models(TRAINING_INTERVAL,training_set,degrees_train_test)
    six_b_i = evaluate_models(TRAINING_INTERVAL, training_set, training_models,display_graphs = False)
    test_set = dataset.get_yearly_averages(CITIES,TESTING_INTERVAL)
    testing_models = generate_models(TESTING_INTERVAL,test_set,degrees_train_test)
    six_b_ii = evaluate_models_testing(TESTING_INTERVAL,test_set,testing_models,False)
    ##################################################################################
