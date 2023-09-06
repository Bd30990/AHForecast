import os

directory = 'icon_images/'

for filename in os.listdir(directory):
    print(filename)
    if filename.endswith('.PNG'):
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, filename.lower())
        try:
            os.rename(old_path, new_path)
            print(f"Renamed {old_path} to {new_path}")
        except Exception as e:
            print(f"Error renaming {old_path} to {new_path}. Error: {e}")
