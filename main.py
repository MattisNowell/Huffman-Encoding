from gui import HuffmanGUI
from encoder import Huffman

if __name__ == "__main__":
    gui = HuffmanGUI(Huffman())
    gui.run()