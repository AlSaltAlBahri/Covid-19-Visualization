import requests
import json
import matplotlib.pyplot as plt
import pandas as pd


def fetchData():
    """
    fetches data from API and returns a 2D list 
    of date and confirmed cases [(date,cases)]
    """
    dayCases = 0
    oldCases = 0
    newCases = 0
    data = requests.get('https://albahri.pythonanywhere.com/statsbydate')
    data = json.loads(data.text)
    mylist = list()
    for entry in data:
        oldCases = dayCases
        dayCases = entry["confirmed"]
        newCases = dayCases - oldCases
        mylist.append([entry["date"], newCases])
    return mylist


def createDf(mylist):
    """
    creates pandas DataFrame
    """
    df = pd.DataFrame(mylist)
    df[0] = pd.to_datetime(df[0])
    df.rename(columns = {0:'Date'}, inplace = True)
    df.rename(columns = {1:'Cases'}, inplace = True)
    df = df.set_index('Date')
    df['5 days'] = df['Cases'].rolling(5).mean()
    df['10 days'] = df['Cases'].rolling(10).mean()
    df[['Cases','5 days','10 days']].plot()
    return df

def plot(df):
    """
    plots df 
    """
    plt.grid(True)
    plt.title("Moving Averages: Oman Covid 19 Cases")
    plt.axis('tight')
    plt.ylabel('Confirmed New Cases')
    plt.show()

def main():
    dataList = fetchData()
    df = createDf(dataList)
    plot(df)


if __name__ == "__main__":
    main()


    
