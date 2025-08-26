#!/usr/bin/env python3
"""
CS144 Project - Khet 3D
Soft Hand-in 2 Implementation
Student: 26972336

This module handles the initial configuration parsing and error checking for the Khet 3D game.
It implements all requirements for Soft Hand-in 2, focusing on configuration file validation.
"""

from pathlib import Path
import argparse
import re
from typing import Dict, List, Tuple, Optional

# Error messages from Appendix A
ERROR_MESSAGES = {
    "no_config": "Config file '{}' not found",
    "invalid_dimensions": "Invalid dimensions format in the configuration file",
    "no_empty_line": "Expected an empty line after dimensions in the configuration file",
    "invalid_line_count": "Expected {} lines according to given dimensions in the configuration file, got {}",
    "invalid_layer_header": "Invalid layer header format and/or layer index at line {}, expected 'Layer {}:'",
    "invalid_row_format": "Invalid row format at layer {}, row {}",
    "invalid_sphinx_layer": "Invalid sphinxes: sphinx found on layer {}, only allowed on layer 0",
    "invalid_pharaoh_layer": "Invalid pharaohs: pharaoh found on layer {}, only allowed on layer {}",
    "invalid_sphinx_count": "Invalid sphinxes: expected exactly 1 sphinx per player",
    "invalid_pharaoh_count": "Invalid pharaohs: expected exactly 1 pharaoh per player"
}

class GamePiece:
    """Represents a game piece with its symbol and owner."""
    def __init__(self, symbol: str, owner: str):
        self.symbol = symbol
        self.owner = owner

    def __repr__(self):
        return f"({self.symbol},{self.owner})"

class GameLayer:
    """Represents a single layer in the game cube."""
    def __init__(self, index: int, n: int, m: int):
        self.index = index
        self.n = n  # columns (x-axis)
        self.m = m  # rows (y-axis)
        self.grid = [[None for _ in range(n)] for _ in range(m)]

    def place_piece(self, x: int, y: int, piece: Optional[GamePiece]):
        """Place a piece at the specified coordinates."""
        if 0 <= x < self.n and 0 <= y < self.m:
            self.grid[y][x] = piece

class KhetGame:
    """Main class for the Khet 3D game implementation."""
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.output_dir = Path("out")
        self.output_dir.mkdir(exist_ok=True)
        self.output_file = self.output_dir / (self.config_path.stem + ".out")
        self.n = self.m = self.k = 0
        self.layers: List[GameLayer] = []
        self.sphinx_count: Dict[str, int] = {"A": 0, "B": 0}
        self.pharaoh_count: Dict[str, int] = {"A": 0, "B": 0}
        self.error_occurred = False

    def _handle_error(self, error_key: str, *args) -> bool:
        """Write error message to output file and set error flag."""
        message = ERROR_MESSAGES[error_key].format(*args)
        self.output_file.write_text(message + "\n")
        self.error_occurred = True
        return False

    def _validate_move_pattern(self, move: str) -> bool:
        """Validate move pattern using regex."""
        move_pattern = re.compile(r'^((\d{1,2},\d{1,2},\d{1,2}))(C|A|M(\d{1,2},\d{1,2},\d{1,2})F?)|q$')
        return bool(move_pattern.match(move))

    def parse_configuration(self) -> bool:
        """Parse and validate the game configuration file.
        Returns True if successful, False if errors occurred."""
        if not self.config_path.exists():
            no_config_file = self.output_dir / "noConfig.out"
            no_config_file.write_text(ERROR_MESSAGES["no_config"].format(self.config_path) + "\n")
            return False

        try:
            lines = self.config_path.read_text(encoding="utf-8").splitlines()
        except Exception:
            return self._handle_error("no_config", str(self.config_path))

        # Validate dimensions line
        if len(lines) < 1:
            return self._handle_error("invalid_dimensions")

        try:
            dimensions = lines[0].strip().split(",")
            if len(dimensions) != 3:
                return self._handle_error("invalid_dimensions")
                
            self.n, self.m, self.k = map(int, dimensions)
            if not (3 <= self.n <= 30 and 3 <= self.m <= 30 and 1 <= self.k <= 8):
                return self._handle_error("invalid_dimensions")
        except ValueError:
            return self._handle_error("invalid_dimensions")

        # Validate empty line after dimensions
        if len(lines) < 2 or lines[1].strip() != "":
            return self._handle_error("no_empty_line")

        # Calculate expected line count and validate
        expected_lines = 2 + self.k * (self.m + 2)
        if len(lines) != expected_lines:
            return self._handle_error("invalid_line_count", expected_lines, len(lines))

        line_index = 2  # Start after dimensions and empty line
        for layer_idx in range(self.k):
            # Validate layer header
            if line_index >= len(lines) or lines[line_index].strip() != f"Layer {layer_idx}:":
                return self._handle_error("invalid_layer_header", line_index + 1, layer_idx)
            line_index += 1

            # Create new layer
            current_layer = GameLayer(layer_idx, self.n, self.m)

            # Process each row in the layer
            for row_idx in range(self.m):
                if line_index >= len(lines):
                    return self._handle_error("invalid_line_count", expected_lines, len(lines))

                row_pieces = lines[line_index].strip().split()
                if len(row_pieces) != self.n:
                    return self._handle_error("invalid_row_format", layer_idx, row_idx)

                for col_idx, piece_str in enumerate(row_pieces):
                    if not (piece_str.startswith("(") and piece_str.endswith(")")):
                        return self._handle_error("invalid_row_format", layer_idx, row_idx)

                    piece_content = piece_str[1:-1].split(",")
                    if len(piece_content) != 2:
                        return self._handle_error("invalid_row_format", layer_idx, row_idx)

                    symbol, owner = piece_content
                    symbol = symbol.strip()
                    owner = owner.strip()

                    # Validate piece ownership
                    if owner not in ("A", "B", "N"):
                        return self._handle_error("invalid_row_format", layer_idx, row_idx)

                    # Create and place the piece
                    piece = GamePiece(symbol, owner)
                    current_layer.place_piece(col_idx, row_idx, piece)

                    # Count special pieces
                    if symbol in ["▲", "▼", "◀", "▶"]:  # Sphinx symbols
                        if layer_idx != 0:
                            return self._handle_error("invalid_sphinx_layer", layer_idx)
                        if owner in ("A", "B"):
                            self.sphinx_count[owner] += 1

                    elif symbol in ["•", "⊕"]:  # Pharaoh symbols
                        if layer_idx != self.k - 1:
                            return self._handle_error("invalid_pharaoh_layer", layer_idx, self.k - 1)
                        if owner in ("A", "B"):
                            self.pharaoh_count[owner] += 1

                line_index += 1

            # Validate empty line after layer
            if line_index >= len(lines) or lines[line_index].strip() != "":
                return self._handle_error("no_empty_line")
            line_index += 1

            self.layers.append(current_layer)

        # Validate sphinx and pharaoh counts
        if self.sphinx_count["A"] != 1 or self.sphinx_count["B"] != 1:
            return self._handle_error("invalid_sphinx_count")

        if self.pharaoh_count["A"] != 1 or self.pharaoh_count["B"] != 1:
            return self._handle_error("invalid_pharaoh_count")

        # If we get here, configuration is valid
        self._write_initial_state()
        return True

    def _write_initial_state(self):
        """Write the initial game state to the output file."""
        output_lines = []
        for layer in self.layers:
            output_lines.append(f"Layer {layer.index}:")
            for row in layer.grid:
                output_lines.append(" ".join(str(piece) if piece else "( ,N)" for piece in row))
            output_lines.append("")  # Empty line after each layer

        self.output_file.write_text("\n".join(output_lines).strip() + "\n")

def main():
    """Main entry point for the Khet 3D game."""
    parser = argparse.ArgumentParser(
        description="Khet 3D Game - Configuration Parser for Soft Hand-in 2",
        epilog="Example: python3 khet.py configs/game1.txt"
    )
    parser.add_argument(
        "config_path",
        type=str,
        help="Path to the game configuration file"
    )
    
    args = parser.parse_args()
    
    game = KhetGame(args.config_path)
    if not game.parse_configuration():
        # Error occurred during parsing
        return

if __name__ == "__main__":
    main()