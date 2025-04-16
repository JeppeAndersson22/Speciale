from socceraction.data.opta import parsers, OptaLoader
import socceraction.spadl as spadl
import pandas as pd

def getEventData(matchID: int, f7: str, f24: str, Home: str, Away: str) -> pd.DataFrame:
    """
    Get event data from Opta feed files.
    
    Parameters
    ----------
    matchID : int
        The match ID.
    f7 : str
        The f7 feed file.
    f24 : str
        The f24 feed file.
    
    Returns
    -------
    pd.DataFrame
        The event data.
    """
    # Load Opta feed files
    api = OptaLoader(
        root = f"C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/{Home}_{Away}", #!Processed for testy.py
        feeds={
            "f7": f7,
            "f24": f24
        },
        parser={
            "f7": parsers.F7XMLParser,  # Use the F7XMLParser for parsing f7 feed files
            "f24": parsers.F24XMLParser  # Use the F24XMLParser for parsing f24 feed files
        }
    )
    
    # Get events
    events = api.events(matchID)
    
    # Convert actions to SPADL
    df_actions = spadl.opta.convert_to_actions(events, 1)
    
    # Merge names for teams and players
    df_actions = (spadl.add_names(df_actions)
                  .merge(api.teams(matchID).merge(api.players(matchID))))
    
    # Merge df_actions with events DataFrame on 'original_event_id' in df_actions and 'event_id' in events
    df_actions = df_actions.merge(events[['event_id', 'timestamp']], left_on='original_event_id', right_on='event_id', how='left')
    
    # Now df_actions will have the 'timestamp' column from the events DataFrame
    
    # Remove rows where 'original_event_id' is NaN
    df_actions = df_actions.dropna(subset=['original_event_id'])
    
    # First, ensure the player_id is treated as a string (object)
    df_actions["player_id"] = df_actions["player_id"].astype("Int64")
    df_actions["player_id"] = df_actions["player_id"].astype("object")
    #df_actions = df_actions[["period_id", "timestamp", "player_id", "type_name", "start_x", "start_y", "bodypart_id"]]
    df_actions.reset_index(drop=True, inplace=True)
    
    return df_actions

