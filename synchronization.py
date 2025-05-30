import pandas as pd
from etsy.sync import EventTrackingSynchronizer
from Trackingdata import getTrackingdata
from Eventdata import getEventData
from loadFiles import loadFiles
import re
import os
import shutil
from datetime import datetime


folder_path = "C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data"
log_path = "C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/!Log"
files_in_folder = os.listdir(folder_path)
log_entries = []
df = pd.DataFrame()
for file in files_in_folder:
    if "!" not in file:
        try:     
            parts = file.split('_')
            Home =  parts[0]
            Away = parts[1]                
            matched_files = loadFiles(Home, Away)
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
            
            df_tracking = getTrackingdata(metadata, rawdata, additional_metadata)
            df_actions = getEventData(match_id, f7, f24, Home, Away)
            syncer = EventTrackingSynchronizer(events=df_actions, tracking=df_tracking, fps=25, kickoff_time=5)
            syncer.synchronize()
            matched_frames_series = syncer.matched_frames.rename("matched_frames")
            scores_series = syncer.scores.rename("scores")
            event_id = syncer.events["original_event_id"]
            team_id = syncer.events["team_id"]
            period_id = syncer.events["period_id"]
            # Combine into a DataFrame
            df = pd.concat([event_id,team_id,period_id, matched_frames_series, scores_series], axis=1)
            df = df.fillna("N/A")
            # Save to Excel
            output_path = f"C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/SyncedExcel/!Slutspil/{match_id}_{Home}_{Away}.xlsx"
            df.to_excel(output_path, index=True, engine="openpyxl")
            
            #Move folder to !Processed
            source = f"C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/{file}"
            source_path = os.path.join(source)
            destination = "C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/!Processed/!Slutspil"
            destination_path = os.path.join(destination)
            shutil.move(source_path, destination_path)
            print(f"{match_id}: Successfully processed")
        except Exception as e:
            log_entries.append(f"[{datetime.now()}] Error processing {file}: {e}")
            source = f"C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/{file}"
            source_path = os.path.join(source)
            destination = "C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/!Failed"
            destination_path = os.path.join(destination)
            shutil.move(source_path, destination_path)
            continue

if log_entries:  # Only create log file if there are errors
    log_file_path = os.path.join(log_path, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
    with open(log_file_path, "w") as log_file:
        for entry in log_entries:
            log_file.write(entry + "\n")
