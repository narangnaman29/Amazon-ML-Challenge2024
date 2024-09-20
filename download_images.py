import os
import pandas as pd
from tqdm import tqdm
from urllib import request
from PIL import Image
from pathlib import Path

# Directory to save the downloaded images
download_folder = './dw_images/'  # Relative path in your project directory
os.makedirs(download_folder, exist_ok=True)


# Function to create placeholder images for invalid URLs
def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        print(f"Error creating placeholder image: {e}")


# Function to download individual images
def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for _ in range(retries):
        try:
            request.urlretrieve(image_link, image_save_path)
            return
        except Exception:
            print(f"Failed to download {image_link}. Retrying...")
            time.sleep(delay)

    create_placeholder_image(image_save_path)


# Load the CSV file (make sure 'train.csv' is in your project folder)
csv_path = 'D:/Amazon ML Challenge/student_resource 3/dataset/train.csv'
df = pd.read_csv(csv_path)

# Extract image links from the 'image_link' column
image_links = df['image_link'].dropna().tolist()

# Download images
for image_link in tqdm(image_links, total=len(image_links)):
    download_image(image_link, save_folder=download_folder)

print("Image downloading complete.")
