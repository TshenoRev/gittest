import sys
from color import Color
from picture import Picture
from instream import InStream
from outstream import OutStream

def string_operations():
    """
    Demonstrates various string operations.
    """
    print("--- String Operations ---")
    sample_string = "Hello, World!"
    print("Original String:", sample_string)
    print("Length of String:", len(sample_string))
    print("Substring (0-5):", sample_string[0:5])
    print("Does it contain 'World'? :", 'World' in sample_string)
    print("Index of 'o':", sample_string.find('o'))
    print("Replaced 'World' with 'Python':", sample_string.replace('World', 'Python'))
    print("Split by ',':", sample_string.split(','))
    print()

def color_operations():
    """
    Demonstrates color operations using the Color class.
    """
    print("--- Color Operations ---")
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)

    print("Red Color:", red)
    print("Green Color:", green)
    print("Blue Color:", blue)

    # Calculate luminance
    luminance_red = 0.299 * red.getRed() + 0.587 * red.getGreen() + 0.114 * red.getBlue()
    print("Luminance of Red Color:", luminance_red)

    # Convert to grayscale
    gray_color = Color(int(luminance_red), int(luminance_red), int(luminance_red))
    print("Grayscale Color from Red:", gray_color)
    print()

def image_processing(image_file):
    """
    Demonstrates image processing by converting an image to grayscale.
    """
    print("--- Image Processing ---")
    try:
        picture = Picture(image_file)
        print("Loaded image:", image_file)
        print("Image dimensions:", picture.width(), "x", picture.height())

        # Convert to grayscale
        for col in range(picture.width()):
            for row in range(picture.height()):
                pixel = picture.get(col, row)
                gray_value = int(0.299 * pixel.getRed() + 0.587 * pixel.getGreen() + 0.114 * pixel.getBlue())
                gray_pixel = Color(gray_value, gray_value, gray_value)
                picture.set(col, row, gray_pixel)

        # Save the new grayscale image
        output_file = "grayscale_" + image_file
        picture.save(output_file)
        print("Grayscale image saved as:", output_file)

    except Exception as e:
        print("Error loading image:", e)

def file_operations(input_file, output_file):
    """
    Demonstrates file input and output operations.
    """
    print("--- File Operations ---")
    try:
        in_stream = InStream(input_file)
        out_stream = OutStream(output_file)

        while not in_stream.isEmpty():
            line = in_stream.readLine()
            out_stream.writeln(line)

        print("Content copied from", input_file, "to", output_file)

    except Exception as e:
        print("Error during file operations:", e)

def main():
    """
    Main function to run the demonstrations.
      """
    string_operations()
    color_operations()

    # Image processing demonstration
    if len(sys.argv) > 1:
        image_file = sys.argv[1]
        image_processing(image_file)

    # File operations demonstration
    if len(sys.argv) > 2:
        input_file = sys.argv[2]
        output_file = "output_" + input_file
        file_operations(input_file, output_file)

if __name__ == "__main__":
    main()
