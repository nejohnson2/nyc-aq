import glob
import numpy as np
import pandas as pd
import requests

from shapely.geometry import Point

def read_aq(fpath):

    data = []
    for i in glob.glob(fpath):
        df = pd.read_csv(i)
        data.append(df)

    data = pd.concat(data, axis=0) 

    data['timestamp'] = pd.to_datetime(data['Date(YYYY-MM-DD)'] + ' ' + data['Time (HH24:MI)'])
    data.index = data['timestamp']
    data = data.sort_index()
    data.drop(['timestamp','Date(YYYY-MM-DD)', 'Time (HH24:MI)'], axis=1, inplace=True)
    
    # clean up column names
    data.columns = data.columns.map(lambda x: " ".join(x.split(' ')[:-2]))    
    
    # remove some crazy outliers
    data['IS 52']['2015-02-05 13:00:00'] = np.nan
    data['IS 52']['2016-02-24 12:00:00'] = np.nan
    data['Port Richmond']['2007':'2010'] = np.nan
    
    return data

# build geometry
def create_geom(x):
    point = Point(x['longitude'],x['latitude'])
    return point

def read_stations_coords():
    site = 'https://data.ny.gov/resource/7i2s-kiup.json'
    
    # This list was created manually
    site_names = ['JHS 45', 'IS 143','PS 19','Division Street','CCNY','Morrisania II','IS 52'
            ,'IS 74', 'Pfizer Lab', 'PS 314', 'JHS 126', 'PS 274', 'Maspeth','Queens College'
            ,'Susan Wagner HS','Port Richmond', 'Fresh Kills West']
    
    # request data from api
    r = requests.get(site)
    # convert to dataframe
    df = pd.DataFrame(r.json())
    
    # subset based on the region
    df = df[df['region'] == '2']
    df['site_name'] = site_names
    
    # build geometry
    df.loc[:,'longitude'] = df['longitude'].astype(float)
    df.loc[:,'latitude'] = df['latitude'].astype(float)    
    df['geometry'] = df.apply(create_geom, axis=1) 
    
    return df[['site_name','latitude','longitude', 'geometry']]