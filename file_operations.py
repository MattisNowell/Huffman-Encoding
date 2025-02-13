from tkinter import filedialog
import json, os
from typing import Optional, Union


class FileOperator:

    @staticmethod
    def browse_files(title:str = '', filetypes:list = []) -> Optional[str]:
        """ Get an input from the user to select a file.

        Parameters
        ----------
        path : tk.StringVar
            String variable class from the tkinter chosen to contain the user-selected path.
        filetype: list 
            List of tuple descriptions of the file types to be constrained to in the file explorer.
        title:
            Title to be displayed in the file explorer.

        Returns
        -------
        None
        """

        try:
            path = filedialog.askopenfilename(title=title, filetypes=filetypes)

            if path and os.path.exists(path):
                return path
            
            return None
            
        except Exception as e:
            raise

    @staticmethod
    def browse_save_files(title:str = '', defaultextension:str = ".json", initialfile:str = "untitled.bin", filetypes:list = []) -> Optional[str]:
        """ Get an input from the user to select a file.

        Parameters
        ----------
        path : tk.StringVar
            String variable class from the tkinter chosen to contain the user-selected path.
        filetype: list 
            List of tuple descriptions of the file types to be constrained to in the file explorer.
        title:
            Title to be displayed in the file explorer.

        Returns
        -------
        None
        """

        try:
            path = filedialog.asksaveasfilename(title=title, 
                                                defaultextension=defaultextension, 
                                                initialfile=initialfile, 
                                                filetypes=filetypes)
            return path

        except Exception as e:
            print(str(e))
            raise

    @staticmethod
    def browse_directories(title:str = '') -> Optional[str]:
        """ Get an input from the user to select a folder. The path is saved in a given path variable.

        Parameters
        ----------     
        path : tk.StringVar
            String variable class from the tkinter chosen to contain the user-selected path.
        title:
            Title to be displayed in the file explorer.

        Returns
        -------
        None
        """

        try:
            path = filedialog.askdirectory(title=title)

            if path:
                return path

            return None

        except Exception as e:
            raise

    @staticmethod
    def save(path:str, data:list) -> None:
        """ Saves the object's huffman tree parameters from a specified JSON file.

        Parameters
        ----------
        path : str
            Text string to represents a path to the file to save the JSON Huffman tree parameters into.

        Returns
        -------
        str
            An error message.
        """

        try:
            file_extension = path.split('.')[-1].lower()

            if file_extension == "txt":
                with open(path, 'w') as file:
                    file.write(data)

            elif file_extension == "bin":
                with open(path, "wb") as file:
                    file.write(data)

            elif file_extension == "json":
                with open(path, 'w') as file:
                    json.dump(data, file)

            else:
                raise 
        
        except:
            raise

    @staticmethod
    def load(path:str) -> Union[str, bytes, list]:
        """ Loads existing huffman tree parameters from a specified JSON file.

        Parameters
        ----------
        path : str
            Text string to represents a path to the file to load the JSON Huffman tree parameters from.

        Returns
        -------
        str
            An error message.
        """
        try:
            if not os.path.exists(path):
                raise 
            
            data = None
                
            file_extension = path.split('.')[-1].lower()

            if file_extension == "txt":
                with open(path, 'r') as file:
                    data = file.read()

            elif file_extension == "bin":
                with open(path, "rb") as file:
                    data = file.read()

            elif file_extension == "json":
                with open(path, 'r') as file:
                    data = json.load(file)

            else:
                raise 
            
            return data 
        
        except:
            raise
