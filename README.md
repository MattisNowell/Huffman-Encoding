# Huffman Encoding Project

## Introduction
This project implements Huffman Encoding, a popular algorithm used for lossless data compression. The goal is to efficiently compress data by assigning shorter codes to more frequent characters.

## Features
- **New Encoder**: Create a new Huffman encoder from a text file.
- **Open Encoder**: Open an existing Huffman encoder from a saved file.
- **Save Encoder**: Save the current Huffman encoder to a file.
- **Compress File**: Compress a text file using the current Huffman encoder.
- **Extract File**: Extract a compressed file using the current Huffman encoder.
- **Encoding Statistics**: View statistics and binary encoding information for the current Huffman encoder.
- **Help**: Access help information about the application.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Huffman-Encoding.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Huffman-Encoding
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```bash
    python main.py
    ```
    or execute the `.exe` file if available.
2. Follow the on-screen menu to:
    - Encode a file
    - Decode a file
    - Display character frequencies
