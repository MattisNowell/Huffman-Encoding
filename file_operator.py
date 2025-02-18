from tkinter import filedialog
import json, os
from typing import Optional, Union

class PathNoneError(Exception):
    """ Exception raised when a path is of type None.

    Attributes
    ----------
    None

    Methods
    -------
    None
    """

    def __init__(self, message="The path is of type None"):
        """ Initializes the PathNoneError class.
        """
        super().__init__(message)

class FileTypeError(Exception):
    """ Exception raised when the file type is not recognised or handled.

    Attributes
    ----------
    None

    Methods
    -------
    None
    """

    def __init__(self, message="The file type is not recognised or handled"):
        """ Initializes the FileTypeError class.
        """
        super().__init__(message)

class FileOperator:
    """ Class to handle file operations such as saving, loading, and browsing files.

    Attributes
    ----------
    None

    Methods
    -------
    browse_files(title:str = '', filetypes:list = []) -> Optional[str]
        Get an input from the user to select a file.
    browse_save_files(title:str = '', defaultextension:str = ".json", initialfile:str = "untitled.bin", filetypes:list = []) -> Optional[str]
        Get an input from the user to select a file.
    browse_directories(title:str = '') -> Optional[str]
        Get an input from the user to select a folder.
    save(path:str, data:Union[str, bytes, list]) -> None
        Saves a given data into a specified file.
    load(path:str) -> Union[str, bytes, list]  
        Load data from a specified file.
    """

    @staticmethod
    def browse_files(title:str = '', filetypes:list = []) -> Optional[str]:
        """ Get an input from the user to select a file.

        Parameters
        ----------
        title: str
            Title to be displayed in the file explorer.
        filetype: list 
            List of tuple descriptions of the file types to be constrained to in the file explorer.

        Returns
        -------
        Optional[str] 
            The path to the file selected by the user.
        """

        try:
            path = filedialog.askopenfilename(title=title, filetypes=filetypes)

            if path:
                return path
            
            raise PathNoneError()
            
        except Exception as e:
            raise e

    @staticmethod
    def browse_save_files(title:str = '', defaultextension:str = ".json", initialfile:str = "untitled.bin", filetypes:list = []) -> Optional[str]:
        """ Get an input from the user to select a file.

        Parameters
        ----------
        title:
            Title to be displayed in the file explorer.
        defaultextension: str
            Default extension to be used for the file.
        initialfile: str
            Initial file name to be displayed in the file explorer.
        filetype: list 
            List of tuple descriptions of the file types to be constrained to in the file explorer.

        Returns
        -------
        Optional[str]
            The path to the file selected by the user.
        """

        try:
            path = filedialog.asksaveasfilename(title=title, 
                                                defaultextension=defaultextension, 
                                                initialfile=initialfile, 
                                                filetypes=filetypes)
            if path:
                return path
        
            raise PathNoneError()

        except Exception as e:
            raise e

    @staticmethod
    def browse_directories(title:str = '') -> Optional[str]:
        """ Get an input from the user to select a folder. The path is saved in a given path variable.

        Parameters
        ----------     
        title:
            Title to be displayed in the file explorer.

        Returns
        -------
        Optional[str] 
            The path to the folder selected by the user.
        """

        try:
            path = filedialog.askdirectory(title=title)

            if path:
                return path

            raise PathNoneError()

        except Exception as e:
            raise e

    @staticmethod
    def save(path:str, data:Union[str, bytes, list]) -> None:
        """ Saves a given data into a specified file.

        Parameters
        ----------
        path : str
            Text string to represents a path to the file to save the data to.
        data : Union[str, bytes, list]
            Data to be saved.
            

        Returns
        -------
        None
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
                raise FileTypeError()
        
        except Exception as e:
            raise e

    @staticmethod
    def load(path:str) -> Union[str, bytes, list]:
        """ Load data from a specified file.

        Parameters
        ----------
        path : str
            Text string to represents a path to the file to load the data from.

        Returns
        -------
        Union[str, bytes, list]
            Data loaded from the file.
        """
        try:
            if not os.path.exists(path):
                raise FileNotFoundError()
            
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
                raise FileTypeError()
            
            return data 
        
        except Exception as e:
            raise e
