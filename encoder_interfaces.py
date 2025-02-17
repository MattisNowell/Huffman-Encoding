import tkinter as tk
from encoders import Encoder, EncoderNoneError
from file_operator import FileOperator, PathNoneError
import os
from abc import ABC, abstractmethod


class EncoderInterface(ABC):
    
    @abstractmethod
    def compress(self):
        pass

    @abstractmethod
    def extract(self):
        pass

class EncoderFileInterface(EncoderInterface):

    def __init__(self, encoder:Encoder):
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

        except PathNoneError as e:
            return None 
        
        except Exception as e:
            raise e 

        # Generate the new huffman tree.
        try:
            data = FileOperator.load(path)
            self.encoder.init(data)
            save_name = "untitled.json*"
            
            return save_name
        
        except Exception as e:
            raise e

    def open_encoder(self, path:str = None) -> None:
        """ 

        Returns
        -------
        None
        """

        # Ask the user for the huffman tree json save.
        try:
            if path == None:             
                path = FileOperator.browse_files(title="Open File", filetypes=[("JSON File", "*.json")])
        
        except PathNoneError as e:
            return None 

        except Exception as e:
            raise e

        # Load the save into the encoder.
        try:
            data = FileOperator.load(path)

            save_name = data[0]
            self.encoder.char_to_bin_index = data[1]
            self.encoder.bin_to_char_index = data[2]
            self.encoder.char_percentages = data[3]

            return save_name
        
        except Exception as e:
            raise e

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
            
        except PathNoneError as e:
            return None
        
        except Exception as e:
            raise e

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
            raise e

    # ***** COMPRESS AND EXTRACT ACTIONS *****

    def compress(self, file_path:str, save_path:str) -> None:
        """ Gets the file to compress and compresses it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        # Get text file to compress and compress.
        
        if not file_path or not save_path:
            raise PathNoneError
        
        else:
            try:
                # Compress file.
                data = FileOperator.load(file_path)
                compressed = self.encoder.encode(data)

                # Save to target path.
                FileOperator.save(save_path, compressed)

            except Exception as e:
                raise e

    def extract(self, file_path:str, save_path:str) -> int:
        """ Gets the file to extract and extracts it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        if not file_path or not save_path:
            raise PathNoneError
        
        else:
            try:
                # Exract file.
                data = FileOperator.load(file_path)
                extracted = self.encoder.decode(data)

                # Save to target path.
                FileOperator.save(save_path, extracted)

            except Exception as e:
                raise e