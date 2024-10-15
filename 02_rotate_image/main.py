import os
from PIL import Image

def rotate_and_save_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(input_dir, filename)
            img = Image.open(file_path)
            base_name, ext = os.path.splitext(filename)

            for angle in range(0, 360, 10):
                rotated_image = img.rotate(angle, expand=True)
                output_filename = f"{base_name}_{angle}{ext}"
                rotated_image.save(os.path.join(output_dir, output_filename))
                print(f"Saved rotated image: {output_filename}")

if __name__ == "__main__":
    input_directory = "in/"  # Change this to your input directory
    output_directory = "out/"  # Change this to your output directory

    rotate_and_save_images(input_directory, output_directory)
