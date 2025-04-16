import os

# Path to the Matchfeeds folder
matchfeeds_path = r"C:\Users\jda\Desktop\data speciale\Event Data 2023-2024\Matchfeeds"

# Function to trim folder names by removing everything after and including the first "(" and the space before it
def trim_folder_names():
    for folder in os.listdir(matchfeeds_path):
        folder_path = os.path.join(matchfeeds_path, folder)
        
        # Only process directories
        if os.path.isdir(folder_path):
            # Trim the folder name by removing everything after and including the first "("
            if "(" in folder:
                fixed_folder_name = folder.split("(", 1)[0].strip()  # Split at the first "(" and strip extra spaces
            else:
                fixed_folder_name = folder  # No change if "(" is not found
            
            # If the name has changed, rename the folder
            if folder != fixed_folder_name:
                fixed_folder_path = os.path.join(matchfeeds_path, fixed_folder_name)
                os.rename(folder_path, fixed_folder_path)
                print(f"Renamed: {folder} -> {fixed_folder_name}")

# Run the function to trim folder names
trim_folder_names()
