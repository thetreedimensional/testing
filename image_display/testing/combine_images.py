from PIL import Image

def combine_images(image_files, output_file, show=False):
    """
    Overlay multiple images on top of each other and save the combined image.

    :param image_files: List of paths to the image files.
    :param output_file: Path to save the combined image.
    :param show: Boolean to indicate if the combined image should be displayed.
    """
    # Open the first image to get the size and initialize the combined image
    base_image = Image.open(image_files[0]).convert("RGBA")
    width, height = base_image.size

    # Create a new blank image with the same size as the individual images
    combined_image = Image.new('RGBA', (width, height))

    # Overlay the images one by one
    for image_file in image_files:
        img = Image.open(image_file).convert("RGBA")
        combined_image = Image.alpha_composite(combined_image, img)
    
    # Convert transparency (alpha channel) to black
    # Split the combined image into its components (R, G, B, A)
    r, g, b, a = combined_image.split()

    # Create a new black image for the RGB channels where transparency exists
    # TODO: change to 0,0,0 for black
    black_image = Image.new("RGB", (width, height), (120, 120, 120))

    # Merge the black image with the alpha channel as a mask to convert transparent pixels to black
    combined_image = Image.composite(black_image, combined_image.convert("RGB"), a)

    # Save the combined image
    combined_image.save(output_file)

    # Optionally, display the combined image
    if show:
        combined_image.show()

    print(f"Combined image saved as '{output_file}'")

# Example usage:
# image_files = ['image1.png', 'image2.png', 'image3.png']
# combine_images(image_files, 'combined_image.png', show=True)

if __name__ == "__main__":
    # Define the image files to combine
    image_files = ['phone.png', 'folder.png', 'plug.png']

    # Define the output file path
    output_file = 'combined_image.png'

    # Combine the images and optionally show the result
    combine_images(image_files, output_file, show=True)