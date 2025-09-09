# GPT Analyzer

<img width="700" height="350" alt="image" src="https://github.com/user-attachments/assets/0949ae93-f991-4423-b6bf-a694df7444d3" />


## Overview
GPT Analyzer is an interactive tool designed to simplify data analysis for everyone. It uses OpenAI's GPT models to generate Python code for analyzing CSV files, executes the code securely in Docker, and provides results and visualizations.


## Features
- **Drag-and-Drop CSV Upload**: Upload your data files effortlessly.
- **Interactive Chat Interface**: Ask questions about your data and get instant insights.
- **Automated Code Generation**: Generates Python code tailored to your analysis needs.
- **Secure Execution**: Runs code in a Docker container for safety.
- **Visualization Support**: Creates charts and saves them as `output.png`.

## Images

<img width="1879" height="857" alt="a1" src="https://github.com/user-attachments/assets/6d3e1803-9b42-4bea-a1b9-09c0828508f5" />

<img width="1838" height="594" alt="a2" src="https://github.com/user-attachments/assets/847a0d89-fa40-4812-940d-9bbdd6ff217b" />

<img width="1759" height="685" alt="a3" src="https://github.com/user-attachments/assets/2966c1d0-758c-4e3c-b9e6-fc7372d0c553" />

## Technologies Used
- **Streamlit**: For the user-friendly web interface.
- **OpenAI GPT Models**: For generating Python code dynamically.
- **Docker**: For secure and isolated code execution.
- **Python**: Backend logic and data processing.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GPT_Analyzer.git
   cd GPT_Analyzer
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open the app in your browser (usually at `http://localhost:8501`).
3. Upload a CSV file and interact with the chat interface to analyze your data.

## Example Workflow
1. **Upload a CSV File**: Drag and drop your file into the app.
2. **Ask Questions**: Use the chat interface to ask questions like "How many rows are in my data?".
3. **View Results**: See the generated Python code, execution results, and visualizations.




