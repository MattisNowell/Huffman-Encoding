import tkinter as tk 
from tkinter import filedialog, messagebox, ttk
from huffman import Huffman
import json, os


class GUI():

    def __init__(self):
        self.encoder = Huffman()

        self.root = tk.Tk()
        self.root.title("Huffman Compressor")

        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.top_menu()
        self.compression_menu()
        self.extraction_menu()


    # ***** MENU DISPLAYS *****
 
    def top_menu(self) -> None:
        """ Sets all the widgets for the top bar menu.  
        
        Returns
        -------
        None
        """

        bar = tk.Menu(self.root)
        encoding = tk.Menu(bar)
        settings = tk.Menu(bar)

        # Sub-Menu Buttons
        encoding.add_command(label="New Huffman Encoding", command=self.new_huffman_tree)
        encoding.add_command(label="Open Huffman Encoding", command=self.open_huffman_tree)
        encoding.add_command(label="Save Huffman Encoding", command=self.save_huffman_tree)

        settings.add_command(label="Encoding and Statistics", command=self.encoding_stats)
        settings.add_command(label="Help", command=self.help)
        settings.add_separator()
        settings.add_command(label="Exit", command=self.root.quit)

        # Menu Button
        bar.add_cascade(label="Encoding", menu=encoding)
        bar.add_cascade(label="Settings", menu=settings)

        self.root.config(menu=bar)
    
    def compression_menu(self) -> None:
        """ Sets all the widgets for the compression menu.  
        
        Returns
        -------
        None
        """

        # Creating compression tab.
        compression_tab = ttk.Frame(self.notebook)
        self.notebook.add(compression_tab, text="Compress")

        # COMPRESSION TITLE
        tk.Label(compression_tab, text="Compress").grid(row=0, column=0, padx=10, pady=10)

        # COMPRESSION FILE ENTRY AND BROWSER 
        self.compression_file_path = tk.StringVar()
        entry = tk.Entry(compression_tab, textvariable=self.compression_file_path, width=50)
        entry.grid(row=1, column=0, padx=10, pady=10)
        entry.config(state="readonly")

        tk.Button(compression_tab, text="Select File", command=lambda: self.browse_files(self.compression_file_path, [("Text Files", "*.txt")], "Select File")).grid(row=2, column=0, padx=10, pady=10)

        # COMPRESSION FOLDER ENTRY AND BROWSER 
        self.compression_target_path = tk.StringVar()
        entry = tk.Entry(compression_tab, textvariable=self.compression_target_path, width=50)
        entry.grid(row=3, column=0, padx=10, pady=10)
        entry.config(state="readonly")

        tk.Button(compression_tab, text="Select Target Directory", command=lambda: self.browse_directories(self.compression_target_path, "Select Folder")).grid(row=4, column=0, padx=10, pady=10)

        # COMPRESS
        tk.Button(compression_tab, text="Compress", command=self.compress).grid(row=6, column=0, padx=10, pady=10)

    def extraction_menu(self) -> None:
        """ Sets all the widgets for the extraction menu.  
        
        Returns
        -------
        None
        """

        # Creating extraction tab.
        extraction_tab = ttk.Frame(self.notebook)     
        self.notebook.add(extraction_tab, text="Extract")

        # EXTRACTION TITLE
        tk.Label(extraction_tab, text="Extract").grid(row=0, column=1, padx=10, pady=10)

        # EXTRACTION FILE ENTRY AND BROWSER
        self.extraction_file_path = tk.StringVar()
        entry = tk.Entry(extraction_tab, textvariable=self.extraction_file_path, width=50)
        entry.grid(row=1, column=1, padx=10, pady=10)
        entry.config(state="readonly")

        tk.Button(extraction_tab, text="Select File", command=lambda: self.browse_files(self.extraction_file_path, [("Binary Files", "*.bin")], "Select File")).grid(row=2, column=1, padx=10, pady=10)

        # EXTRACTION TARGET FOLDER ENTRY AND BROWSER
        self.extraction_target_path = tk.StringVar()
        entry = tk.Entry(extraction_tab, textvariable=self.extraction_target_path, width=50)
        entry.grid(row=3, column=1, padx=10, pady=10)
        entry.config(state="disabled")

        tk.Button(extraction_tab, text="Select Target Directory", command=lambda: self.browse_directories(self.extraction_target_path, "Select Folder")).grid(row=4, column=1, padx=10, pady=10)

        # EXTRACT
        tk.Button(extraction_tab, text="Extract", command=self.extract).grid(row=6, column=1, padx=10, pady=10)

    
    def reset_menus(self) -> None:
        """ Resets all entries in all menus to blank.  
        
        Returns
        -------
        None
        """

        self.compression_file_path.set("")
        self.compression_target_path.set("")

        self.extraction_file_path.set("")
        self.extraction_target_path.set("")

    
    # ***** TOP_MENU ACTIONS *****

    def encoding_stats(self) -> None:
        """ Creates a new window with the current huffman tree's statistics and binary encoding information. 
        
        Returns
        -------
        None
        """
        
        # Creating the new window.
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Encoding and Statistics")

        # Displaying the stats and encoding.

        row, column = 0, 0
        for i in range(len(self.encoder.char_to_bin_index.keys())):
            row, column = i%10, i//10
            char = list(self.encoder.char_to_bin_index.keys())[i]
            val = self.encoder.char_to_bin_index[char]
            tk.Label(stats_window, text=f"{char}: {val}").grid(row=row, column=column, padx=10, pady=10)
        tk.Button(stats_window, text="Close", command=stats_window.destroy).grid(row=row+1, column=0, padx=10, pady=10)

    def new_huffman_tree(self) -> None:
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
            messagebox.showerror("Error", "Please select a valid file.")
            return None 
        
        # Generate the new huffman tree.
        try:
            with open(path.get(), 'r') as file:
                self.encoder.set_huffman(file.read())
                messagebox.showinfo("Success", "A new huffman encoding was successfully generated.")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred with the selected file.")
            print(e)
        
        return None

    def open_huffman_tree(self) -> None:
        """ 
        
        Returns
        -------
        None
        """

        path = tk.StringVar()

        # Ask the user for the huffman tree json save.
        try:
            self.browse_files(path, [("JSON File", "*.json")], "Open File")
        except Exception as e:
            messagebox.showerror(title="Error", message="Please select a valid file.")
            print(e)
            return None

        # Load the save into the encoder.
        try:
            self.load_save(path.get())
            messagebox.showinfo("Success", "The huffman encoding was successfully loaded.")
        except Exception as e:
            messagebox.showerror(title="Error", message="The huffman encoding failed to load.")
            print(e)

        return None 

    def save_huffman_tree(self) -> None:
        """ Generates a new huffman tree and a new corresponding binary encoding for future compressions and extractions.
        
        Returns
        -------
        None
        """
        
        path = tk.StringVar()

        # Ask the user for the directory in which to save the huffman tree json file.
        try:
            self.save_file(path=path, title="Save File As", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        except Exception as e:
            messagebox.showerror(title="Error", message="Please select a valid file.")
            print(e)
            return None

        # Save the huffman encoding in the directory as a json file.
        try:
            self.create_save(path.get())
            messagebox.showinfo("Success", "The current huffman encoding was successfully saved.")
        except Exception as e:
            messagebox.showerror("Error", "The current huffman encoding failed to save.")
            print(e)

        return None

    def help(self) -> None:
        """ Creates a new window with the "help" information.

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
            tk.Label(help_window, text=help_text).grid(row=0, column=0, padx=10, pady=10)
            tk.Button(help_window, text="Close", command=help_window.destroy).grid(row=1, column=0, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Error", "The UI failed to display.")
            print(e)

    
    # ***** COMPRESSION_MENU ACTIONS *****

    def browse_files(self, path:tk.StringVar, filetype:list, title:str='') -> None:
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
            file_path = filedialog.askopenfilename(title=title, filetype=filetype)
            if file_path:
                path.set(file_path)
        except Exception as e:
            return e 

    
    def save_file(self, path:tk.StringVar, filetype:list, defaultextension:str=".json", title:str='') -> None:
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
            file_path = filedialog.asksaveasfilename(title=title, defaultextension=".json", filetypes=filetype)
            if file_path:
                path.set(file_path)
        except Exception as e:
            return e

    def browse_directories(self, path:tk.StringVar, title:str='') -> None:
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
            return e


    def compress(self) -> None:
        """ Gets the file to compress and compresses it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        # Get text file to compress and compress.
        if not self.compression_file_path:
            return 1
        
        res = None
        with open(self.compression_file_path.get(), 'r') as file:
            res = self.encoder.encode(file.read())

        # Get target directory to save the compressed file, and write the compressed file.
        if not self.compression_target_path:
            self.compression_target_path = ""

        with open(f"{self.compression_target_path.get()}/compressed.bin", 'wb') as file:
            file.write(res)
        
        messagebox.showinfo("Success", f"File succesfully encoded to: {self.compression_target_path.get()}/compressed.bin")
        self.reset_menus()
    
    def extract(self) -> int: 
        """ Gets the file to extract and extracts it to the directory file. 

        Returns
        -------
        int
            Error code with 0 being successful and 1 pointing to an error.
        """

        # Get text file to extract, and extract.
        if not self.extraction_file_path:
            return 1
        
        res = None
        with open(self.extraction_file_path.get(), 'rb') as file:
            res = self.encoder.decode(file.read())

        # Get target directory to save the extracted file, and write the extracted file.
        if not self.extraction_target_path:
            self.extraction_target_path = ""

        with open(f"{self.extraction_target_path.get()}/extracted.txt", 'w') as file:
            file.write(res)
            
        messagebox.showinfo("Success", f"File succesfully extracted to: {self.extraction_target_path.get()}/extracted.txt")
        self.reset_menus()
        return 0
    
    def create_save(self, path:str):
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
                data = [self.encoder.char_to_bin_index, self.encoder.bin_to_char_index]
                json.dump(data, json_file, indent=4)
        except Exception as e:
            return str(e)
    
    def load_save(self, path:str):
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
                    self.encoder.char_to_bin_index, self.encoder.bin_to_char_index = data[0], data[1]
            else:
                return None
        except Exception as e:
            return e

    # ***** Run *****

    def run(self):
        self.root.mainloop()
