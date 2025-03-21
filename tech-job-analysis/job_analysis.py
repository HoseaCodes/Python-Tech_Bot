import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set the style for plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)

# Make sure output directory exists
if not os.path.exists('output'):
    os.makedirs('output')
    print("Created output directory")

def analyze_spreadsheet_with_service_account(key_file_path, spreadsheet_id, sheet_name='Sheet1'):
    """
    Extract and analyze data from a Google Spreadsheet using a service account.
    
    Args:
        key_file_path: Path to the service account JSON key file
        spreadsheet_id: ID of the Google Spreadsheet
        sheet_name: Name of the sheet to analyze
        
    Returns:
        Tuple of (report text, cleaned DataFrame)
    """
    # Set up the range
    range_name = f"{sheet_name}!A1:Z1000"  # Adjust range as needed
    
    try:
        # Authenticate with service account
        credentials = service_account.Credentials.from_service_account_file(
            key_file_path, 
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        # Build the service
        service = build('sheets', 'v4', credentials=credentials)
        
        # Get the data
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        
        if not values:
            return "No data found in the spreadsheet.", None
        
        # Create pandas DataFrame
        headers = values[0]
        data = values[1:]
        df = pd.DataFrame(data, columns=headers)
        
        # Print column names to help with debugging
        print("Columns in the spreadsheet:", df.columns.tolist())
        
        # Clean and analyze the data
        clean_df = clean_data(df)
        report = generate_analysis_report(clean_df)
        
        # Save cleaned data
        clean_df.to_csv('output/cleaned_job_data.csv', index=False)
        
        with open('output/job_analysis_report.md', 'w') as f:
            f.write(report)
        
        return report, clean_df
        
    except Exception as e:
        error_msg = f"Error accessing Google Sheets: {str(e)}"
        print(error_msg)
        return error_msg, None

def clean_data(df):
    """Clean and preprocess the data."""
    # Create a copy to avoid modifying the original dataframe
    clean_df = df.copy()
    
    # Convert all column names to string
    clean_df.columns = clean_df.columns.astype(str)
    
    # Handle missing values
    for col in clean_df.columns:
        if clean_df[col].dtype == 'object':
            clean_df[col] = clean_df[col].fillna('')
    
    # Try to convert date columns to datetime
    for col in clean_df.columns:
        if any(date_word in col.lower() for date_word in ['date', 'time', 'posted', 'created']):
            try:
                clean_df[col] = pd.to_datetime(clean_df[col], errors='coerce')
                
                # If conversion worked, add day of week
                if pd.api.types.is_datetime64_any_dtype(clean_df[col]):
                    clean_df['day_of_week'] = clean_df[col].dt.day_name()
                    break  # Only do this for the first valid date column
            except:
                pass
    
    # Extract job category from job title if available
    job_title_col = next((col for col in clean_df.columns if any(word in col.lower() for word in ['title', 'position', 'role'])), None)
    
    if job_title_col:
        def categorize_job(title):
            if pd.isna(title) or title == '':
                return 'Unknown'
                
            title = str(title).lower()
            if any(term in title for term in ['software', 'developer', 'full stack', 'frontend', 'backend', 'code', 'programmer']):
                return 'Software Development'
            elif any(term in title for term in ['network', 'cloud', 'systems', 'infrastructure', 'admin']):
                return 'Network Engineering'
            elif any(term in title for term in ['data', 'machine learning', 'analyst', 'analytics', 'scientist']):
                return 'Data Science'
            elif any(term in title for term in ['devops', 'reliability', 'site', 'ops']):
                return 'DevOps'
            elif any(term in title for term in ['product manager', 'product owner', 'project manager']):
                return 'Product Management'
            elif any(term in title for term in ['qa', 'test', 'quality']):
                return 'QA/Testing'
            elif any(term in title for term in ['security', 'cybersecurity', 'secure']):
                return 'Cybersecurity'
            elif any(term in title for term in ['ux', 'ui', 'design', 'user experience']):
                return 'UX/UI Design'
            else:
                return 'Other'
        
        clean_df['job_category'] = clean_df[job_title_col].apply(categorize_job)
    
    # Extract hashtags if available
    hashtag_col = next((col for col in clean_df.columns if any(word in col.lower() for word in ['hashtag', 'tag', 'keyword'])), None)
    
    if hashtag_col:
        clean_df['hashtag_list'] = clean_df[hashtag_col].apply(
            lambda x: re.findall(r'#\w+', str(x)) if not pd.isna(x) else []
        )
    
    # Extract skills from descriptions if available
    desc_col = next((col for col in clean_df.columns if any(word in col.lower() for word in ['description', 'desc', 'details', 'requirements'])), None)
    
    if desc_col:
        skills_to_extract = ['JavaScript', 'AWS', 'SQL', 'Java', 'DevOps', 'Python', 'React', 'Node.js',
                             'TypeScript', 'Docker', 'Kubernetes', 'HTML', 'CSS', 'Git', 'CI/CD',
                             'MongoDB', 'Redis', 'Linux', 'Agile', 'Scrum']
        
        for skill in skills_to_extract:
            clean_df[f'has_{skill.lower().replace(".", "")}'] = clean_df[desc_col].apply(
                lambda x: 1 if skill.lower() in str(x).lower() else 0
            )
    
    # Check if remote in location if available
    location_col = next((col for col in clean_df.columns if any(word in col.lower() for word in ['location', 'place', 'where'])), None)
    
    if location_col:
        clean_df['is_remote'] = clean_df[location_col].apply(
            lambda x: 1 if 'remote' in str(x).lower() else 0
        )
    
    return clean_df

def analyze_job_categories(df):
    """Analyze job categories and create visualization."""
    try:
        if 'job_category' not in df.columns:
            print("No job_category column found for category analysis")
            return None
            
        category_counts = df['job_category'].value_counts().reset_index()
        category_counts.columns = ['job_category', 'count']
        
        plt.figure(figsize=(12, 8))
        # Updated to avoid FutureWarning
        sns.barplot(x='count', y='job_category', data=category_counts, 
                palette='viridis', orient='h', hue='job_category', legend=False)
        plt.title('Job Postings by Category', fontsize=16)
        plt.xlabel('Number of Job Postings', fontsize=14)
        plt.ylabel('Job Category', fontsize=14)
        plt.tight_layout()
        plt.savefig('output/job_categories.png')
        print("Saved job categories visualization")
        
        return category_counts
    except Exception as e:
        print(f"Error in analyze_job_categories: {e}")
        return None

def analyze_top_companies(df):
    """Analyze top companies with the most job postings."""
    try:
        # Find the company column
        company_col = next((col for col in df.columns if any(word in col.lower() for word in ['company', 'employer', 'organization'])), None)
        
        if not company_col:
            print("No company column found for company analysis")
            return None
            
        company_counts = df[company_col].value_counts().head(10).reset_index()
        company_counts.columns = ['company', 'count']
        
        plt.figure(figsize=(12, 8))
        # Updated to avoid FutureWarning
        sns.barplot(x='count', y='company', data=company_counts, 
                palette='mako', orient='h', hue='company', legend=False)
        plt.title('Top 10 Companies with the Most Job Postings', fontsize=16)
        plt.xlabel('Number of Job Postings', fontsize=14)
        plt.ylabel('Company', fontsize=14)
        plt.tight_layout()
        plt.savefig('output/top_companies.png')
        print("Saved top companies visualization")
        
        return company_counts
    except Exception as e:
        print(f"Error in analyze_top_companies: {e}")
        return None

def analyze_locations(df):
    """Analyze job locations."""
    try:
        # Find the location column
        location_col = next((col for col in df.columns if any(word in col.lower() for word in ['location', 'place', 'where'])), None)
        
        if not location_col:
            print("No location column found for location analysis")
            return None
            
        location_counts = df[location_col].value_counts().head(10).reset_index()
        location_counts.columns = ['location', 'count']
        
        plt.figure(figsize=(12, 8))
        # Updated to avoid FutureWarning
        sns.barplot(x='count', y='location', data=location_counts, 
                palette='magma', orient='h', hue='location', legend=False)
        plt.title('Top 10 Job Locations', fontsize=16)
        plt.xlabel('Number of Job Postings', fontsize=14)
        plt.ylabel('Location', fontsize=14)
        plt.tight_layout()
        plt.savefig('output/top_locations.png')
        print("Saved top locations visualization")
        
        # Pie chart for remote vs. on-site if is_remote column exists
        if 'is_remote' in df.columns:
            remote_count = df['is_remote'].sum()
            onsite_count = len(df) - remote_count
            
            plt.figure(figsize=(10, 7))
            plt.pie([remote_count, onsite_count], labels=['Remote', 'On-site'], 
                autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99'])
            plt.title('Remote vs. On-site Jobs', fontsize=16)
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig('output/remote_vs_onsite.png')
            print("Saved remote vs. onsite visualization")
        
        return location_counts
    except Exception as e:
        print(f"Error in analyze_locations: {e}")
        return None

def analyze_hashtags(df):
    """Analyze hashtags used in job postings."""
    try:
        if 'hashtag_list' not in df.columns:
            print("No hashtags found for hashtag analysis")
            return None
            
        # Flatten list of hashtags
        all_hashtags = [tag for sublist in df['hashtag_list'] for tag in sublist]
        
        if not all_hashtags:
            print("No hashtags found for analysis")
            return None
            
        hashtag_counts = pd.Series(all_hashtags).value_counts().head(15).reset_index()
        hashtag_counts.columns = ['hashtag', 'count']
        
        plt.figure(figsize=(12, 8))
        # Updated to avoid FutureWarning
        sns.barplot(x='count', y='hashtag', data=hashtag_counts, 
                palette='crest', orient='h', hue='hashtag', legend=False)
        plt.title('Top 15 Hashtags in Job Postings', fontsize=16)
        plt.xlabel('Count', fontsize=14)
        plt.ylabel('Hashtag', fontsize=14)
        plt.tight_layout()
        plt.savefig('output/top_hashtags.png')
        print("Saved hashtags visualization")
        
        return hashtag_counts
    except Exception as e:
        print(f"Error in analyze_hashtags: {e}")
        return None

def generate_analysis_report(df):
    """Generate a comprehensive analysis report."""
    try:
        # Run all the analyses
        category_counts = analyze_job_categories(df)
        company_counts = analyze_top_companies(df)
        location_counts = analyze_locations(df)
        hashtag_counts = analyze_hashtags(df)
        
        report = "# Tech Job Market Analysis Report\n\n"
        
        report += "## Overview\n"
        report += f"This report provides an analysis of {len(df)} tech job postings from your Google Sheet. "
        report += "The analysis covers job categories, companies, locations, and hashtags.\n\n"
        
        # Date information
        date_col = next((col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])), None)
        if date_col:
            report += "## Job Posting Trends\n"
            report += f"Date range: {df[date_col].min().strftime('%Y-%m-%d') if not pd.isna(df[date_col].min()) else 'N/A'} to {df[date_col].max().strftime('%Y-%m-%d') if not pd.isna(df[date_col].max()) else 'N/A'}\n\n"
            
            # Analyze posting by date
            date_counts = df.groupby(df[date_col].dt.date).size().reset_index(name='count')
            if not date_counts.empty:
                # Find peak posting days
                peak_dates = date_counts.nlargest(3, 'count')
                report += "Peak posting dates:\n"
                for _, row in peak_dates.iterrows():
                    report += f"- {row[date_col].strftime('%Y-%m-%d')}: {row['count']} postings\n"
                report += "\n"
        
        # Category information
        if category_counts is not None and not category_counts.empty:
            report += "## Job Categories\n"
            top_categories = category_counts.head(5)
            report += "Top 5 job categories:\n"
            for _, row in top_categories.iterrows():
                report += f"- {row['job_category']}: {row['count']} postings\n"
            report += "\n"
        
        # Company information
        if company_counts is not None and not company_counts.empty:
            report += "## Top Companies\n"
            top_companies = company_counts.head(5)
            report += "Companies with the most job postings:\n"
            for _, row in top_companies.iterrows():
                report += f"- {row['company']}: {row['count']} postings\n"
            report += "\n"
        
        # Location information
        if location_counts is not None and not location_counts.empty:
            report += "## Geographic Distribution\n"
            top_locations = location_counts.head(5)
            report += "Top 5 job locations:\n"
            for _, row in top_locations.iterrows():
                report += f"- {row['location']}: {row['count']} postings\n"
            report += "\n"
            
            if 'is_remote' in df.columns:
                remote_count = df['is_remote'].sum()
                remote_percentage = (remote_count / len(df)) * 100
                report += f"Remote positions: {remote_count} ({remote_percentage:.1f}% of all postings)\n\n"
        
        # Hashtag information
        if hashtag_counts is not None and not hashtag_counts.empty:
            report += "## Hashtag Analysis\n"
            top_hashtags = hashtag_counts.head(10)
            report += "Top 10 hashtags used in job postings:\n"
            for _, row in top_hashtags.iterrows():
                report += f"- {row['hashtag']}: {row['count']} occurrences\n"
            report += "\n"
        
        report += "## Methodology\n"
        report += "This analysis was performed using Python with pandas for data manipulation and seaborn/matplotlib for visualization.\n"
        report += "The data was extracted from your Google Sheet, cleaned and processed to extract key dimensions including job categories, companies, and locations.\n\n"
        
        report += "## Visualizations\n"
        report += "All visualizations have been saved to the 'output' directory in your project folder.\n"
        
        return report
    except Exception as e:
        print(f"Error in generate_analysis_report: {e}")
        return f"Error generating report: {str(e)}"

def analyze_csv(csv_path):
    """Analyze a CSV file directly."""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path)
        
        # Print column names
        print("Columns in the CSV:", df.columns.tolist())
        
        # Clean and analyze the data
        clean_df = clean_data(df)
        report = generate_analysis_report(clean_df)
        
        # Save cleaned data
        clean_df.to_csv('output/cleaned_job_data.csv', index=False)
        
        # Save report
        with open('output/job_analysis_report.md', 'w') as f:
            f.write(report)
        
        return report, clean_df
    except Exception as e:
        error_msg = f"Error analyzing CSV: {str(e)}"
        print(error_msg)
        return error_msg, None

if __name__ == "__main__":
    # Download the spreadsheet as CSV option
    print("Do you want to analyze:")
    print("1. A locally saved CSV file")
    print("2. Google Spreadsheet (requires service account key)")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        # Local CSV file
        csv_path = input("Enter the path to your CSV file: ")
        print(f"Analyzing CSV file: {csv_path}")
        report, df = analyze_csv(csv_path)
    else:
        # Google Sheet
        key_file = input("Enter the path to your service account key file (or press Enter to skip): ")
        if not key_file:
            print("No key file provided. Using default 'service_account_credentials.json'")
            key_file = 'service_account_credentials.json'
        
        spreadsheet_id = input("Enter your Google Spreadsheet ID (or press Enter to use default): ")
        if not spreadsheet_id:
            spreadsheet_id = '1aGaGfPucJ-hmmnDHWZs2YQ2sF2IhE3H6PPw-_OiC38Y'
            print(f"Using default spreadsheet ID: {spreadsheet_id}")
        
        sheet_name = input("Enter sheet name (or press Enter for 'Sheet1'): ")
        if not sheet_name:
            sheet_name = 'Sheet1'
            print(f"Using default sheet name: {sheet_name}")
        
        print(f"Analyzing Google Sheet: {spreadsheet_id}, Sheet: {sheet_name}")
        report, df = analyze_spreadsheet_with_service_account(key_file, spreadsheet_id, sheet_name)
    
    # Print report
    print("\n" + report)
    
    print("\nAnalysis complete! Check the output directory for visualizations and the report.")