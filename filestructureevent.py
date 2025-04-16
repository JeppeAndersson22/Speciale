import os
import shutil

# Mapping of abbreviations to full team names
team_mapping = {
    "FCM": "FC Midtjylland",
    "HVI": "Hvidovre IF",
    "LBK": "Lyngby Boldklub",
    "FCK": "F.C. København",  # Fixed encoding issue
    "BIF": "Brøndby IF",
    "OB": "OB",
    "AGF": "AGF",
    "VFF": "Viborg FF",
    "RFC": "Randers FC",
    "ACH": "AC Horsens",
    "SIF": "Silkeborg IF",
    "VB": "Vejle Boldklub",
    "FCN": "FC Nordsjælland"
}

# Source and destination directories
source_matchfeeds = "C:/Users/jda\Desktop/data speciale/Event Data 2023-2024/Matchfeeds"
destination_base = "C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data"

# Loop through all folders in the destination
for team_folder in os.listdir(destination_base):
    team_folder_path = os.path.join(destination_base, team_folder)
    
    # Ensure it's a directory
    if os.path.isdir(team_folder_path):
        parts = team_folder.split("_")
        
        if len(parts) == 2:
            team1_abbr, team2_abbr = parts  # Extract team abbreviations
            
            # Convert abbreviations to full names
            team1_full = team_mapping.get(team1_abbr, team1_abbr)
            team2_full = team_mapping.get(team2_abbr, team2_abbr)
            
            # Loop through existing files in the folder to extract match dates
            for filename in os.listdir(team_folder_path):
                if filename.startswith("20") and "-" in filename:  # Match the format YYYYMMDD
                    match_id = filename.split("-")[0]  # Extract date (e.g., 20230721)
                    match_date = f"{match_id[:4]}-{match_id[4:6]}-{match_id[6:]}"  # Convert to YYYY-MM-DD
                    
                    # Construct expected Matchfeed folder name
                    matchfeed_folder_name = f"{match_date} {team1_full} - {team2_full}"
                    
                    # Search for the matching folder in Matchfeeds
                    matchfeed_path = os.path.join(source_matchfeeds, matchfeed_folder_name)
                    
                    if os.path.exists(matchfeed_path):
                        # Move all .xml files from the matchfeed folder
                        for file in os.listdir(matchfeed_path):
                            if file.endswith(".xml"):
                                source_path = os.path.join(matchfeed_path, file)
                                destination_path = os.path.join(team_folder_path, file)
                                
                                if not os.path.exists(destination_path):
                                    shutil.move(source_path, destination_path)
                                    print(f"Moved {file} -> {destination_path}")
                                else:
                                    print(f"Skipped {file}, already exists in {team_folder_path}")
                    else:
                        print(f"Matchfeed folder not found: {matchfeed_path}")
