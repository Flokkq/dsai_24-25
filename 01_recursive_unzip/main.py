import zipfile
import os
import sys

def unzip_recursive(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted: {zip_path} to {extract_to}")

    for root, _, files in os.walk(extract_to):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                new_extract_to = os.path.splitext(file_path)[0]
                unzip_recursive(file_path, new_extract_to)
                os.remove(file_path)  # Remove the nested zip after extracting

if __name__ == "__main__":
    zip_file_path = "dir.zip"
    output_directory = "dir"

    if not os.path.exists(zip_file_path):
        print(f"File {zip_file_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    unzip_recursive(zip_file_path, output_directory)
