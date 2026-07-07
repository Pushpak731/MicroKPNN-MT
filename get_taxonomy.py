import urllib.request
import zipfile
import os

# Define URL and Paths
url = "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip"
save_path = "Default_Database/taxdmp.zip"
extract_path = "Default_Database"

# Ensure folder exists
os.makedirs(extract_path, exist_ok=True)

print("Downloading NCBI Taxonomy database (this might take a minute)...")
try:
    urllib.request.urlretrieve(url, save_path)
    print("Download complete.")
    
    print("Extracting files...")
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        # We only need nodes.dmp and names.dmp
        zip_ref.extract("nodes.dmp", extract_path)
        zip_ref.extract("names.dmp", extract_path)
        
    print("Success! 'nodes.dmp' and 'names.dmp' are now in Default_Database.")
    
    # Optional cleanup
    os.remove(save_path)

except Exception as e:
    print(f"Error: {e}")