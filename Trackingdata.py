from kloppy import secondspectrum, opta
import numpy as np
import pandas as pd
from kloppy.domain import OptaPitchDimensions, TrackingDataset




def loadTrackingData(meta_data: str, raw_data: str, additional_meta_data: str = None, sample_rate: float = None, coordinates: str = "secondspectrum", only_alive: bool = True) -> TrackingDataset:
    """
    Load tracking data from a SecondSpectrum dataset.

    Parameters
    ----------
    meta_data : str
        Path to the metadata file.
    raw_data : str
        Path to the raw data file.
    additional_meta_data : str, optional
        Path to the additional metadata file.
    sample_rate : float, optional
        The sample rate of the tracking data.
    coordinates : str, optional
        The coordinate system of the tracking data. Can be either "opta" or "secondspectrum".
    only_alive : bool, optional
        Whether to only include alive players in the tracking data.

    Returns
    -------
    TrackingData
        The tracking data.
    """

    # Load tracking data
    tracking_dataset = secondspectrum.load(
        meta_data=meta_data,
        raw_data=raw_data,
        
        additional_meta_data=additional_meta_data,
        sample_rate=sample_rate,
        coordinates=coordinates,
        only_alive=only_alive
    )
    
    tracking_dataset = tracking_dataset.transform(to_coordinate_system="opta", to_orientation="BALL_OWNING_TEAM", to_pitch_dimensions=OptaPitchDimensions())
    return tracking_dataset




def flattenTrackingData(TrackingData: TrackingDataset) -> pd.DataFrame:
    """
    Flatten tracking data.

    Parameters
    ----------
    TrackingData : TrackingDataset
        The tracking data.

    Returns
    -------
    pd.DataFrame
        The flattened tracking data.
    """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

    # Extract structured data from tracking dataset
    data_rows = []
    i = 0
    match_start_time = pd.Timestamp("2023-10-20 18:00:00")  # Replace with actual match start time
    for frame in TrackingData.records:
        frame_number = i
        timestamp = frame.timestamp  # This is in timedelta format
        period_id = frame.period.id
        i += 1

        # Ball data
        if frame.ball_coordinates:
            ball_x = frame.ball_coordinates.x
            ball_y = frame.ball_coordinates.y
            ball_z = frame.ball_coordinates.z
            ball_timestamp = match_start_time + timestamp  # Add timedelta to match start time
            data_rows.append({
                "period_id": period_id,
                "timestamp": ball_timestamp,  # Store as datetime
                "frame": frame_number, #SKAL DET HER VÆRE FRAME ID I STEDET FOR?????????????????
                "player_id": None,  # No player ID for ball
                "ball": True,
                "x": ball_x,
                "y": ball_y,
                "z": ball_z,
                "acceleration": frame.ball_speed if frame.ball_speed else 0
            })

        # Player data
        for player, data in frame.players_data.items():
            player_timestamp = match_start_time + timestamp  # Add timedelta to match start time
            data_rows.append({
                "period_id": period_id,
                "timestamp": player_timestamp,  # Store as datetime
                "frame": frame_number,
                "player_id": player.player_id,
                "ball": False,
                "x": data.coordinates.x,
                "y": data.coordinates.y,
                "z": None,  # Players don't have Z-coordinates
                "acceleration": data.speed if hasattr(data, "speed") else None
            })

    # Convert to DataFrame
    df_tracking = pd.DataFrame(data_rows)

    return df_tracking

def getTrackingdata(meta_data: str, raw_data: str, additional_meta_data: str = None, sample_rate: float = None, coordinates: str = "secondspectrum", only_alive: bool = True) -> pd.DataFrame:
    TrackingData = loadTrackingData(meta_data, raw_data, additional_meta_data, sample_rate, coordinates, only_alive)
    df_tracking = flattenTrackingData(TrackingData)
    df_tracking["timestamp"] = df_tracking["timestamp"].apply(
        lambda x: str(x).split()[2] if isinstance(x, pd.Timedelta) else x
    )  # CREATE TIMESTAMP
    
    df_tracking = df_tracking[(df_tracking['z'].isna()) | (df_tracking['z'] >= 0)].copy()  # REMOVE NEGATIVE Z VALUES & COPY KAN OGSÅ SÆTTES TIL 0
    
    df_tracking.loc[:, "player_id"] = df_tracking["player_id"].astype("Int64")  # CONVERT PLAYER ID TO INT
    
    df_tracking.reset_index(drop=True, inplace=True)  # RESET INDEX
    
    return df_tracking