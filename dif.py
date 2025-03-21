


baseline = "/Users/spot/Downloads/131b4scan"
cmp = '/Users/spot/Downloads/131b3scan'

import os
import hashlib
import shutil
import tempfile

def compress_folder(folder_path):
    # Create a temporary file
    temp_file = tempfile.mktemp()
    
    # Compress the folder
    shutil.make_archive(temp_file, 'zip', folder_path)
    
    # Calculate MD5 hash of the compressed file
    md5_hash = hashlib.md5()
    with open(temp_file + '.zip', "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    md5_digest = md5_hash.hexdigest()
    #print(f'folder: {folder_path}, md5: {md5_digest}')
    # Delete the temporary file
    os.remove(temp_file + '.zip')
    
    return md5_digest

def compare_folders(folder1, folder2):
    # Get list of subfolders in each folder
    subfolders1 = [f for f in os.listdir(folder1) if os.path.isdir(os.path.join(folder1, f))]
    subfolders2 = [f for f in os.listdir(folder2) if os.path.isdir(os.path.join(folder2, f))]
    #print(f'FOLDER1{subfolders1}, FOLDER2{subfolders2}')    
    # Check if the number of subfolders is the same
    #if len(subfolders1) != len(subfolders2):
    #    return False
    
    # Check if the compressed files for each subfolder have the same MD5 hash
    dif = []
    for subfolder in subfolders1:
        print(subfolder)
        compressed_file1 = compress_folder(os.path.join(folder1, subfolder))
        compressed_file2 = compress_folder(os.path.join(folder2, subfolder))
        if compressed_file1 != compressed_file2:
            dif.append(subfolder)
    print(dif)
    return True

# Example usage:
folder1_path = baseline
folder2_path = cmp
result = compare_folders(folder1_path, folder2_path)
print("Folders are identical:", result)

