import pandas as pd
import numpy as np
import re


def ballCoordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a dataframe of the ball coordinates and returns a list of ball coordinates
    :param df: DataFrame of ball coordinates
    :return: List of ball coordinates
    """
    df = df.copy() 
    df['start_coordinates'] = list(zip(df['start_x'], df['start_y']))
    df['end_coordinates'] = list(zip(df['end_x'], df['end_y']))
    return df


def row_to_matrix(row, df: pd.DataFrame) -> np.array:
    player_ids = sorted(set([col.split('_')[0] for col in df.columns if re.match(r'\d+_x', col)]))
    players = []
    ball_team = row['ball_owning_team_id']
    for pid in player_ids:
        if not (pd.isna(row[f'{pid}_x']) or pd.isna(row[f'{pid}_y'])):
            x = row[f'{pid}_x']
            y = row[f'{pid}_y']
            player_team = row[f'{pid}_teamid']
            team_indicator = 1 if player_team == ball_team else 0
            players.append([x, y, team_indicator])
    return np.array(players)


# Function to remove rows with nan values from a matrix
def remove_nan_from_matrix(matrix):
    # Filter out rows where any element is nan
    return [player for player in matrix if not any(np.isnan(player))]

# Apply the function to the 'player_matrix' column

