import os
from typing import Optional
from abc import ABC, abstractmethod

from encoders import Encoder
from file_operator import FileOperator, PathNoneError


class EncoderInterface(ABC):
    """ Abstract class to represent an interface between a user and an encoder.

    Attributes
    ----------
    None 

    Methods
    -------
    compress() -> None
        Compresses a file.

    extract() -> None
        Extracts a file.
    """

    @abstractmethod
    def compress(self):
        """ Compresses a file.
        """
        pass

    @abstractmethod
    def extract(self):
        """ Extracts a file.
        """
        pass

class EncoderFileInterface(EncoderInterface):
    """ Class to represent an interface between a user and an encoder through file operations.

    Attributes
    ----------
    encoder: Encoder
        The encoder to interface with.
    
    Methods
    -------
    new_encoder() -> Optional[str]
        Generates a new encoder for future compressions and extractions.
    open_encoder(path:Optional[str]) -> Optional[str]
        Opens an encoder from a json file.
    save_encoder() -> Optional[str]
        Saves the currently opened encoding to a json file.
    compress(file_path:str, save_path:str) -> None
        Compresses a file and saves it to a target file.
    extract(file_path:str, save_path:str) -> None
        Extracts a file and saves it to a target file.
    """

    def __init__(self, encoder:Encoder):
        self.encoder = encoder

        # ***** ENCODING MENU ACTIONS *****

    def new_encoder(self) -> Optional[str]:
        """ Generates a new huffman tree and a new corresponding binary encoding for future compressions and extractions.

        Parameters
        ----------
        None

        Returns
        -------
        Optional[str]
            The name of the generated encoding file.
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

    def open_encoder(self, path:Optional[str] = None) -> Optional[str]:
        """ Opens an encoder from a json file.

        Parameters
        ----------
        path: Optional[str]
            The path to the json file to open.

        Returns
        -------
        Optional[str]
            The name of the opened encoding file.
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

    def save_encoder(self) -> Optional[str]:
        """ Saves the currently opened encoding to a json file.

        Parameters
        ----------
        None

        Returns
        -------
        Optional[str]
            The name of the saved encoding file.
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
        """ Compresses a file and saves it to a target file.

        Parameters
        ----------
        file_path: str
            The path to the file to compress.
        save_path: str
            The path to the directory to save the compressed file.

        Returns
        -------
        None
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

    def extract(self, file_path:str, save_path:str) -> None:
        """ Extracts a file and saves it to a target file.

        Parameters
        ----------
        file_path: str
            The path to the file to extract.
        save_path: str
            The path to the directory to save the extracted file.

        Returns
        -------
        None
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