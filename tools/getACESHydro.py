from selenium import webdriver
import pandas as pd
from sys import argv
from datetime import datetime

ACES_URL = "https://www.aspennature.org/ecological-data/stream-gauge"
DATA_CMD = 'return Drupal.settings.acesHydro.dischargeData'
datefmt = "%Y%m%d"
alltime = False

if (len(argv) == 1):
    print("Returning all time from ACES hydrograph.")
    alltime =True
elif (len(argv) != 3):
    print("usage: <start YYYYMMDD> <end YYYYMMDD>")
else:
    startDate = datetime.strptime(argv[1], datefmt)
    endDate = datetime.strptime(argv[2], datefmt)
    print("Start Date:%s, End Date: %s"%(startDate, endDate))


drv = webdriver.Chrome()
drv.get(ACES_URL)
data = drv.execute_script(DATA_CMD)
drv.close()

data = pd.DataFrame(data)
data.columns = ['time', 'discharge']
data = data.set_index(pd.to_datetime(data['time']/1000, unit='s'))
data.drop('time', axis=1, inplace=True)

if not alltime: 
    data = data[(data.index >= startDate) & (data.index <= endDate)].head()

lastTime = datetime.strftime(data.index[-1], "%Y%m%d")

data.to_csv("ACESdata_%s.csv"%lastTime)
