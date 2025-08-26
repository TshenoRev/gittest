#!/usr/bin/env python3
"""
CS144 Project - Khet 3D
Soft Hand-in 2 Implementation (Alternate Style)

This script parses and validates the initial configuration file
for the Khet 3D game. It follows the same functional requirements
as the original, but uses a different coding style.
"""

from pathlib import Path
import argparse
import re
from typing import Dict, List, Optional

# ----------------------------------------------------------------------
# Error message templates from Appendix A
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------
class Piece:
    """Represents a game piece with symbol and owner."""
    def __init__(self, symbol: str, owner: str):
        self.symbol = symbol
        self.owner = owner

    def __repr__(self) -> str:
        return f"({self.symbol},{self.owner})"


class Layer:
    """One layer (z-level) of the Khet 3D board."""
    def __init__(self, index: int, width: int, height: int):
        self.index = index
        self.width = width   # number of columns (x-axis)
        self.height = height # number of rows (y-axis)
        self.cells: List[List[Optional[Piece]]] = [
            [None] * width for _ in range(height)
        ]

    def put(self, x: int, y: int, piece: Optional[Piece]) -> None:
        """Place a piece at coordinates (x, y) if within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = piece


# ----------------------------------------------------------------------
# Main game parser
# ----------------------------------------------------------------------
class Khet3D:
    """Configuration parser and validator for Khet 3D."""

    def __init__(self, config_file: str):
        self.config_path = Path(config_file)
        self.output_dir = Path("out")
        self.output_dir.mkdir(exist_ok=True)

        self.output_file = self.output_dir / (self.config_path.stem + ".out")
        self.width = 0
        self.height = 0
        self.layers_count = 0

        self.layers: List[Layer] = []
        self.sphinxes: Dict[str, int] = {"A": 0, "B": 0}
        self.pharaohs: Dict[str, int] = {"A": 0, "B": 0}
        self.error_flag = False

    # --------------------------------------------------------------
    # Utility: write error and mark parsing failed
    # --------------------------------------------------------------
    def fail(self, key: str, *fmt_args) -> bool:
        message = ERROR_MESSAGES[key].format(*fmt_args)
        self.output_file.write_text(message + "\n")
        self.error_flag = True
        return False

    # --------------------------------------------------------------
    # Utility: move string validator (currently unused)
    # --------------------------------------------------------------
    def valid_move(self, move: str) -> bool:
        pattern = re.compile(
            r'^(((\d{1,2},\d{1,2},\d{1,2}))(C|A|M(\d{1,2},\d{1,2},\d{1,2})F?)|q)$'
        )
        return bool(pattern.match(move))

    # --------------------------------------------------------------
    # Main parser
    # --------------------------------------------------------------
    def parse(self) -> bool:
        # Step 1: file existence
        if not self.config_path.exists():
            (self.output_dir / "noConfig.out").write_text(
                ERROR_MESSAGES["no_config"].format(self.config_path) + "\n"
            )
            return False

        try:
            lines = self.config_path.read_text(encoding="utf-8").splitlines()
        except Exception:
            return self.fail("no_config", self.config_path)

        # Step 2: dimensions
        if not lines:
            return self.fail("invalid_dimensions")

        dims = lines[0].strip().split(",")
        if len(dims) != 3:
            return self.fail("invalid_dimensions")

        try:
            self.width, self.height, self.layers_count = map(int, dims)
        except ValueError:
            return self.fail("invalid_dimensions")

        if not (3 <= self.width <= 30 and 3 <= self.height <= 30 and 1 <= self.layers_count <= 8):
            return self.fail("invalid_dimensions")

        # Step 3: blank line after dimensions
        if len(lines) < 2 or lines[1].strip():
            return self.fail("no_empty_line")

        # Step 4: total line count check
        expected = 2 + self.layers_count * (self.height + 2)
        if len(lines) != expected:
            return self.fail("invalid_line_count", expected, len(lines))

        # Step 5: layer-by-layer parsing
        idx = 2
        for z in range(self.layers_count):
            # layer header
            if idx >= len(lines) or lines[idx].strip() != f"Layer {z}:":
                return self.fail("invalid_layer_header", idx + 1, z)
            idx += 1

            layer = Layer(z, self.width, self.height)

            # rows
            for row in range(self.height):
                if idx >= len(lines):
                    return self.fail("invalid_line_count", expected, len(lines))

                tokens = lines[idx].strip().split()
                if len(tokens) != self.width:
                    return self.fail("invalid_row_format", z, row)

                for col, token in enumerate(tokens):
                    if not (token.startswith("(") and token.endswith(")")):
                        return self.fail("invalid_row_format", z, row)

                    parts = token[1:-1].split(",")
                    if len(parts) != 2:
                        return self.fail("invalid_row_format", z, row)

                    symbol, owner = (p.strip() for p in parts)
                    if owner not in ("A", "B", "N"):
                        return self.fail("invalid_row_format", z, row)

                    piece = Piece(symbol, owner)
                    layer.put(col, row, piece)

                    # special piece checks
                    if symbol in ["▲", "▼", "◀", "▶"]:  # sphinx
                        if z != 0:
                            return self.fail("invalid_sphinx_layer", z)
                        if owner in ("A", "B"):
                            self.sphinxes[owner] += 1

                    elif symbol in ["•", "⊕"]:  # pharaoh
                        if z != self.layers_count - 1:
                            return self.fail("invalid_pharaoh_layer", z, self.layers_count - 1)
                        if owner in ("A", "B"):
                            self.pharaohs[owner] += 1

                idx += 1

            # blank line after each layer
            if idx >= len(lines) or lines[idx].strip():
                return self.fail("no_empty_line")
            idx += 1

            self.layers.append(layer)

        # Step 6: piece counts
        if self.sphinxes["A"] != 1 or self.sphinxes["B"] != 1:
            return self.fail("invalid_sphinx_count")
        if self.pharaohs["A"] != 1 or self.pharaohs["B"] != 1:
            return self.fail("invalid_pharaoh_count")

        # Step 7: write initial state
        self.write_state()
        return True

    # --------------------------------------------------------------
    # Write the initial parsed state to output file
    # --------------------------------------------------------------
    def write_state(self) -> None:
        lines_out = []
        for layer in self.layers:
            lines_out.append(f"Layer {layer.index}:")
            for row in layer.cells:
                lines_out.append(
                    " ".join(str(piece) if piece else "( ,N)" for piece in row)
                )
            lines_out.append("")  # blank line after each layer
        self.output_file.write_text("\n".join(lines_out).strip() + "\n")


# ----------------------------------------------------------------------
# CLI Entry Point
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Khet 3D Game - Configuration Parser",
        epilog="Example: python3 khet.py configs/game1.txt"
    )
    parser.add_argument("config_path", type=str, help="Path to configuration file")
    args = parser.parse_args()

    game = Khet3D(args.config_path)
    game.parse()  # Output/error file written regardless of success


if __name__ == "__main__":
    main()