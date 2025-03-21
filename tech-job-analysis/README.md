# Download and Analyze Your Google Sheet


## Option 1: Manual Download and Analysis

### Step 1: Download your Google Sheet as CSV

1. Open your Google Sheet (with ID: `1aGaGfPucJ-hmmnDHWZs2YQ2sF2IhE3H6PPw-_OiC38Y`)
2. Go to **File** → **Download** → **Comma Separated Values (.csv)**
3. Save the CSV file to your project directory (example: `job_data.csv`)

### Step 2: Use the simplified script to analyze your data

I've created a fixed script that gives you two options:
1. Analyze a local CSV file (perfect for the file you just downloaded)
2. Try the Google Sheets API approach again (if you want to set up service account credentials)

## Running the Analysis

1. Save the provided Python script as `job_analysis.py`
2. Make sure all required packages are installed:
   ```bash
   pip install pandas matplotlib seaborn
   ```
3. Run the script:
   ```bash
   python job_analysis.py
   ```
4. When prompted, select option 1 (for CSV file)
5. Enter the path to your downloaded CSV file

## What the Analysis Will Include

The script will analyze your job postings data and generate:

1. **Visualizations**:
   - Job categories breakdown
   - Top companies hiring
   - Top job locations
   - Hashtag analysis

2. **A Comprehensive Report** with insights about:
   - Overall job market trends
   - Most in-demand job categories
   - Companies with the most job postings
   - Geographic distribution of jobs
   - Popular hashtags used in job postings

3. **Cleaned Data** for further analysis

All output files will be saved to an 'output' directory in your project folder.

## Troubleshooting

If you encounter any issues with the script:

1. Make sure your CSV file is properly formatted with headers matching the original Google Sheet
2. Check that you have the required Python packages installed
3. Ensure you have write permissions in the directory where you're running the script

