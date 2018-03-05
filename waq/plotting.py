import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import griddata

def plot_contour(x, y, values, bounds, n=1000, s=1):

	xi = np.linspace(bounds['minx'], bounds['maxx'], n)
	yi = np.linspace(bounds['miny'], bounds['maxy'], n)
	grid_x, grid_y = np.meshgrid(xi, yi)

	points = np.array([x,y]).T
	f = LinearNDInterpolator(points, values)
	z = f(grid_x, grid_y)

	#levels = np.arange(np.min(z[~np.isnan(z)]), np.max(z[~np.isnan(z)]), s)

	plt.contourf(grid_x, grid_y, z, figsize=(10,10))