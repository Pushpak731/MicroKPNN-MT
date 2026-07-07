import tarfile
import os

# The file we want to unzip
zip_file = "Dataset/relative_abundance.tar.gz"

print(f"Extracting {zip_file}...")

try:
    with tarfile.open(zip_file, "r:gz") as tar:
        tar.extractall(path="Dataset")
        print("Success! Unzipped 'relative_abundance.csv' into Dataset folder.")
except FileNotFoundError:
    print("Error: Could not find the zip file. Make sure you are in the MicroKPNN-MT folder.")