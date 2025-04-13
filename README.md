# 3D Bar Chart VR Visualizer

Visualize CSV data as an interactive 3D bar chart in a web-based VR environment using A-Frame.

## Description

This project allows users to upload a simple CSV file containing categories and values, which are then rendered as a 3D bar chart. Users can navigate the scene, interact with the chart bars and legend, and switch between different viewpoints. It supports both desktop browsers and VR headsets compatible with WebXR.

A Python script (`csv_formatter.py`) is included to help convert data from various formats (Excel, CSV, TXT) into the required CSV structure.

## Features

*   **Data Preparation Script:** Convert Excel, CSV, or TXT files into the required format using `csv_formatter.py`.
*   **CSV Upload:** Load data from a local CSV file (specifically formatted).
*   **3D Bar Chart:** Renders data as dynamically sized bars.
*   **Interactive Legend:** Displays categories and colors, scrollable for large datasets, and highlights corresponding bars on hover.
*   **Bar Highlighting:** Bars highlight on hover, showing their category and value. Legend items also highlight corresponding bars.
*   **Multiple Viewpoints:** Predefined camera positions for front, top, and side views.
*   **VR & Desktop Support:** Works in standard desktop browsers (with mouse/keyboard controls) and VR headsets (using WebXR).
*   **Floating UI Panel:** Provides a quick reference for keyboard shortcuts.
*   **Feedback Messages:** Displays status updates and error messages.

## Data Preparation (`csv_formatter.py`)

If your data is not already in the required CSV format (see below), you can use the included Python script `csv_formatter.py` to convert it.

**Purpose:** Reads data from Excel (`.xlsx`, `.xls`), CSV (`.csv`), or Text (`.txt` - attempts comma-separated, then tab-separated) files and attempts to extract 'Category' and 'Value' columns. It then saves the data into a new CSV file formatted correctly for the visualizer.

**Requirements:**

*   Python 3.x
*   `pandas` library

**Installation:**

1.  Make sure you have Python installed.
2.  Navigate to the project directory in your terminal or command prompt.
3.  Install the required library:

    ```bash
    pip install -r requirements.txt
    ```

**Usage:**

1.  Run the script from the project directory:

    ```bash
    python csv_formatter.py
    ```
    
2.  A file dialog will open. Select your input data file (Excel, CSV, or TXT).
3.  The script will attempt to identify columns named 'Category'/'Label'/'Name'/'Item' and 'Value'/'Amount'/'Count'/'Quantity'/'Number' (case-insensitive). If these are not found, it will try using the first two columns.
4.  Follow the prompts in the terminal to specify an output filename for the formatted CSV (a default name will be suggested).
5.  The script will create the new, correctly formatted CSV file in the project directory.

**Note:** Use the CSV file generated by this script for uploading into the web visualizer.

## How to Use (Web Visualizer)

1.  **Prepare Data:** Ensure your data is in the correct CSV format (see below). Use the `csv_formatter.py` script if needed.
2.  **Serve the Files:** You need a local web server to run `index.html` due to browser security restrictions on loading local files (`file:///`).
    *   If you have Node.js installed, you can use `npx http-server` in the project directory.
    *   Alternatively, use an extension like "Live Server" for VS Code (which seems to be configured in `.vscode/settings.json` to use port 5501).
3.  **Open in Browser:** Navigate to the local server address (e.g., `http://localhost:5501` or `http://127.0.0.1:5501`) in a WebXR-compatible browser (like Chrome, Edge, Firefox, or Oculus Browser).
4.  **Upload Data:**
    *   Click the "Upload CSV" button (either the one in the scene or the fallback button on desktop).
    *   Select the **correctly formatted** CSV file from your computer (e.g., `sample_data.csv` or one generated by `csv_formatter.py`).
5.  **Explore:**
    *   Use WASD keys and mouse drag (or VR controllers) to move around.
    *   Hover over bars or legend items to see details.
    *   Use the viewpoint buttons or keyboard shortcuts to change perspective.
    *   Use PageUp/PageDown, ',', '.', or the mouse wheel (while hovering over the legend) to scroll the legend if needed.
    *   Click the floating '☰' icon to toggle the shortcut help panel.

## CSV Format (Required by Web Visualizer)

The CSV file uploaded to the web visualizer **must** adhere to the following format. The `csv_formatter.py` script can help generate files in this format from other sources.

*   **Header Row:** The first row must be exactly `Category,Value` (case-insensitive).
*   **Data Rows:** Each subsequent row should contain two columns:
    *   Column 1: The category name (string). Cannot be empty.
    *   Column 2: The numerical value. Must be a valid number. Negative values will have their absolute value used for bar height.
*   **Comments:** Lines starting with `//` will be ignored.

**Example (`sample_data.csv`):**

```csv
Category,Value
Food,15
Transport,25
Housing,45
Entertainment,18
Education,30
Healthcare,20
Clothing,10
Utilities,12
```

## Keyboard Shortcuts

*   **W, A, S, D:** Move the camera (desktop).
*   **Mouse Drag:** Look around (desktop).
*   **U:** Trigger CSV file upload.
*   **R:** Reset the chart and clear data.
*   **1:** Switch to Front View.
*   **2:** Switch to Top View.
*   **3:** Switch to Side View.
*   **PageUp / . (Period):** Scroll legend up.
*   **PageDown / , (Comma):** Scroll legend down.
*   **Tab:** Toggle the floating shortcut help panel.

## Deployment to GitHub Pages

This project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) to automatically deploy the visualizer to GitHub Pages.

**Setup:**
1.  **Push to GitHub:** Ensure your project code, including the `.github` directory, is pushed to a GitHub repository.
2.  **Enable Pages:** In your GitHub repository settings:
    *   Go to the "Pages" section (usually under "Code and automation").
    *   Under "Build and deployment", select "GitHub Actions" as the **Source**.
3.  **Trigger Deployment:** Push a change to your `main` branch (or the default branch specified in the workflow file). The GitHub Actions workflow will automatically run.
4.  **View Site:** Once the action completes successfully, your site will be available at the URL provided in the Pages settings (e.g., `https://<your-username>.github.io/<your-repository-name>/`).

## Technologies Used

*   [A-Frame](https://aframe.io/): Web framework for building virtual reality experiences.
*   HTML, CSS, JavaScript
*   Python 3.x (for data preparation script)
*   Pandas (Python library, for data preparation script)
*   GitHub Actions (for deployment)
