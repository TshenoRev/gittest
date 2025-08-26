from stdlib import stdio
import sys

class Game:
    def __init__(self, config_file):
        self.config_file = config_file
        self.output_file = config_file.replace('.txt', '.out')  # Output file name
        self.n = self.m = self.k = 0  # Dimensions of the cube
        self.board = None
        self.read_configuration()

    def read_configuration(self):
        try:
            with open(self.config_file, 'r') as file:
                # Read dimensions
                dimensions = file.readline().strip().split(',')
                if len(dimensions) != 3:
                    self.write_error("Invalid dimensions format in the configuration file")
                    return

                self.n, self.m, self.k = map(int, dimensions)

                # Check for valid dimensions
                if self.n < 3 or self.m < 3:
                    self.write_error("Invalid dimensions: must be at least 3x3.")
                    return

                # Read layers
                for layer in range(self.k):
                    layer_header = file.readline().strip()
                    if layer_header != f"Layer {layer}:":
                        self.write_error(f"Invalid layer header format at layer {layer}. Expected 'Layer {layer}:'")
                        return

                    for row in range(self.m):
                        line = file.readline().strip()
                        if not line:
                            self.write_error(f"Expected {self.m} lines according to given dimensions in the configuration file, got {layer * self.m + row}")
                            return

                        pieces = line.split()
                        if len(pieces) != self.n:
                            self.write_error(f"Invalid row format at layer {layer}, row {row}. Expected {self.n} pieces.")
                            return

                # If we reach here, the configuration is valid
                stdio.writeln("Configuration read successfully.")

        except FileNotFoundError:
            self.write_error(f"Config file '{self.config_file}' not found.")
        except Exception as e:
            self.write_error(f"Error reading configuration file: {e}")

    def write_error(self, message):
        with open(self.output_file, 'w') as out_file:
            out_file.write(message + '\n')
        stdio.writeln(message)  # Also print to console for debugging
        sys.exit(1)  # Exit the program

def main():
    if len(sys.argv) != 2:
        stdio.writeln("Usage: python3 khet.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    game = Game(config_file)

if __name__ == '__main__':
    main()
