import os
import shutil

# Define source directories
source_dir_games = r"C:\Users\jda\Desktop\data speciale\3. Nedrykningsspil 2023_2024"
source_dir_metadata = r"C:\Users\jda\Desktop\data speciale\Metadata 2023_2024"
# Destination base directory
destination_base = r"C:\Users\jda\Desktop\Hvidovre IF - Silkeborg IF\python\data"

# Ensure the destination base folder exists
os.makedirs(destination_base, exist_ok=True)

# Process all game data files
for filename in os.listdir(source_dir_games):
    if filename.endswith(".jsonl"):  # Process only JSONL files
        parts = filename.split('-')
        
        if len(parts) > 2:
            team_names = parts[1] + "_" + parts[2].split('_')[0]  # Extract team names
            match_id = parts[0]  # Get the date part (20230721, etc.)
            
            # Create the destination folder
            new_folder = os.path.join(destination_base, team_names)
            os.makedirs(new_folder, exist_ok=True)
            
            # Move game data file
            source_path = os.path.join(source_dir_games, filename)
            destination_path = os.path.join(new_folder, filename)
            
            if not os.path.exists(destination_path):
                shutil.move(source_path, destination_path)
                print(f"Moved {filename} -> {destination_path}")
            else:
                print(f"Skipped {filename}, already exists in {new_folder}")

            # Now, move corresponding metadata files
            for meta_filename in os.listdir(source_dir_metadata):
                if meta_filename.startswith(match_id + '-' + parts[1] + '-' + parts[2].split('_')[0]):
                    source_meta_path = os.path.join(source_dir_metadata, meta_filename)
                    destination_meta_path = os.path.join(new_folder, meta_filename)

                    if not os.path.exists(destination_meta_path):
                        shutil.move(source_meta_path, destination_meta_path)
                        print(f"Moved metadata {meta_filename} -> {destination_meta_path}")
                    else:
                        print(f"Skipped metadata {meta_filename}, already exists in {new_folder}")
