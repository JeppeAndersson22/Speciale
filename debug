import os
import tqdm
import pandas as pd
import numpy as np
#%load_ext autoreload
#%autoreload 2
import socceraction.spadl as spadl
import socceraction.vaep.features as fs
import socceraction.xthreat as xthreat
import matplotsoccer as mps
from scipy.interpolate import RectBivariateSpline
import socceraction.spadl.config as spadlconfig



file_path = r"C:\Users\jda\Desktop\Speciale\alleactions.csv"
data = pd.read_csv(file_path)
data2 = data.dropna(subset=['end_x'])


xTModel = xthreat.ExpectedThreat(l=16, w=12)
xTModel.fit(data2)

xTModel.save_model("xTmodelv2.pkl")

# Inspect the learned heatmap
mps.heatmap(xTModel.xT, cmap="hot", linecolor="white", cbar="True")

# Create the interpolator manually
cell_length = spadlconfig.field_length / xTModel.xT.shape[1]
cell_width = spadlconfig.field_width / xTModel.xT.shape[0]
x = np.arange(0.0, spadlconfig.field_length, cell_length) + 0.5 * cell_length
y = np.arange(0.0, spadlconfig.field_width, cell_width) + 0.5 * cell_width

# Use RectBivariateSpline instead of interp2d
interp = RectBivariateSpline(y, x, xTModel.xT)

# Generate fine-grid values
x_fine = np.linspace(0, 100, 1000)
y_fine = np.linspace(0, 100, 1000)
X, Y = np.meshgrid(x_fine, y_fine)

# Plot interpolated heatmap
mps.heatmap(interp(y_fine, x_fine), cmap="hot", linecolor="white", cbar="True")
