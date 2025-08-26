import math
import stddraw
from color import Color
def red_function(x, y):
    return math.sin(math.pi * math.sin(math.pi * math.sin(math.pi * 
           (math.sin(math.pi * math.sin(math.pi * math.sin(math.pi * 
           (math.sin(math.pi * math.cos(math.pi * y)))))) * 
           math.cos(math.pi * math.sin(math.pi * 
           (0.5 * (math.sin(math.pi * y) + (x * x)))))))))

def green_function(x, y):
    return math.sin(math.pi * x)

def blue_function(x, y):
    return 4.3 * math.cos(math.sin(math.pi * x)) - 3.31

def main():
    # Set up the canvas
    stddraw.setCanvasSize(512, 512)
    stddraw.setXscale(-1, 1)
    stddraw.setYscale(-1, 1)

    # Loop through each pixel in the canvas
    for i in range(512):
        for j in range(512):
            # Map pixel coordinates to the range -1 to 1
            x = (i / 256) - 1  # Maps 0-511 to -1 to 1
            y = (j / 256) - 1  # Maps 0-511 to -1 to 1

            # Calculate the color values
            r = red_function(x, y)
            g = green_function(x, y)
            b = blue_function(x, y)

            # Normalize the color values to the range [0, 1]
            r = (r + 1) / 2  # Map from [-1, 1] to [0, 1]
            g = (g + 1) / 2  # Map from [-1, 1] to [0, 1]
            b = (b + 1) / 2  # Map from [-1, 1] to [0, 1]

            # Set the color and draw the pixel
            stddraw.setPenColor(Color(int(r * 255), int(g * 255), int(b * 255)))
            stddraw.point(x, y)

    # Show the canvas
    stddraw.show()

if __name__ == "__main__": 
    main()
