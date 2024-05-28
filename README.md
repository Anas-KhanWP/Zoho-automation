# Zoho Automation Tool

## Overview
The Zoho Automation Tool is a Python-based application designed to automate the execution of Zoho functions. It allows users to specify a range of functions to execute, streamlining repetitive tasks and increasing efficiency. With this tool, you can execute a sequence of functions by simply providing the function name and the range of numbers.

## Features
- **Automated Function Execution**: Execute a series of Zoho functions based on a specified range.
- **User-Friendly Interface**: Simple fields to input the function name and range for easy setup.
- **Batch Processing**: Run multiple functions in a single operation.

## Fields
The tool has three primary fields:
1. **Function Name**: The base name of the Zoho function.
2. **Minimum Number**: The starting number of the function sequence.
3. **Maximum Number**: The ending number of the function sequence.

## How It Works
1. **Input the Function Name**: Enter the base name of the Zoho function you want to execute. For example, "Zoho Function".
2. **Specify the Range**: Enter the minimum and maximum numbers for the function range.
   - **Minimum Number**: The number where the sequence starts (e.g., 1).
   - **Maximum Number**: The number where the sequence ends (e.g., 99).

When executed, the tool will automatically run each function in the specified range. For instance, if you input "Zoho Function" with a range from 1 to 99, it will execute "Zoho Function 1" through "Zoho Function 99".

## Example
To automate the execution of functions from "Zoho Function 1" to "Zoho Function 99":

- **Function Name**: Zoho Function
- **Minimum Number**: 1
- **Maximum Number**: 99

The tool will execute:
- Zoho Function 1
- Zoho Function 2
- ...
- Zoho Function 99

## Installation
To install and set up the Zoho Automation Tool, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Anas-KhanWP/Zoho-automation.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Zoho-automation
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To use the Zoho Automation Tool, follow these steps:

1. Launch the tool:
    ```bash
    python ui.py
    ```
2. Fill in the fields in the user interface:
   - **Function Name**: Enter the base name of the Zoho function.
   - **Minimum Number**: Enter the starting number of the function sequence.
   - **Maximum Number**: Enter the ending number of the function sequence.
3. Click the "Execute" button to start the automation.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or issues, please contact us at anaskhanwp@gmail.com.

---

Thank you for using the Zoho Automation Tool! We hope it significantly enhances your workflow with Zoho functions.
