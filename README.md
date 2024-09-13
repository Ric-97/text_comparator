# Text Comparison App

This Streamlit application allows users to upload a PKL file containing text data and compare different texts or processed versions of the same text. It provides a visual comparison of the differences and allows for downloading a PDF report of the comparison.

## Features

- Upload PKL files containing text data
- Select and compare two texts or a text and its processed version
- Visual highlighting of differences between texts
- Generate and download a PDF report of the text comparison

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/text-comparison-app.git
   cd text-comparison-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501)

3. Upload a PKL file using the file uploader in the app

4. Select the texts you want to compare using the dropdown menus

5. View the comparison results and download the PDF report if desired

## Data Format

The uploaded PKL file should contain a pandas DataFrame with the following columns:
- content_id
- key
- processed_text
- text
- title
- category
- publication_date

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.