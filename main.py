from gui import EncoderGUI
from encoders import Huffman

if __name__ == "__main__":
    gui = EncoderGUI(Huffman())
    gui.run()