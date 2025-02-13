import tkinter as tk
from encoder import Huffman
from file_operations import FileOperator
import os

class EncoderInterface:
    
    def compress(self):
        pass

    def extract(self):
        pass



class EncoderFileInterface(EncoderInterface):

    def __init__(self, encoder:Huffman):
        self.encoder = encoder

        # ***** ENCODING MENU ACTIONS *****

    def new_encoder(self) -> None:
        """ Generates a new huffman tree and a new corresponding binary encoding for future compressions and extractions.

        Returns
        -------
        None
        """

        # Ask the user for a text file from which generate the new huffman tree.
        try:
            path = FileOperator.browse_files(title="Select File", filetypes=[("Text File", "*.txt")])

            if path == None:
                return None
        except:
            raise

        # Generate the new huffman tree.
        try:
            data = FileOperator.load(path)
            self.encoder.set_huffman(data)
            save_name = "untitled.json*"
            
            return save_name
        except Exception as e:
            raise

    def open_encoder(self, manual_path:str = None) -> None:
        """ 

        Returns
        -------
        None
        """

        # Ask the user for the huffman tree json save.
        try:
            if manual_path == None:             
                path = FileOperator.browse_files(title="Open File", filetypes=[("JSON File", "*.json")])
                if path == None:
                    return None
            else:
                path = manual_path

        except Exception as e:
            print(str(e))
            raise

        # Load the save into the encoder.
        try:
            data = FileOperator.load(path)

            save_name = data[0]
            self.encoder.char_to_bin_index = data[1]
            self.encoder.bin_to_char_index = data[2]
            self.encoder.char_percentages = data[3]

            return save_name
        
        except Exception as e:
            raise

    def save_encoder(self) -> None:
        """ Saves the currently loaded huffman encoding to the target path.

        Returns
        -------
        None
        """

        # Ask the user for the directory in which to save the huffman tree json file.
        try:
            path = FileOperator.browse_save_files(title="Save File As", 
                                                  defaultextension=".json", 
                                                  filetypes=[("JSON File", "*.json")],
                                                  initialfile="untitled")
            if path == None:
                return None
            
        except Exception as e:
            raise

        # Save the huffman encoding in the directory as a json file.
        try:
            data = [os.path.basename(path),
                    self.encoder.char_to_bin_index,
                    self.encoder.bin_to_char_index,
                    self.encoder.char_percentages]

            FileOperator.save(path, data)
            save_name = os.path.basename(path)
            
            return save_name

        except Exception as e:
            raise

    # ***** COMPRESS AND EXTRACT ACTIONS *****

    def compress(self, file_path:str, save_path:str) -> None:
        """ Gets the file to compress and compresses it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        # Get text file to compress and compress.
        if self.encoder.char_to_bin_index == None:
            raise
        elif not file_path:
            raise
        elif not save_path:
            raise
        else:
            try:
                # Compress file.
                data = FileOperator.load(file_path)
                compressed = self.encoder.encode(data)

                # Save to target path.
                FileOperator.save(save_path, compressed)

            except Exception as e:
                raise

        return None

    def extract(self, file_path:str, save_path:str) -> int:
        """ Gets the file to extract and extracts it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        if self.encoder.char_to_bin_index == None:
            raise
        elif not file_path:
            raise
        elif not save_path:
            raise
        else:
            try:
                # Exract file.
                data = FileOperator.load(file_path)
                extracted = self.encoder.decode(data)

                # Save to target path.
                FileOperator.save(save_path, extracted)
    
            except Exception as e:
                raise

        return None
