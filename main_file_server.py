import data_analysis_server
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.ticker import LinearLocator

def get_link():
    ns5min=5*60*1e9
    
    end = pd.Timestamp("now", tz="UTC")
    end = pd.Timestamp(end.value//ns5min*ns5min) #round to nearest 5min
    
    start = end-pd.Timedelta(minutes=10)
    
    print start,end
    
    link = "http://109.237.25.161/particle/measurements?device={}&measurement={}&start_date={}&end_date={}".format("{}","{}",start,end)

    return link

def main():
    
    link = get_link()
    
    kitchen = data_analysis_server.main(room="kitchen",api_link=link)
    living_room = data_analysis_server.main(room="living_room",api_link=link)
    
    execfile("parse_csvs.py")

if __name__ == '__main__':
    main()