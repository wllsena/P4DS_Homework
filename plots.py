import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analyze import analyze 
from sklearn import linear_model, preprocessing
def remove_outliers(data):
    m = 2
    while True:
        noout = data[abs(data - np.mean(data)) < m * np.std(data)].dropna()
        if data.shape[0] <= 40/39*noout.shape[0]:
            break
        m += 1
    return noout
    
def scatter(data, year, indexes, plot=True):
    '''Generates scatter plot and trend line or the r squared, coefficient and number of countries (plot=False) in comparison between two indexes (list of strs) in a given year (int)'''
    
    if type(year) == int:
        df = analyze(data, year)[indexes].dropna()
    else:
        df = analyze(data, year[0])[[indexes[0]]].join(analyze(data, year[1])[indexes[1]]).dropna()
    
    df = np.array(remove_outliers(df))
    x = df[:,0].reshape(-1, 1)
    y = df[:,1].reshape(-1, 1)
    xlist = [(x, "x"), (np.log(x), "log(x)")] if x.min() > 0 else [(x, "x")]
    ylist = [(y, "y"), (np.log(y), "log(y)")] if y.min() > 0 else [(y, "y")]
    r2 = 0
    for i in xlist:
        for k in ylist:
            modeltest = linear_model.LinearRegression().fit(i[0], k[0])
            r2test = modeltest.score(i[0], k[0])
            if r2test > r2:
                x, y = i[0], k[0]
                leix, leiy = i[1], k[1]
                model, r2 = modeltest, r2test
                    
    if plot:
        plt.plot(x, model.predict(x), color='red', linewidth=2.)
        plt.scatter(x, y, color='blue', s=50, alpha=.5)
        plt.legend(["R**2 = {:0.4}".format(r2)])
        plt.title('Tendency line {} - {}'.format(leix, leiy))
        plt.xlabel(indexes[0])
        plt.ylabel(indexes[1])
        plt.show()
        
    else:
        return r2, model.coef_[0][0], len(x)
    
def trend(data, country, index, years):
    '''Generates the trend over the years (list of ints) of the countries (list of strs) and requested index (str)'''
    
    for i in country:
        plt.plot(analyze(data, "c-"+i)[index].loc[[str(i) for i in range(years[0], years[1]+1)]])
    plt.legend(country)
    plt.title('Tendency')
    plt.setp(plt.xticks()[1], rotation=60)
    plt.xlabel('Years')
    plt.ylabel(index)
    plt.show()
    
def lmh(data, year, index, x):
    '''Generates the x (int) smaller, middle and higher values for the indicated year (int) and index (str)'''
    
    df = analyze(data, year).drop("World", 0)[index].dropna().sort_values()
    amount = int(len(df)/2)-int(x/2)
    df.iloc[list(range(0,x))+list(range(amount, amount+x))+list(range(-x,0))].plot(kind="bar")
    plt.title('Bar plot')
    plt.xlabel('Country')
    plt.ylabel(index)
    plt.show()
    
def trend_years(data, country, indexes, years, plot=True):
    '''Generates the trend line or the r squared, coefficient and number of countries (plot=False) of the years (list of ints) of the country (str) and the requested index (str)'''
    
    if type(indexes) == str:
        df = analyze(data, "c-"+country)[indexes].loc[[str(i) for i in range(years[0], years[1]+1)]].dropna()
        x = np.array(df.index, dtype="float64").reshape(-1, 1)
        y = preprocessing.MinMaxScaler().fit_transform(np.array(df.values, dtype="float64").reshape(-1, 1))
        model = linear_model.LinearRegression().fit(x, y)
        if plot:
            plt.plot(df.index, model.predict(x), color='red', linewidth=2.)
            plt.plot(df.index, y)
            plt.legend(["R**2 = {:0.4}".format(model.score(x, y)), "Coef = {:0.4}".format(model.coef_[0][0])])
            plt.title('Tendency line')
            plt.setp(plt.xticks()[1], rotation=60)
            plt.xlabel('Years')
            plt.ylabel(indexes)
            plt.show()

        else:
            return model.score(x, y), model.coef_[0][0], len(x)
    else:
        df = analyze(data, "c-"+country)[indexes].loc[[str(i) for i in range(years[0], years[1]+1)]].dropna()
        for ind in indexes:
            plt.plot(df.index, preprocessing.MinMaxScaler().fit_transform(np.array(df[ind], dtype="float64").reshape(-1, 1)))
        plt.legend(indexes)
        plt.setp(plt.xticks()[1], rotation=60)
        plt.show() 
        
def comparison_filter(data, year=2014, years=[2000,2014], country="World", index='GDP per capita (current US$)', r2=0.45, coef=0.05, num=10):
    '''Generates index graphs that match the index and criteria provided'''
    
    indcoef = trend_years(data, country, index, years, False)[1]
    for ind in analyze(data, year).columns.drop(index):
        try:
            isc = scatter(data, year, [index]+[ind], False)
            itr = trend_years(data, country, ind, years, False)[1]
            if isc[0] >= r2 and abs(itr-indcoef) <= coef and isc[2] >= num:
                print(index + " and " + ind)
                scatter(data, year, [index]+[ind])
                trend_years(data, country, [index]+[ind], years)
        except:
            pass