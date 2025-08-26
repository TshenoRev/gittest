import sys
import math
import random
from picture import Picture
from color import Color

def fibonacci_spiral(width, height):
    """
    Generate a Fibonacci spiral pattern.
    """
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    picture = Picture(width, height)

    for x in range(width):
        for y in range(height):
            # Convert pixel coordinates to polar coordinates
            center_x = width / 2
            center_y = height / 2
            dx = x - center_x
            dy = y - center_y
            r = math.sqrt(dx**2 + dy**2)
            theta = math.atan2(dy, dx)

            # Apply Fibonacci spiral formula
            r_spiral = phi ** (theta / math.pi)

            # Calculate color based on the spiral position
            if r_spiral > 0:
                color_value = int(255 * (r_spiral % 1))  # Normalize to [0, 255]
                color = Color(color_value, 100, 150)  # Example color scheme
            else:
                color = Color(128, 128, 128)  # Default gray for invalid r

            # Set the pixel color
            if 0 <= x < width and 0 <= y < height:
                picture.set(x, y, color)

    return picture

def galaxy_spiral(width, height):
    """
    Generate a multi-arm spiral galaxy pattern.
    """
    picture = Picture(width, height)
    total_arms = random.randint(2, 4)  # Random number of arms

    for x in range(width):
        for y in range(height):
            # Convert pixel coordinates to polar coordinates
            center_x = width / 2
            center_y = height / 2
            dx = x - center_x
            dy = y - center_y
            r = math.sqrt(dx**2 + dy**2)
            theta = math.atan2(dy, dx)

            # Create multiple spiral arms
            for arm_number in range(total_arms):
                theta_arm = theta + (arm_number * 2 * math.pi / total_arms)
                r_spiral = 0.1 * math.exp(0.1 * theta_arm)  # Logarithmic spiral

                # Add noise for realistic effect
                noise = random.uniform(-0.1, 0.1)
                r_spiral += noise

                # Calculate color based on the spiral position
                if r_spiral > 0:
                    color_value = int(255 * (r_spiral % 1))  # Normalize to [0, 255]
                    color = Color(color_value, 100, 150)  # Example color scheme
                else:
                    color = Color(128, 128, 128)  # Default gray for invalid r

                # Set the pixel color
                if 0 <= x < width and 0 <= y < height:
                    picture.set(x, y, color)

    return picture

def main():
    """
    Main function to generate spiral art based on command-line parameters.
    """
    if len(sys.argv) < 3:
        # Default to a gray image if no arguments are given
        width, height = 800, 600
        picture = Picture(width, height)
        for x in range(width):
            for y in range(height):
                picture.set(x, y, Color(128, 128, 128))  # Gray color
        picture.show()
        return

    width = int(sys.argv[1])
    height = int(sys.argv[2])
    pattern_type = sys.argv[3].lower()

    if pattern_type == "fibonacci":
        picture = fibonacci_spiral(width, height)
    elif pattern_type == "galaxy":
        picture = galaxy_spiral(width, height)
    else:
        print("Unknown pattern type. Use 'fibonacci' or 'galaxy'.")
        return

    # Show the generated picture
    picture.show()

if __name__ == "__main__": main
