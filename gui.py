import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from huffman import Huffman
import json
import os
import logging
import sys


class GUI():

    def __init__(self):
        self.encoder = Huffman()

        self.root = tk.Tk()
        self.root.title("Huffman Compressor")

        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.save_name = tk.StringVar()
        self.save_name.set("None")

        try:
            self.load_save("default.json")
        except Exception as e:
            pass

        logging.basicConfig(
            filename="error.log",
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        sys.excepthook = self.global_error_handler

        self.top_menu()
        self.compression_menu()
        self.extraction_menu()

    def global_error_handler(self, exctype, value, traceback):
        logging.error("Uncaught Exception", exc_info=(
            exctype, value, traceback))

    # ***** MENU DISPLAYS *****

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
            encoding.add_command(label="New Huffman Encoding",
                                 command=self.new_huffman_encoder)
            encoding.add_command(label="Open Huffman Encoding",
                                 command=self.open_huffman_encoder)
            encoding.add_command(label="Save Huffman Encoding",
                                 command=self.save_huffman_encoder)

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
            bar.add_cascade(label="Encoding", 
                            menu=encoding)
            bar.add_cascade(label="Parameters", 
                            menu=parameters)

            self.root.config(menu=bar)

        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="An UI error occured. Please see log files for details.")
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

            tk.Label(compression_tab, textvariable=self.save_name).grid(
                row=0, column=0, padx=10, pady=10)

            # COMPRESSION TITLE
            tk.Label(compression_tab, text="Compress").grid(
                row=1, column=0, padx=10, pady=10)

            # COMPRESSION FILE ENTRY AND BROWSER
            self.compression_file_path = tk.StringVar()
            entry = tk.Entry(
                compression_tab, textvariable=self.compression_file_path, width=50)
            entry.grid(row=2, 
                       column=0, 
                       padx=10, 
                       pady=10)
            entry.config(state="readonly")

            tk.Button(compression_tab, text="Select File", command=lambda: self.browse_files(path=self.compression_file_path, 
                                                                                             filetype=[("Text Files", "*.txt")], 
                                                                                             title="Select File")).grid(row=3, column=0, padx=10, pady=10)

            # COMPRESSION FOLDER ENTRY AND BROWSER
            self.compression_target_path = tk.StringVar()
            entry = tk.Entry(
                compression_tab, textvariable=self.compression_target_path, width=50)
            entry.grid(row=4, column=0, padx=10, pady=10)
            entry.config(state="readonly")

            tk.Button(compression_tab, text="Save As", command=lambda: self.browse_save_files(
                self.compression_target_path, 
                filetype=[("Binary File", "*.bin")], 
                defaultextension=".bin", 
                initialfile=os.path.splitext(os.path.basename(self.compression_file_path.get()))[0], 
                title="Save As"
                )).grid(row=5, column=0, padx=10, pady=10)

            # COMPRESS
            tk.Button(compression_tab, text="Compress", command=self.compress).grid(
                row=7, column=0, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror(
                "Error", "An UI error occured. Please log files for details.")
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

            tk.Label(extraction_tab, textvariable=self.save_name).grid(row=0, 
                                                                       column=0, 
                                                                       padx=10, 
                                                                       pady=10)

            # EXTRACTION TITLE
            tk.Label(extraction_tab, text="Extract").grid(
                row=1, column=0, padx=10, pady=10)

            # EXTRACTION FILE ENTRY AND BROWSER
            self.extraction_file_path = tk.StringVar()
            entry = tk.Entry(extraction_tab, 
                             textvariable=self.extraction_file_path, 
                             width=50)
            entry.grid(row=2, 
                       column=0, 
                       padx=10, 
                       pady=10)
            entry.config(state="readonly")

            tk.Button(extraction_tab, 
                      text="Select File", 
                      command=lambda: 
                      self.browse_files(self.extraction_file_path, 
                                        filetype=[("Binary Files", "*.bin")], 
                                        title="Select File")).grid(row=3, column=0, padx=10, pady=10)

            # EXTRACTION TARGET FOLDER ENTRY AND BROWSER
            self.extraction_target_path = tk.StringVar()
            entry = tk.Entry(
                extraction_tab, textvariable=self.extraction_target_path, width=50)
            entry.grid(row=4, column=0, padx=10, pady=10)
            entry.config(state="disabled")

            tk.Button(extraction_tab, text="Save As", command=lambda: self.browse_save_files(
                self.extraction_target_path, 
                filetype=[("Text File", "*.txt")], 
                defaultextension=".txt", 
                initialfile=os.path.splitext(os.path.basename(self.extraction_file_path.get()))[0], 
                title="Save As"
                )).grid(row=5, column=0, padx=10, pady=10)

            # EXTRACT
            tk.Button(extraction_tab, text="Extract", command=self.extract).grid(
                row=7, column=0, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="The UI error occured. Please see log files for details.")
            logging.error(msg=str(e), exc_info=True)

    def reset_menus(self) -> None:
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

    # ***** ENCODING MENU ACTIONS *****

    def new_huffman_encoder(self) -> None:
        """ Generates a new huffman tree and a new corresponding binary encoding for future compressions and extractions.

        Returns
        -------
        None
        """

        path = tk.StringVar()

        # Ask the user for a text file from which generate the new huffman tree.
        try:
            self.browse_files(path, [("Text Files", "*.txt")], "Select File")
        except:
            logging.error(str(e), exc_info=True)
            return None

        # Generate the new huffman tree.
        try:
            with open(file=path.get(), mode='r') as file:
                self.encoder.set_huffman(text=file.read())
                self.save_name.set(value="untitled.json")
                messagebox.showinfo(title="Success", 
                                    message="A new huffman encoding was successfully generated.")
                
        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="An error occurred with the selected file.")
            logging.error(msg=str(e), exc_info=True)

    def open_huffman_encoder(self) -> None:
        """ 

        Returns
        -------
        None
        """

        path = tk.StringVar()

        # Ask the user for the huffman tree json save.
        try:
            self.browse_files(path=path, 
                              filetype=[("JSON File", "*.json")], 
                              title="Open File")
            
        except Exception as e:
            logging.error(msg=str(e), exc_info=True)
            return None

        # Load the save into the encoder.
        try:
            self.load_save(path.get())
            messagebox.showinfo(title="Success", 
                                message="The huffman encoding was successfully loaded.")
            
        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="The huffman encoding failed to load.")
            logging.error(msg=str(e), exc_info=True)

    def save_huffman_encoder(self) -> None:
        """ Saves the currently loaded huffman encoding to the target path.

        Returns
        -------
        None
        """

        path = tk.StringVar()

        # Ask the user for the directory in which to save the huffman tree json file.
        try:
            self.browse_save_files(path=path, 
                                   title="Save File As", 
                                   defaultextension=".json", 
                                   filetype=[("JSON Files", "*.json")],
                                   initialfile="untitled")
            
        except Exception as e:
            logging.error(msg=str(e), exc_info=True)
            return None

        # Save the huffman encoding in the directory as a json file.
        try:
            self.create_save(path.get())
            messagebox.showinfo(title="Success", 
                                message="The current huffman encoding was successfully saved.")
            
        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="The current huffman encoding failed to save.")
            logging.error(str(e), exc_info=True)

    # ***** SETTINGS MENU ACTIONS *****

    def encoding_stats(self) -> None:
        """ Creates a new window with the current huffman tree's statistics and binary encoding information. 

        Returns
        -------
        None
        """

        try:
            # Displaying the stats and encoding.
            if self.encoder.char_to_bin_index == None:
                messagebox.showinfo(title="Information", 
                                    message="No encoder detected. Please open or create an encoder to see its details.")
                return None
            else:
                # Creating the new window.
                stats_window = tk.Toplevel(self.root)
                stats_window.title("Encoding and Statistics")

                left_frame = tk.Frame(stats_window)
                left_frame.pack(side=tk.LEFT, 
                                fill=tk.BOTH,
                                padx=10, 
                                pady=10, 
                                expand=True)

                right_frame = tk.Frame(stats_window)
                right_frame.pack(side=tk.LEFT, 
                                 fill=tk.BOTH,
                                 padx=10, 
                                 pady=10, 
                                 expand=True)

                self.listbox = tk.Listbox(
                    left_frame, height=15, selectmode=tk.SINGLE)
                self.listbox.pack(side=tk.LEFT, 
                                  fill=tk.BOTH, 
                                  expand=True)

                items = [i for i in list(
                    self.encoder.char_to_bin_index.keys())]
                for i in items:
                    self.listbox.insert(tk.END, i)

                self.listbox.bind("<<ListboxSelect>>",
                                  self.display_character_info)

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

    def display_character_info(self, event) -> None:
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
            percentage = self.encoder.char_percentages[char]
            binary = self.encoder.char_to_bin_index[char]

            # Update the displayed string text.
            self.info.config(
                text=f"Character: {char}\n Percentage of appearance: {percentage}\nBinary Encoding: {binary}")

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

            tk.Label(settings_window, text="Default Save Folder: ").grid(
                row=0, column=0, padx=10, pady=10)

            self.default_saving_dir_path = tk.StringVar()
            entry = tk.Entry(
                settings_window, textvariable=self.default_saving_dir_path, width=50)
            entry.grid(row=0, column=1, padx=10, pady=10)
            entry.config(state="readonly")
            tk.Button(settings_window, text="Select Default Save Folder", command=lambda: self.browse_directories(
                self.default_saving_dir_path, "Select Folder")).grid(row=1, column=0, padx=10, pady=10)

            tk.Label(settings_window, text="Default Encoder File: ").grid(
                row=2, column=0, padx=10, pady=10)

            self.default_encoding_file_path = tk.StringVar()
            entry = tk.Entry(
                settings_window, textvariable=self.default_encoding_file_path, width=50)
            entry.grid(row=2, column=1, padx=10, pady=10)
            entry.config(state="readonly")
            tk.Button(settings_window, text="Select Default Encoder File", command=lambda: self.browse_files(
                self.default_encoding_file_path,  [("Binary Files", "*.bin")], "Select File")).grid(row=3, column=0, padx=10, pady=10)

            tk.Button(settings_window, text="Save and Close", command=settings_window.destroy).grid(
                row=4, column=1, padx=10, pady=10)
            tk.Button(settings_window, text="Cancel", command=settings_window.destroy).grid(
                row=4, column=0, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror(
                "Error", "An UI error occured. Please see log files for more details.")
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

            # Help text:
            help_text = "Select a huffman encoding."

            # Display the help dialogue.
            tk.Label(help_window, text=help_text).grid(row=0, 
                                                       column=0, 
                                                       padx=10, 
                                                       pady=10)
            tk.Button(help_window, text="Close", command=help_window.destroy).grid(
                row=1, column=0, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror(
                "Error", "An UI error occured. Please see log files for more details.")
            logging.error(str(e), exc_info=True)

    # ***** FILE EXPLORER BROWSING ACTIONS *****

    def browse_files(self, path: tk.StringVar, filetype: list, title: str = '') -> None:
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
            file_path = filedialog.askopenfilename(title=title, 
                                                   filetype=filetype)
            if file_path:
                path.set(file_path)
        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="The file operation failed. Please see log files for more details.")
            logging.error(msg=str(e), exc_info=True)
            raise

    def browse_save_files(self, path: tk.StringVar, filetype: list, defaultextension: str = ".json", title: str = '', initialfile:str="untitled") -> None:
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
            file_path = filedialog.asksaveasfilename(title=title, 
                                                     defaultextension=defaultextension, 
                                                     initialfile=initialfile, 
                                                     filetypes=filetype)
            if file_path:
                path.set(file_path)

        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="The file operation failed. Please see log files for more details.")
            logging.error(msg=str(e), exc_info=True)
            raise

    def browse_directories(self, path: tk.StringVar, title: str = '') -> None:
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
            directory_path = filedialog.askdirectory(title=title)
            if directory_path:
                path.set(directory_path)

        except Exception as e:
            messagebox.showerror(title="Error", 
                                 message="The file operation failed. Please see log files for more details.")
            logging.error(msg=str(e), exc_info=True)
            raise

    # ***** FILE SAVE AND LOAD FUNCTIONS *****

    def create_save(self, path: str):
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

        # Saving the Huffman parameters in a file.
        try:
            with open(path, "w") as json_file:
                data = [os.path.basename(path), 
                        self.encoder.char_to_bin_index,
                        self.encoder.bin_to_char_index, 
                        self.encoder.char_percentages]
                json.dump(data, json_file, indent=4)
                self.save_name.set(data[0])

        except Exception as e:
            raise

    def load_save(self, path: str) -> None:
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
            if os.path.exists(path):
                with open(path, 'r') as json_file:
                    data = json.load(json_file)
                    self.save_name.set(data[0])
                    self.encoder.char_to_bin_index, self.encoder.bin_to_char_index, self.encoder.char_percentages = data[1], data[2], data[3]
            else:
                return None
        except Exception as e:
            raise

    # ***** COMPRESS AND EXTRACT ACTIONS *****

    def compress(self) -> None:
        """ Gets the file to compress and compresses it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        # Get text file to compress and compress.

        if self.encoder.char_to_bin_index == None:
            messagebox.showerror(
                "Error", "No encoder detected. Please open or create an encoder to compress files.")
        elif not self.compression_file_path.get():
            messagebox.showerror("Error", "Please select a file to compress.")
        elif not self.compression_target_path.get():
            self.compression_target_path.set("")
        else:
            try:
                res = None
                # Compress file.
                with open(self.compression_file_path.get(), 'r') as file:
                    res = self.encoder.encode(file.read())
                # Save to target path.
                with open(self.compression_target_path.get(), 'wb') as file:
                    file.write(res)
                messagebox.showinfo(
                    "Success", f"File succesfully encoded to: {self.compression_target_path.get()}")
                self.reset_menus()
            except Exception as e:
                messagebox.showerror(
                    "Error", "An error has occured during compression. Please see log file for more details.")
                logging.error(str(e), exc_info=True)
        return None

    def extract(self) -> int:
        """ Gets the file to extract and extracts it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        if self.encoder.char_to_bin_index == None:
            messagebox.showerror(
                "Error", "No encoder detected. Please open or create an encoder to extract files.")
        elif not self.extraction_file_path.get():
            messagebox.showerror("Error", "Please select a file to extract.")
        elif not self.extraction_target_path.get():
            self.compression_target_path.set("")
        else:
            try:
                res = None
                # Exract file.
                with open(self.extraction_file_path.get(), 'rb') as file:
                    res = self.encoder.decode(file.read())
                # Save to target path.
                with open(self.extraction_target_path.get(), 'w') as file:
                    file.write(res)
                messagebox.showinfo(
                    "Success", f"File succesfully extracted to: {self.extraction_target_path.get()}")
                self.reset_menus()
            except Exception as e:
                messagebox.showerror(
                    "Error", "An error has occured during extraction. Please see log files for more details.")
                logging.error(str(e), exc_info=True)
        return None

    # ***** Run *****

    def run(self):
        self.root.mainloop()
