import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def select_input_file():
    """Opens a file dialog for the user to select an input file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    filepath = filedialog.askopenfilename(
        title="Select Input Data File",
        filetypes=(
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        )
    )
    root.destroy() # Close the hidden window
    return filepath

def parse_input_file(filepath):
    """
    Reads data from the selected file (CSV, TXT, Excel) using pandas
    and attempts to extract Category and Value columns.

    Args:
        filepath (str): The path to the input file.

    Returns:
        dict: A dictionary with 'Category' as keys and 'Value' as values,
              or None if parsing fails.
    """
    if not filepath:
        print("No file selected.")
        return None

    try:
        filename, extension = os.path.splitext(filepath)
        extension = extension.lower()

        if extension in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
        elif extension in ['.csv', '.txt']:
            # Try CSV first, then tab-separated for TXT
            try:
                df = pd.read_csv(filepath)
            except pd.errors.ParserError:
                 try:
                     df = pd.read_csv(filepath, sep='\t')
                 except Exception as e:
                     print(f"Could not parse '{filepath}' as CSV or TSV: {e}")
                     return None
        else:
            print(f"Unsupported file type: {extension}")
            return None

        if df.empty:
            print("The selected file is empty.")
            return None

        # --- Identify Category and Value columns ---
        category_col = None
        value_col = None
        possible_cat_cols = ['category', 'label', 'name', 'item']
        possible_val_cols = ['value', 'amount', 'count', 'quantity', 'number']

        df_cols_lower = [str(col).lower() for col in df.columns]

        # Try finding specific names
        for col_name in possible_cat_cols:
            if col_name in df_cols_lower:
                category_col = df.columns[df_cols_lower.index(col_name)]
                break
        for col_name in possible_val_cols:
            if col_name in df_cols_lower:
                value_col = df.columns[df_cols_lower.index(col_name)]
                break
        
        # Fallback to first two columns if specific names not found
        if category_col is None and len(df.columns) > 0:
            category_col = df.columns[0]
            print(f"Warning: Could not find a typical category column name. Using first column: '{category_col}'")
        if value_col is None and len(df.columns) > 1:
             # Ensure the value column is different from the category column
            if category_col == df.columns[1]:
                 if len(df.columns) > 2:
                     value_col = df.columns[2]
                     print(f"Warning: Category and default value columns are the same. Using third column: '{value_col}'")
                 else:
                     print("Error: Cannot determine distinct category and value columns.")
                     return None
            else:
                value_col = df.columns[1]
                print(f"Warning: Could not find a typical value column name. Using second column: '{value_col}'")


        if category_col is None or value_col is None:
            print("Error: Could not identify both Category and Value columns in the file.")
            return None

        print(f"Identified Category column: '{category_col}'")
        print(f"Identified Value column: '{value_col}'")

        # --- Extract data into dictionary ---
        data_dict = {}
        skipped_rows = 0
        for index, row in df.iterrows():
            category = row[category_col]
            value = row[value_col]

            # Basic validation
            if pd.isna(category) or not str(category).strip():
                skipped_rows += 1
                continue
            if pd.isna(value):
                 skipped_rows += 1
                 continue

            category_str = str(category).strip()

            try:
                # Convert value to numeric, handling potential errors
                numeric_value = pd.to_numeric(value)
                if pd.isna(numeric_value): # Check again after conversion
                    skipped_rows += 1
                    continue
                data_dict[category_str] = float(numeric_value)
            except (ValueError, TypeError):
                 skipped_rows += 1
                 continue # Skip if value cannot be converted to numeric

        if skipped_rows > 0:
            print(f"Warning: Skipped {skipped_rows} rows due to missing or invalid data.")
            
        if not data_dict:
             print("No valid data could be extracted from the file.")
             return None

        return data_dict

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading or parsing file {filepath}: {e}")
        return None


def format_data_to_csv(data_dict, output_filename="formatted_data.csv"):
    """
    Converts a dictionary of category-value pairs into the CSV format
    required by the VR Bar Chart Visualizer. (Handles validation internally)

    Args:
        data_dict (dict): A dictionary where keys are category names (str)
                          and values are numerical values (int or float).
        output_filename (str): The name of the CSV file to create.
    """
    if not isinstance(data_dict, dict):
        # This check might be redundant if parse_input_file always returns a dict or None
        print("Error: Invalid data provided for CSV formatting.")
        return False # Indicate failure
    if not data_dict:
        print("Warning: Input data is empty. Creating an empty CSV with header.")
        # Allow creating header-only file

    # Determine output path relative to the script's location
    script_dir = os.path.dirname(__file__) if __file__ else '.'
    output_filepath = os.path.join(script_dir, output_filename)

    header = ['Category', 'Value']
    rows = []
    invalid_entries = 0

    for category, value in data_dict.items():
        # Re-validate just in case, though parse_input_file should handle most cases
        if not isinstance(category, str) or not category.strip():
            invalid_entries += 1
            continue
        if not isinstance(value, (int, float)):
             try:
                 value = float(value)
             except (ValueError, TypeError):
                 invalid_entries += 1
                 continue

        processed_value = abs(value) # Use absolute value
        rows.append([category.strip(), processed_value])

    if invalid_entries > 0:
         print(f"Warning: {invalid_entries} invalid entries skipped during final formatting.")

    try:
        with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            if rows: # Only write rows if there are any valid ones
                writer.writerows(rows)
        print(f"Successfully created formatted CSV file: {output_filepath}")
        return True # Indicate success
    except IOError as e:
        print(f"Error writing to CSV file {output_filepath}: {e}")
        return False # Indicate failure
    except Exception as e:
        print(f"An unexpected error occurred during CSV writing: {e}")
        return False # Indicate failure

# --- Main Execution ---
if __name__ == "__main__":
    print("Please select the input data file (Excel, CSV, TXT)...")
    input_filepath = select_input_file()

    if input_filepath:
        print(f"Selected input file: {input_filepath}")
        parsed_data = parse_input_file(input_filepath)

        if parsed_data:
            # Suggest an output filename
            base_name = os.path.basename(input_filepath)
            name_part, _ = os.path.splitext(base_name)
            default_output_name = f"{name_part}_formatted.csv"

            # Ask user for output filename, providing the default
            output_name_prompt = f"Enter the desired output filename (default: {default_output_name}): "
            user_output_name = input(output_name_prompt).strip()

            # Use default if user input is empty, otherwise use user's input
            final_output_name = user_output_name if user_output_name else default_output_name

            # Ensure the filename ends with .csv
            if not final_output_name.lower().endswith('.csv'):
                final_output_name += ".csv"

            print(f"Attempting to save formatted data to: {final_output_name}")
            format_data_to_csv(parsed_data, final_output_name)
        else:
            print("Could not parse data from the selected file.")
    else:
        print("File selection cancelled.")

    # Keep console open until user presses Enter
    input("\nPress Enter to exit...")
