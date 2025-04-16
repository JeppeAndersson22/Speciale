from mplsoccer import Pitch, FontManager, Sbopen
import matplotlib.pyplot as plt
import pandas as pd
from kloppy.domain import TrackingDataset


def plotSyncedFrames(tracking_dataset: TrackingDataset, event_dataset: pd.DataFrame, frame_idx: int, eventID: int) -> None:
    tracking_dataset = tracking_dataset
    frame_data = tracking_dataset.records[frame_idx]
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
    df_pass_event = event_dataset[event_dataset["original_event_id"] == eventID]
    if not df_pass_event.empty:
        pitch.scatter(df_pass_event.start_x, df_pass_event.start_y, 
                    c='red', marker = 'x', s=100, label='Pass Event', ax=ax)

    # Show the plot
    plt.legend()
    plt.show()
    return None

