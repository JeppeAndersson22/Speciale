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

file_path = r"C:\Users\jda\Desktop\Speciale\xtmodelv2.pkl"
xTModel = xthreat.load_model(file_path)

action_path = r"C:\Users\jda\Desktop\Speciale\alleactionsv2.csv"
df = pd.read_csv(action_path)
#drop where end_x is NaN
df = df.dropna(subset=['end_x'])
#only keep where type_name = 'pass' 
df = df[df["type_name"].isin(["pass", "cross"])]


df["xT_succ"] = xTModel.rate(df)
df["xT_succ"] = df["xT_succ"].apply(lambda x: max(x, 0))

df_unsuccess = df.copy()
df_unsuccess["end_x"] = 100-df_unsuccess["end_x"]
df_unsuccess["end_y"] = 100-df_unsuccess["end_y"]
df["xT_unsucc"] = xTModel.rateunsuc(df_unsuccess)

#merge xt_succ and xt_unsucc into xt, take the value that is not nan
df["xT"] = df["xT_succ"].combine_first(df["xT_unsucc"])

result = df[["original_event_id", "xT", "xT_succ", "xT_unsucc", "team_name", "player_name", "start_x", "start_y", "end_x", "end_y"]]
result.to_csv(r"C:\Users\jda\Desktop\Speciale\xtdata.csv", index=False)
