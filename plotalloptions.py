# %%
from Trackingdata import loadTrackingData
from Eventdata import getEventData
from loadFiles import loadFiles
import re
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# %%
#load from csv
import pandas as pd
#matched = pd.read_csv('Specialedatav2.csv')

# %%
Home = "AGF"
Away = "BIF"
path = "C:/Users/jda/Desktop/Speciale/data/!Processed"
matched_files = loadFiles(Home, Away, path)




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

# %%

df_actions = getEventData(match_id, f7, f24, Home, Away, path)

# %%
tracking = loadTrackingData(metadata, rawdata, additional_metadata)

# %%
#filtered_matched = matched[matched['original_event_id'] == 2590851523]
#print(filtered_matched)

frame_data = tracking.records[12304]
# Define the pitch
pitch = Pitch(pitch_type='opta')
fig, ax = pitch.draw(figsize=(10, 7))

# Extract player positions
teammate_locs = [data.coordinates for player, data in frame_data.players_data.items() if player.team == frame_data.ball_owning_team]
opponent_locs = [data.coordinates for player, data in frame_data.players_data.items() if player.team != frame_data.ball_owning_team]

# Convert to x, y coordinates
teammate_x = [p.x for p in teammate_locs]
teammate_y = [p.y for p in teammate_locs]
opponent_x = [p.x for p in opponent_locs]
opponent_y = [p.y for p in opponent_locs]

# Plot players
pitch.scatter(teammate_x, teammate_y, c='orange', s=80, edgecolors='black', label='Teammates', ax=ax)
pitch.scatter(opponent_x, opponent_y, c='blue', s=80, edgecolors='black', label='Opponents', ax=ax)


# Ball position
if frame_data.ball_coordinates:
    pitch.scatter(frame_data.ball_coordinates.x, frame_data.ball_coordinates.y, 
                c='red', s=100, edgecolors='black', label='Ball', ax=ax)

# Plot a specific pass event
df_pass_event = df_actions[df_actions["original_event_id"] == 2590869737]
if not df_pass_event.empty:
    if not df_pass_event.empty and df_pass_event.iloc[0].result_id == 1:
        color = 'green'
    else:
        color = 'red'
    pitch.arrows(df_pass_event.start_x, df_pass_event.start_y, df_pass_event.end_x, df_pass_event.end_y,
            color=color, width=2, ax=ax)

# Show the plot
plt.legend()
plt.show()