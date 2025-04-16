import os


def loadFiles(Home: str, Away: str) -> dict: #Root: str for testy.py
    """
    Load data from a SecondSpectrum dataset.

    Parameters
    ----------
    Home : str
        The home team.
    Away : str
        The away team.

    Returns
    -------
    dict
        The files.
    """

    # Define the folder path
    folder_path = f"C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/{Home}_{Away}" #folder_path = f"C:/Users/jda/Desktop/Hvidovre IF - Silkeborg IF/python/data/{Root}/{Home}_{Away}" for testy.py
    print(f"Folder path: {folder_path}")


    # Define the file patterns
    file_patterns = {
        "metadata": "_SecondSpectrum_Metadata.xml",
        "raw": "_SecondSpectrum_Data.jsonl",
        "additionalMetaData": "_SecondSpectrum_Metadata.json",
        "f7": "-matchresults.xml",
        "f24": "-eventdetails.xml"
    }

    # Get all files in the folder
    files_in_folder = os.listdir(folder_path)

    # Match files to patterns
    matched_files = {}
    for key, ending in file_patterns.items():
        for file in files_in_folder:
            if file.endswith(ending):
                if key in ["f7", "f24"]:
                    matched_files[key] = file
                else:
                    matched_files[key] = os.path.join(folder_path, file)
                break  # Stop once we find a match

    return matched_files

