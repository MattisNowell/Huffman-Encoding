from collections import Counter
import string
from abc import ABC, abstractmethod
from typing import Optional

from node import Leaf, Inner

class EncoderNoneError(Exception):
    """ Exception raised when the encoder value is None. 
    
    Attributes
    ----------
    None

    Methods
    -------
    None
    """

    def __init__(self, message = "Encoder value is None."):
        """ Initializes the EncoderNoneError class.
        """
        super().__init__(message)

class Encoder(ABC):    
    """ Abstract class to represent an encoder.
    
    Attributes
    ----------
    None
    
    Methods
    -------
    init() -> None
        Initializes the encoder.
        
    encode() -> None
        Encodes a file.
    
    decode() -> None
        Decodes a file.
    """

    @abstractmethod
    def init(self):
        """ Initializes the encoder.
        """
        pass

    @abstractmethod
    def encode(self):
        """ Encodes a file.

        """
        pass

    @abstractmethod
    def decode(self):
        """ Decodes a file.
        """
        pass

class Huffman(Encoder):
    """ Class to represent a Huffman encoder.

    Attributes
    ----------
    char_to_bin_index : dict
        A dictionary that maps characters to their binary representation.
    bin_to_char_index : dict
        A dictionary that maps binary values to their corresponding characters.
    char_percentages : dict
        A dictionary that maps characters to their percentage of appearance in the text.
    root : Inner
        The root node of the Huffman tree.
    
    Methods
    -------
    bit_to_byte(bin_string:str) -> bytes
        Converts a string type variable that contains a sequence of bits into a bytes type variable that contains the corresponding byte representation.
    byte_to_bit(byte_content:bytes) -> str
        Converts a list type variable that contains a sequence of bytes into a string type variable that contains the corresponding bit representation.
    get_char_percentages(text:str, fill:bool=False) -> dict
        Calculates the percentage of appearance of each character in the given text file.
    init(text:str) -> None
        Computes the Huffman tree data structure.
    encode(text:str) -> bytearray
        Encodes the given text file into a byte array following the Huffman Encoding method.
    decode(byte_content:bytes) -> str
        Decodes the given byte array into a character string following the Huffman coding method.
    """

    def __init__(self, text:Optional[str]) -> None:
        """Initializes the Huffman encoder.
        
        Parameters
        ----------
        text : str
            Text to generate the huffman tree from.
        
        Returns
        -------
        None
        """

        self.char_to_bin_index = None
        self.bin_to_char_index = None
        if text is not None:
            self.init(text=text)

    @staticmethod
    def bit_to_byte(bin_string: str) -> bytes:
        """ Converts a string type variable that contains a sequence of bits into a bytes type variable that contains the
        corresponding byte representation.

        Parameters
        ----------
        bin_string : str
            Binary string to be converted into the bytes data type.

        Returns
        -------
        bytes
            The bytes representation of the binary string.
        """

        if len(bin_string) % 8 != 0:
            bin_string = bin_string + '0' * (len(bin_string) % 8) 

        byte_content = []
        for chunk_position in range(0, len(bin_string) - 8, 8):
            chunk = bin_string[chunk_position:chunk_position+8]
            byte_content.append(int(chunk, 2)) # Converting the chunk into base 2 integer.

        return bytes(byte_content)

    @staticmethod
    def byte_to_bit(byte_content: bytes) -> str:
        """ Converts a list type variable that contains a sequence of bytes into a string type variable that contains the
        corresponding bit representation.

        Parameters
        ----------
        byte_content : bytes
            Bytes content to convert into a binary string.

        Returns
        -------
        str
            A binary value as a string.
        """

        bin_string = bin(int.from_bytes(byte_content, 'big'))[2:]
        while len(bin_string) % 8 != 0:
            bin_string = '0' + bin_string
        return bin_string
    
    @staticmethod
    def get_char_percentages(text:str, fill:bool=False) -> dict:
        """Calculates the percentage of appearance of each character in the given text file. 

        Parameters
        ----------
        text : str
            Text string to retrieve the percentages of character appearance from. The file must be an opened file of the 'file' type. 

        Returns
        -------
        dict
            A dictionnary with each unique character as the keys and their percentage of appearance as values.
        """

        # Get all necessary preliminary values:
        total_char_number = len(text)
        char_counter = dict(Counter(text))

        # Compute percentages on the input text characters:
        percentage_dict: dict = {}
        for char in char_counter:
            percentage_dict[char] = (char_counter[char] / total_char_number) * 100
            
        if fill:
            # Add other non-encountered ASCII characters.
            for char in string.printable:
                if char not in percentage_dict.keys():
                    percentage_dict[char] = 0.0
        
        # Return the percentage dictionnary sorted in ascending order:
        return dict(sorted(percentage_dict.items(), key=lambda x: x[1]))

    def init(self, text:str) -> None:
        """Computes the Huffman tree data structure. For more details on the logic behind the Huffman tree, see: https://en.wikipedia.org/wiki/Huffman_coding   

        Parameters
        ----------
        text_file : file
            Text file to compute the huffman tree from. The file must be an opened file of the 'file' type. 

        Returns
        -------
        None
        """

        # Huffman Tree: 
        self.char_percentages = Huffman.get_char_percentages(text, fill=True)
        nodes = list([Leaf(char=char, probability=self.char_percentages[char]) for char in self.char_percentages])

        while len(nodes) > 1:
            nodes.append(Inner(first_child_node=nodes[0], second_child_node=nodes[1]))
            nodes = sorted(nodes[2::], key=lambda x: x.probability)
        self.root = nodes[0]

        # Character to Binary index:
        self.char_to_bin_index = {}

        for char in string.printable:
            if char not in self.char_to_bin_index:
                char_to_bin = ''
                current_node = self.root
                # As long as base leaf not reached:
                while isinstance(current_node, Inner):
                    # Follow tree down and add binary path.
                    if char in current_node.first_child_node.chars:
                        current_node = current_node.first_child_node
                        char_to_bin += str(current_node.binary_id)
                    else:
                        current_node = current_node.second_child_node
                        char_to_bin += str(current_node.binary_id)
                self.char_to_bin_index[char] = char_to_bin
    
        self.bin_to_char_index = {binary: char for char, binary in self.char_to_bin_index.items()}

    def encode(self, text:str) -> bytearray:
        """Encodes the given text file into a byte array following the Huffman Encoding method. For more details on the Huffman Encoding method, see: https://en.wikipedia.org/wiki/Huffman_coding

        Parameters
        ----------
        text : str
            Text string to encode. The file must be an opened file of the 'file' type. 
       
        Returns
        -------
        bytearray
            The encoded text file as a sequence of bytes.
        """

        if not self.char_to_bin_index:
            raise EncoderNoneError 

        bin_encoding = ''
        for char in text:
            bin_encoding += self.char_to_bin_index[char]

        # Converting the binary data into byte arrays.
        byte_series = Huffman.bit_to_byte(bin_encoding)
            
        # Returning the byte array. 
        return byte_series
    
    def decode(self, byte_content:bytes) -> str:
        """Decodes the given byte array into a character string following the Huffman coding method. For more details on the Huffman Encoding method, see: https://en.wikipedia.org/wiki/Huffman_coding

        Parameters
        ----------
        byte_array : bytearray
            Byte array to decode.
       
        Returns
        -------
        str
            The decoded text string.
        """

        if not self.bin_to_char_index:
            raise EncoderNoneError 

        # Converting the byte array into a binary value stored as a string. 
        bin_string = Huffman.byte_to_bit(byte_content)
        text = ''
        
        # Iterating through the binary content to extract characters following the index. 
        left, right = 0, 1
        while right < len(bin_string):
            if bin_string[left:right] in self.bin_to_char_index:
                text += self.bin_to_char_index[bin_string[left:right]] 
                left = right
            right += 1
        
        return text