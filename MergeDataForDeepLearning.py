import pandas as pd
from Trackingdata import loadTrackingData
from Eventdata import getEventData
from loadFiles import loadFiles
from ConvertToMatrices import ballCoordinates
import re
import os
# This script processes the event data and tracking data for matches, calculates ball coordinates, and saves the results to a CSV file.
result2 = pd.DataFrame()


folder_path = "C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/!Processed"
files_in_folder = os.listdir(folder_path)
df = pd.DataFrame()
for file in files_in_folder:
    parts = file.split('_')
    Home =  parts[0]
    Away = parts[1]       
    matched_files = loadFiles(Home, Away, "!Processed")
    metadata = matched_files["metadata"]
    rawdata = matched_files["raw"]
    additional_metadata =  matched_files["additionalMetaData"]
    f7 =  matched_files["f7"]
    f24 =  matched_files["f24"]
    match = re.search(r'(\d+)-eventdetails.xml$', f24)
    if match:
        # Extract the number from the match
        match_id = int(match.group(1))
        print(f"Extracted number: {match_id}")
    else:
        print("No match found")
    excel_file_path = f'SyncedExcel/{match_id}_{Home}_{Away}.xlsx'
    df = pd.read_excel(excel_file_path)
    df = df.dropna(subset=['matched_frames'])
    df['matched_frames'] = df['matched_frames'].astype(int)
    df_actions = getEventData(match_id, f7, f24, Home, Away)
    result_event = df.merge(df_actions, how='left', left_on='original_event_id', right_on='original_event_id')
    TrackingData = loadTrackingData(metadata, rawdata, additional_metadata)
    dfTrack = TrackingData.to_df()
    dfTrack['Id'] = range(len(dfTrack))
    result_df = result_event.merge(dfTrack, how='left', left_on='matched_frames', right_on='Id')
    result2 = pd.concat([result2, result_df], ignore_index=True)
    print (f"Processed {Home} vs {Away}")
    
    
result2 = result2[result2['type_name'].isin(['pass', 'cross'])]
result2 = ballCoordinates(result2)
result2["ball_owning_team_id"] = result2["ball_owning_team_id"].astype(int)
result2.to_csv('GrundspiltilModel.csv', index=False)


