import numpy as np

def idw(x):
    w = np.sum([[i[0]/i[1], 1.0/i[1]] for i in x], axis=0)
    return w[0]/w[1]

def find_nearest_point(point, pts, n=3):
	'''Find the nearest n points

	Parameters:
	point: Point,
		The point to be tested
	pts: gp.GeoDataFrame,
		A collection of points form which to 
		find the n nearest 
	n: int,
		Number of nearby points to use
	'''
	pts['dist'] = pts.apply(lambda x: point['geometry'].distance(x['geometry']), axis=1)
	return pts.iloc[pts['dist'].argsort()[:n]]

def calc_mean_pm25(point, stations, aq, time=0, n=3):
    '''Calculate the mean IDW PM25 value from nearby stations
    
    Parameters:
    ----------
    point : pd.Series,
        The point location for determining PM levels
    stations : pd.DataFrame,
        All possible nearby air quality monitoring stations
        that will be used to determine the local PM level
    aq : pd.DataFrame,
        Air quality measurements associated with each station
    n : int,
    	Number of stations to include in calculations
        
    Returns:
    -------
    pm25 : float,
        Computed PM value based on the IDW of nearby stations
    '''
    # -- Find the nearest stations
    near_by = find_nearest_point(point, stations, n)[['site_name', 'dist']]
    
    # -- Get AQ data from those stations
    nb = [[aq[i[0]][time], i[1]] for i in near_by.values]
    
    # -- Compute Inverse Weighted Distance
    pm25 = idw(nb)
    
    return pm25

def calc_pm25(x1, x2):
	'''Calculate PM25
	Parameters:
    ----------
	x1: np.float,
		The mean PM25 for nearby stations
	x2: np.int64,
		The number of boiler units within 1km buffer
	'''
	beta_0 = -1.45
	beta_1 = 1.08
	beta_2 = 0.0055
	pm25 = beta_0 + (beta_1*x1) + (beta_2*x2)
	return pm25    