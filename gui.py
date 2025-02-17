import tkinter as tk
from tkinter import messagebox, ttk
from encoders import Huffman
from encoder_interfaces import EncoderFileInterface, EncoderNoneError
from file_operator import FileOperator, FileTypeError, PathNoneError
import os, logging, sys


class EncoderGUI():

    def __init__(self, encoder:Huffman):

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

    def global_error_handler(self, exctype, value, traceback):
        logging.error("Uncaught Exception", exc_info=(
            exctype, value, traceback))
        


    # ***** MAIN MENUS *****

    def top_menu(self) -> None:
        """ Sets all the widgets for the top bar menu.  

        Returns
        -------
        None
        """

        try:
            bar = tk.Menu(self.root)
            encoding = tk.Menu(bar)
            parameters = tk.Menu(bar)

            # Sub-Menu Buttons
            encoding.add_command(label="New Encoder",
                                 command=lambda: self.save_name.set(self.file_manager.new_encoder()))
            encoding.add_command(label="Open Encoder",
                                 command=lambda: self.save_name.set(self.file_manager.open_encoder()))
            encoding.add_command(label="Save As",
                                 command=lambda: self.save_name.set(self.file_manager.save_encoder()))

            parameters.add_command(label="Encoding and Statistics", 
                                   command=self.encoding_stats)
            parameters.add_command(label="Settings", 
                                   command=self.settings)
            parameters.add_command(label="Help", 
                                   command=self.help)
            parameters.add_separator()
            parameters.add_command(label="Exit", 
                                   command=self.root.quit)

            # Menu Button
            bar.add_cascade(label="Encoder", 
                            menu=encoding)
            bar.add_cascade(label="Parameters", 
                            menu=parameters)

            self.root.config(menu=bar)

        except Exception as e:
            messagebox.showerror(title="Error", message="An UI error occured. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)

    def compression_menu(self) -> None:
        """ Sets all the widgets for the compression menu.  

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
        """ Creates a new window with the current huffman tree's statistics and binary encoding information. 

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

    def settings(self) -> None:
        """ Creates a new window to allow for in-app settings modification. 

        Returns
        -------
        None
        """

        try:
            # Create the new window.
            settings_window = tk.Toplevel(self.root)
            settings_window.title("Help")

            # Default Save setting UI:
            default_save_label = tk.Label(settings_window, text="Default Save Folder: ")

            self.default_saving_dir_path = tk.StringVar()
            save_path_entry = tk.Entry(settings_window, textvariable=self.default_saving_dir_path, width=50)
            save_path_entry.config(state="readonly")

            try:
                browse_save = lambda: self.default_saving_dir_path.set(FileOperator.browse_directories( 
                    "Select Folder"
                ))
                browse_save_button = tk.Button(settings_window, text="Select Default Save Folder", command=browse_save)
            
            except Exception as e:
                pass

            # Default Encoder setting UI:
            default_encoder_label = tk.Label(settings_window, text="Default Encoder File: ")

            self.default_encoding_file_path = tk.StringVar()
            encoder_path_entry = tk.Entry(settings_window, textvariable=self.default_encoding_file_path, width=50)
            encoder_path_entry.config(state="readonly")

            try:
                browse_encoder = lambda: self.default_encoding_file_path.set(FileOperator.browse_files(
                    [("Binary Files", "*.bin")], 
                    "Select File"
                ))
                browse_encoder_button = tk.Button(settings_window, text="Select Default Encoder File", command=browse_encoder)
            
            except Exception as e:
                pass

            # Close window UI:
            save_close_button = tk.Button(settings_window, text="Save and Close", command=settings_window.destroy)

            cancel_button = tk.Button(settings_window, text="Cancel", command=settings_window.destroy)

            # Widget positions.
            default_save_label.grid(row=0, column=0, padx=10, pady=10)
            save_path_entry.grid(row=0, column=1, padx=10, pady=10)
            browse_save_button.grid(row=1, column=0, padx=10, pady=10)
            default_encoder_label.grid(row=2, column=0, padx=10, pady=10)
            encoder_path_entry.grid(row=2, column=1, padx=10, pady=10)
            browse_encoder_button.grid(row=3, column=0, padx=10, pady=10)
            save_close_button.grid(row=4, column=1, padx=10, pady=10)
            cancel_button.grid(row=4, column=0, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror(title="Error", message="An UI error occured. Please see log files for more details.")
            logging.error(str(e), exc_info=True)

    def help(self) -> None:
        """ Creates a new window with the help information.

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

    def browse_files_handler(self, filetypes:list):
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
    
    def compress_handler(self):
    
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
    
    def extract_handler(self):

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

    def display_character_info_handler(self, event) -> None:
        """ Updates the character information frame of the statistics window when selecting a specific character.

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
        """ Resets all entries in all menus to blank.  

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
