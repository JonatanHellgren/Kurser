from PIL import Image

pieces = [
    "wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"
]
for piece in pieces:
    Image.open("images/" + piece + ".png").save("images/" + piece + ".bmp")
