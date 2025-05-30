import pandas as pd
import numpy as np
import socceraction.xthreat as xthreat

#This script calculates the xT success for all passes and crosses.

xTModel = xthreat.load_model('xtmodelv2.pkl')
df = pd.read_csv('alleactionsv2.csv')
intentedend = pd.read_csv('IntentedEnd.csv')
intentedend["end_x1"] = intentedend["end_x"].copy()
intentedend["end_y1"] = intentedend["end_y"].copy()
df = df[df["original_event_id"].isin(intentedend["original_event_id"])]
#left join the two dataframes on original_event_id
df = df.merge(intentedend[['original_event_id', 'end_x1', 'end_y1']], on='original_event_id', how='left')
#drop where end_x is NaN
df = df.dropna(subset=['end_x'])
#only keep where type_name = 'pass' 
df = df[df["type_name"].isin(["pass", "cross"])]

#replace end_x and end_y with inteded_x and inteded_y
df['end_x'] = df['end_x1']
df['end_y'] = df['end_y1']
#remove columns inteded_x and inteded_y
df["xT_succ"] = xTModel.rate(df)
df["xT_succ"] = df["xT_succ"].apply(lambda x: max(x, 0))

result = df[["original_event_id", "xT_succ", "team_name", "player_name", "start_x", "start_y", "end_x", "end_y"]]
result.to_csv(r"C:\Users\jda\Desktop\Speciale\xtdatasucc.csv", index=False)
