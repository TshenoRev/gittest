import sys
from picture import Picture

def apply_filter(image, filter_type):
    """
    Apply the specified filter to the image.

    Parameters:
    image (Picture): The image to apply the filter to.
    filter_type (str): The type of filter to apply ('sepia', 'noir', 'brightness').

    Returns:
    Picture: The filtered image.
    """
    width = image.getWidth()
    height = image.getHeight()
    new_image = Picture(width, height)

    for x in range(width):
        for y in range(height):
            pixel = image.getPixel(x, y)
            r = pixel.getRed()
            g = pixel.getGreen()
            b = pixel.getBlue()

            if filter_type == "sepia":
                new_r = min(255, int(0.393 * r + 0.769 * g + 0.189 * b))
                new_g = min(255, int(0.349 * r + 0.686 * g + 0.168 * b))
                new_b = min(255, int(0.272 * r + 0.534 * g + 0.131 * b))
            elif filter_type == "noir":
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                enhanced = min(255, max(0, int(gray * 1.5 - 64)))
                new_r = new_g = new_b = enhanced
            elif filter_type == "brightness":
                new_r = min(255, int(r * 1.2))
                new_g = min(255, int(g * 1.2))
                new_b = min(255, int(b * 1.2))
            else:
                raise ValueError("Invalid filter type. Choose 'sepia', 'noir', or 'brightness'.")

            new_pixel = new_image.getPixel(x, y)
            new_pixel.setRed(new_r)
            new_pixel.setGreen(new_g)
            new_pixel.setBlue(new_b)

    return new_image

def main():
    """
    Main function to execute the image filtering program.
    """
    if len(sys.argv) != 3:
        print("Usage: python3 image_filter.py <image_file> <filter_type>")
        sys.exit(1)

    image_file = sys.argv[1]
    filter_type = sys.argv[2]

    # Load the image
    image = Picture(image_file)

    # Apply the filter
    filtered_image = apply_filter(image, filter_type)

    # Save the new image with a modified name
    new_image_file = image_file.split('.')[0] + f"_{filter_type}.jpg"
    filtered_image.write(new_image_file)
    print(f"Filtered image saved as '{new_image_file}'.")

if __name__ == "__main__":
    main()
