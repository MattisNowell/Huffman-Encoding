import os, logging, sys
from typing import Optional
import tkinter as tk
from tkinter import messagebox, ttk

from encoders import Huffman, EncoderNoneError
from encoder_interfaces import EncoderFileInterface
from file_operator import FileOperator, FileTypeError, PathNoneError


class EncoderGUI():
    """ Class to handle the GUI for the encoder application.

    Attributes
    ----------
    root : tk.Tk
        The main window of the GUI.
    notebook : ttk.Notebook
        The notebook to handle multiple tabs within the GUI.
    file_manager : EncoderFileInterface
        The file manager to handle the encoder.
    save_name : tk.StringVar
        The name of the current encoder file.
    compression_file_path : tk.StringVar
        The path to the file to be compressed.
    compression_target_path : tk.StringVar
        The path to the compressed file.
    extraction_file_path : tk.StringVar
        The path to the file to be extracted.
    extraction_target_path : tk.StringVar
        The path to the extracted file.
    listbox : tk.Listbox
        The listbox to display the characters of the encoding.
    info : tk.Label
        The label to display the character information.
    
    Methods
    -------
    global_error_handler(exctype:type, value:Exception, traceback:traceback) -> None
        Global error handler for the GUI application.
    top_menu() -> None
        Sets all the widgets for the top bar menu.
    compression_menu() -> None
        Sets all the widgets for the compression menu.
    extraction_menu() -> None
        Sets all the widgets for the extraction menu.
    encoding_stats() -> None
        Sets all the widgets for a menu to display the current encoding's statistics.
    help() -> None
        Sets all the widgets for a help menu.
    close_handler() -> None
        Handles event calls for the closing of the application.
    browse_files_handler(filetypes:list) -> Optional[str]
        Handles event calls for the browsing of files.
    browse_saves_handler(filetypes:list, defaultextension:str, defaultname:str)
        Handles event calls for the browsing and creation of save files.
    new_encoder_handler() -> Optional[str]
        Handles event calls for the creation of a new encoder.
    open_encoder_handler() -> Optional[str]
        Handles event calls for the opening of an encoder.
    save_encoder_handler() -> Optional[str]
        Handles event calls for the saving of an encoder.
    compress_handler() -> None
        Handles event calls for the compression of a file.
    extract_handler() -> None
        Handles event calls for the extraction of a file.
    display_character_info_handler(event:tk.Event) -> None
        Updates the character information frame of the statistics window when selecting a specific character.
    reset_menu() -> None
        Resets entries to all menus to none.
    run() -> None
        Runs the GUI application.
    
    """

    def __init__(self, encoder:Huffman):
        """ Initialises the GUI for the encoder.
        
        Parameters
        ----------
        encoder : Huffman
            The encoder to be used by the GUI.
        
        Returns
        -------
        None
        """

        self.root = tk.Tk()
        self.root.title("Compressor")
        self.root.resizable(False, False)

        try:
            self.file_manager = EncoderFileInterface(Huffman())

            # Add ICON if available.
            try:
                current_folder = os.path.dirname(os.path.abspath(__file__))
                icon_path = os.path.join(current_folder, "assets", "icon.ico")
                self.root.iconbitmap(icon_path)

            except Exception as e:
                messagebox.showerror(title="Error", message="Failed to load icons. Please see log files for details.")
                logging.error(msg=str(e), exc_info=True)


            # Open default encoder if available.
            self.save_name = tk.StringVar(self.root, "None")
            try:
                current_folder = os.path.dirname(os.path.abspath(__file__))
                default_path = os.path.join(current_folder, "saves", "default.json")
                save_name = self.file_manager.open_encoder(default_path)
                self.save_name.set(save_name)
            
            except FileNotFoundError as e:
                messagebox.showerror(title="Error", message="The provided default file was not found or does not exist. Please see log files for details.")
                logging.error(msg=str(e), exc_info=True)


            except FileTypeError as e:
                messagebox.showerror(title="Error", message="The provided default file's extension is imcompatible. Please see log files for details.")
                logging.error(msg=str(e), exc_info=True)


            except Exception as e:
                messagebox.showerror(title="Error", message="The provided default file failed to load. Please see log files for details.")
                logging.error(msg=str(e), exc_info=True)
            
            self.root.protocol("WM_DELETE_WINDOW", self.close_handler)

            # Notebooks allow for multiple tabs within the app.
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(expand=True, fill='both')

            # Launching all menus and UIs.
            self.top_menu()
            self.compression_menu()
            self.extraction_menu()

            # Setting up logging.
            try:
                log_path = os.path.join(current_folder, "logs", "error.log")
                logging.basicConfig(
                    filename=log_path,
                    level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s"
                ) 
                sys.excepthook = self.global_error_handler
            
            except Exception as e:
                messagebox.showerror(title="Error", message="The logging system failed to set-up. Please see log files for details.")
                logging.error(msg=str(e), exc_info=True)
        
        except Exception as e:
            messagebox.showerror(title="Error", message=f"The system failed to load. {str(e)}")       
            print(str(e))

    def global_error_handler(self, exctype, value, traceback) -> None:
        """ Global error handler for the GUI application.

        Parameters
        ----------
        exctype : type
            The type of the exception.
        value : Exception
            The exception that was raised.
        traceback : traceback
            The traceback of the exception.
        
        Returns
        -------
        None
        """

        logging.error("Uncaught Exception", exc_info=(exctype, value, traceback))
        


    # ***** MAIN MENUS *****

    def top_menu(self) -> None:
        """ Sets all the widgets for the top bar menu.  

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        try:
            bar = tk.Menu(self.root)
            encoding = tk.Menu(bar)
            parameters = tk.Menu(bar)

            # Sub-Menu Buttons
            encoding.add_command(label="New Encoder", command=lambda: self.save_name.set(self.new_encoder_handler()))
            encoding.add_command(label="Open Encoder", command=lambda: self.save_name.set(self.open_encoder_handler()))
            encoding.add_command(label="Save As",command=lambda: self.save_name.set(self.save_encoder_handler()))

            parameters.add_command(label="Encoding and Statistics", command=self.encoding_stats)
            parameters.add_command(label="Help", command=self.help)
            parameters.add_separator()
            parameters.add_command(label="Exit", command=self.root.quit)

            # Menu Button
            bar.add_cascade(label="Encoder", menu=encoding)
            bar.add_cascade(label="Parameters", menu=parameters)

            self.root.config(menu=bar)

        except Exception as e:
            messagebox.showerror(title="Error", message="An UI error occured. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)

    def compression_menu(self) -> None:
        """ Sets all the widgets for the compression menu.  

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        try:
            # Creating compression tab.
            compression_tab = ttk.Frame(self.notebook)
            self.notebook.add(compression_tab, text="Compress")

            save_label = tk.Label(compression_tab, textvariable=self.save_name)

            # COMPRESSION TITLE
            compress_label = tk.Label(compression_tab, text="Compress")

            # COMPRESSION FILE ENTRY AND BROWSER
            self.compression_file_path = tk.StringVar()
            file_path_entry = tk.Entry(compression_tab, textvariable=self.compression_file_path, width=50)
            file_path_entry.config(state="readonly")

            browse_file_button = tk.Button(compression_tab, text="Select File", command=lambda: self.compression_file_path.set(self.browse_files_handler(filetypes=[("Text Files", "*.txt")])))

            
            # COMPRESSION FOLDER ENTRY AND BROWSER
            self.compression_target_path = tk.StringVar()
            save_path_entry = tk.Entry(compression_tab, textvariable=self.compression_target_path, width=50)
            save_path_entry.config(state="readonly")

            defaultname = os.path.splitext(os.path.basename(self.compression_file_path.get()))[0]
            browse_save_button = tk.Button(compression_tab, text="Save As", command=lambda: self.compression_target_path.set(self.browse_saves_handler(filetypes=[("Binary Files", "*.bin")], 
                                                                                                                      defaultextension=".bin", 
                                                                                                                      defaultname=defaultname)))

            # COMPRESS

            compress_button = tk.Button(compression_tab, text="Compress", command=self.compress_handler)
            
            # Position UI elements:
            save_label.grid(row=0, column=0, padx=10, pady=10)
            compress_label.grid(row=1, column=0, padx=10, pady=10)
            file_path_entry.grid(row=2, column=0, padx=10, pady=10)
            browse_file_button.grid(row=3, column=0, padx=10, pady=10)
            save_path_entry.grid(row=4, column=0, padx=10, pady=10)
            browse_save_button.grid(row=5, column=0, padx=10, pady=10)
            compress_button.grid(row=7, column=0, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror(title="Error", message="An UI error occured. Please log files for details.")
            logging.error(str(e), exc_info=True)

    def extraction_menu(self) -> None:
        """ Sets all the widgets for the extraction menu.  

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        try:
            # Creating extraction tab.
            extraction_tab = ttk.Frame(self.notebook)
            self.notebook.add(extraction_tab, text="Extract")

            save_label = tk.Label(extraction_tab, textvariable=self.save_name)

            # EXTRACTION TITLE
            extract_label = tk.Label(extraction_tab, text="Extract")

            # EXTRACTION FILE ENTRY AND BROWSER
            self.extraction_file_path = tk.StringVar()
            file_path_entry = tk.Entry(extraction_tab, textvariable=self.extraction_file_path, width=50)
            file_path_entry.config(state="readonly")

            browse_file_button = tk.Button(extraction_tab, text="Select File", command=lambda: self.extraction_file_path.set(self.browse_files_handler(filetypes=[("Binary Files", "*.bin")])))

            # EXTRACTION TARGET FOLDER ENTRY AND BROWSER
            self.extraction_target_path = tk.StringVar()
            save_path_entry = tk.Entry(extraction_tab, textvariable=self.extraction_target_path, width=50)
            save_path_entry.config(state="readonly")

            defaultname = os.path.splitext(os.path.basename(self.extraction_file_path.get()))[0]
            browse_save_button = tk.Button(extraction_tab, text="Save As", command=lambda: self.extraction_target_path.set(self.browse_saves_handler(filetypes=[("Text Files", "*.txt")], 
                                                                                                                     defaultextension=".txt", 
                                                                                                                     defaultname=defaultname)))
            
            # EXTRACT
            
            extract_button = tk.Button(extraction_tab, text="Extract", command=self.extract_handler)

            save_label.grid(row=0, column=0, padx=10, pady=10)
            extract_label.grid(row=1, column=0, padx=10, pady=10)
            file_path_entry.grid(row=2, column=0, padx=10, pady=10)
            browse_file_button.grid(row=3, column=0, padx=10, pady=10)
            save_path_entry.grid(row=4, column=0, padx=10, pady=10)
            browse_save_button.grid(row=5, column=0, padx=10, pady=10)
            extract_button.grid(row=7, column=0, padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror(title="Error", message="The UI error occured. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)



    # ***** SETTINGS MENUS *****

    def encoding_stats(self) -> None:
        """ Sets all the widgets for a menu to display the current encoding's statistics. 

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        try:
            # Displaying the stats and encoding.
            if self.file_manager.encoder.char_to_bin_index == None:
                messagebox.showinfo(title="Information", 
                                    message="No encoder detected. Please open or create an encoder to see its details.")
                return None
            else:
                # Creating the new window.
                stats_window = tk.Toplevel(self.root)
                stats_window.title("Encoding and Statistics")

                left_frame = tk.Frame(stats_window)
                left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

                right_frame = tk.Frame(stats_window)
                right_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

                self.listbox = tk.Listbox(left_frame, height=15, selectmode=tk.SINGLE)
                self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                items = [i for i in list(self.file_manager.encoder.char_to_bin_index.keys())]
                for i in items:
                    self.listbox.insert(tk.END, i)

                self.listbox.bind("<<ListboxSelect>>", self.display_character_info_handler)

                self.info = tk.Label(right_frame, 
                                     text="Select a character to view details", 
                                     anchor="w", 
                                     justify="left", 
                                     wraplength=200)
                
                self.info.pack(pady=10, anchor="w")

        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="An UI error occured. Please see log files for more details.")
            logging.error(msg=str(e), exc_info=True)

    def help(self) -> None:
        """ Sets all the widgets for a help menu.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        
        try:
            # Create the new window.
            help_window = tk.Toplevel(self.root)
            help_window.title("Help")

            # Display the help dialogue.
            current_folder = os.path.dirname(os.path.abspath(__file__))
            help_path = os.path.join(current_folder, "assets", "help.txt")

            help_text = FileOperator.load(help_path)

            help_label = tk.Label(help_window, text=help_text)

            help_label.pack(padx=10, pady=10)

            # Close Button
            close_button = tk.Button(help_window, text="Close", command=help_window.destroy)

            # Widget positions.
            help_label.grid(row=0, column=0, padx=10, pady=10)
            close_button.grid(row=1, column=0, padx=10, pady=10)
    
        except FileTypeError as e:
            print("Provided help text is of the wrong file type.")
        
        except FileNotFoundError as e:
            print("Provded help text does not exist.")

        except Exception as e:
            messagebox.showerror(title="Error", message="An UI error occured. Please see log files for more details.")
            logging.error(str(e), exc_info=True)



    # ***** EVENT HANDLERS *****

    def close_handler(self):
        """ Handles event calls for the closing of the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.save_name.get() == "untitled.json*":
            save_changes = tk.messagebox.askyesnocancel("Save Encoder", "Do you want to save the encoder before exiting? Loosing your encoder might mean you will not be able to extract any compressed file.")

            if save_changes is None:
                return 
            
            elif save_changes == False:
                self.root.destroy()

            else:
                self.file_manager.save_encoder()

        else:
            self.root.destroy()

    def browse_files_handler(self, filetypes:list) -> Optional[str]:
        """ Handles event calls for the browsing of files.

        Parameters
        ----------
        filetypes : list
            List of file types to be browsed.

        Returns
        -------
        Optional[str]
            The path to the selected file.
        """

        try:
            return FileOperator.browse_files(
                filetypes=filetypes, 
                title="Select File"
            )
        
        except PathNoneError as e:
            return None
        
        except Exception as e:
            messagebox.showerror(title="Error", message="An error occured while retrieving the selected file. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)
    
    def browse_saves_handler(self, filetypes:list, defaultextension:str, defaultname:str):
        """ Handles event calls for the browsing and creation of save files.

        Parameters
        ----------
        filetypes : list
            List of file types to be browsed.
        defaultextension : str
            The default file extension to be used.
        defaultname : str
            The default file name to be used.
        
        Returns
        -------
        Optional[str]
            The path to the selected file.
        """
        try:
            return FileOperator.browse_save_files(
                filetypes=filetypes, 
                defaultextension=defaultextension, 
                initialfile=defaultname, 
                title="Save As"
            )

        except PathNoneError as e:
            return None
        
        except Exception as e:
            messagebox.showerror(title="Error", message="An error occured while retrieving the selected file. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)
    
    def new_encoder_handler(self) -> Optional[str]:
        """ Handles event calls for the creation of a new encoder.
        
        Parameters
        ----------
        None

        Returns
        -------
        Optional[str]
            The name of the new encoding file.
        """
        try:
            save = self.file_manager.new_encoder()
            
            if save is not None:
                return save
        
        except Exception as e:
            messagebox.showerror(title="Error", message="An error occured while creating a new encoder. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)
    
    def open_encoder_handler(self) -> Optional[str]:
        """ Handles event calls for the opening of an encoder.
        
        Parameters
        ----------
        None

        Returns
        -------
        Optional[str]
            The name of the opened encoding file.
        """

        try:
            save = self.file_manager.open_encoder()

            if save is not None:
                return save
        
        except Exception as e:
            messagebox.showerror(title="Error", message="An error occurred while opening an encoder. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)

    def save_encoder_handler(self) -> Optional[str]:
        """ Handles event calls for the saving of an encoder.
        
        Parameters
        ----------
        None

        Returns
        -------
        Optional[str]
            The name of the saved encoding file.
        """
        try:
            save = self.file_manager.save_encoder()

            if save is not None:
                return save

        except Exception as e:
            messagebox.showerror(title="Error", message="An error occurred while saving an encoder. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)
    
    def compress_handler(self) -> None:
        """ Handles event calls for the compression of a file.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            self.file_manager.compress(self.compression_file_path.get(), self.compression_target_path.get())
            self.reset_menu()
            messagebox.showinfo(title="Information", message="File successfully compressed.")
        
        except EncoderNoneError as e:
            messagebox.showinfo(title="Information", message="You must open or create an encoder to compress a file. Please see the help menu for more information.")
        
        except PathNoneError as e:
            messagebox.showerror(title="Error", message="Please provide a file to compress and a save file.")
        
        except Exception as e:
            messagebox.showerror(title="Error", message="An error occured during compression. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)
    
    def extract_handler(self) -> None:
        """ Handles event calls for the extraction of a file.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        try:
            self.file_manager.extract(self.extraction_file_path.get(), self.extraction_target_path.get())
            self.reset_menu()
            messagebox.showinfo(title="Information", message="File successfully extracted.")
        
        except EncoderNoneError as e:
            messagebox.showinfo(title="Information", message="You must open or create the encoder that was used to compress the extracted file. Please see the help menu for more information.")
            logging.error(msg=str(e), exc_info=True)

        except PathNoneError as e:
            messagebox.showerror(title="Error", message="Please provide a file to extract and a save file.")

        except Exception as e:
            messagebox.showerror(title="Error", message="An error occured during extraction. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)

    def display_character_info_handler(self, event:tk.Event) -> None:
        """ Updates the character information frame of the statistics window when selecting a specific character.

        Parameters
        ----------
        event : tk.Event
            The event that triggered the function.

        Returns
        -------
        None
        """

        try:
            # Get the current selection.
            selection = self.listbox.curselection()

            if not selection:
                return None

            # Get the data.
            char = self.listbox.get(selection[0])
            percentage = self.file_manager.encoder.char_percentages[char]
            binary = self.file_manager.encoder.char_to_bin_index[char]

            # Update the displayed string text.
            self.info.config(text=f"Character: {char}\n Percentage of appearance: {percentage}\nBinary Encoding: {binary}")

        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="An UI error occured. Please see log files for more details.")
            logging.error(msg=str(e), exc_info=True)

    def reset_menu(self) -> None:
        """ Resets entries to all menus to none.  

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        try:
            self.compression_file_path.set("")
            self.compression_target_path.set("")

            self.extraction_file_path.set("")
            self.extraction_target_path.set("")

        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="An UI error occured. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)



    # ***** Run *****

    def run(self):
        self.root.mainloop()
