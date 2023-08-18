import re
import pandas as pd

# Load the data gathered using the webscraping script
with open('10-k_file.txt', 'r') as file:
    raw_10k = file.read()

# Apply REGEX to find target sections

def content_sections(text_file):
    ''' This function takes in a 10K text file and separates the 
    text content into different sections for analysis
    '''

    # Create a list of all the regex patters for the needed sections
    item1_pattern = re.compile(r'Item\s+1.\s+Business')
    item1a_pattern = re.compile(r'Item\s+1A.\s+Risk\s+Factors')
    item7_pattern = re.compile(r"Item\s+7.\s+Management’s\s+Discussion\s+and\s+Analysis\s+of\s+Financial\s+Condition\s+and\s+Results\s+of\s+Operations")
    item7a_pattern = re.compile(r"Item\s+7A.\s+Quantitative\s+and\s+Qualitative\s+Disclosures\s+About\s+Market\s+Risk")
    item8_pattern = re.compile(r"Item\s+8.\s+Financial\s+Statements\s+and\s+Supplementary\s+Data")
    item10_pattern = re.compile(r"Item\s+10.\s+Directors,\s+Executive\s+Officers\s+and\s+Corporate\s+Governance")
    item11_pattern = re.compile(r"Item\s+11.\s+Executive\s+Compensation")

    # Make a list of all the patterns for each section and the sections in the text that will match it

    #List of patterns for each section
    patterns = [item1_pattern, item1a_pattern, item7_pattern, item7a_pattern, item8_pattern, item10_pattern, item11_pattern]
    #List of sections that match the patterns
    matches = ['item1_matches', 'item1a_matches', 'item7_matches', 'item7a_matches', 'item8_matches', 'item10_matches', 'item11_matches'] 

    # Loop through all the patterns and store the matching section into test_df
    test_dfs = []
    for pattern, item_matches in zip(patterns, matches):
        item_matches = pattern.finditer(raw_10k)
        for match in item_matches:
            print(match)
            test_df = pd.DataFrame({'Section':match.group(), 'Start': match.start(), 'End': match.end()}, index=[0])
            test_dfs.append(test_df)
    
    # Concatenate all the dataframes into one dataframe and 
    # sort the values according to their order in the text file
    merged_df = pd.concat(test_dfs)
    merged_df = merged_df.sort_values(by='Start')
    merged_df.set_index('Section', inplace=True)

    # Create the separate sections
    Business = raw_10k[merged_df['Start'].loc['Item 1.    Business']: merged_df['End'].loc['Item 1A.    Risk Factors']]
    Risk_Factors = raw_10k[merged_df['Start'].loc['Item 1A.    Risk Factors']: merged_df['End'].loc['Item 7.    Management’s Discussion and Analysis of Financial Condition and Results of Operations']]
    MDA = raw_10k[merged_df['Start'].loc['Item 7.    Management’s Discussion and Analysis of Financial Condition and Results of Operations']: merged_df['End'].loc['Item 7A.    Quantitative and Qualitative Disclosures About Market Risk']]
    Market_Risk = raw_10k[merged_df['Start'].loc['Item 7A.    Quantitative and Qualitative Disclosures About Market Risk']: merged_df['End'].loc['Item 8.    Financial Statements and Supplementary Data']]
    Fin_Statements = raw_10k[merged_df['Start'].loc['Item 8.    Financial Statements and Supplementary Data']: merged_df['End'].loc['Item 10.    Directors, Executive Officers and Corporate Governance']]
    DEOC = raw_10k[merged_df['Start'].loc['Item 10.    Directors, Executive Officers and Corporate Governance']:merged_df['End'].loc['Item 11.    Executive Compensation']]

    # Store the sections and their contents into a dataframe
    df_10K = pd.DataFrame({
        'Company Name': 'Apple Inc.',
        'TIC': 'AAPL',
        'CIK': '0000320193', 
        'Business' : Business,
        'Risk Factors': Risk_Factors,
        'MDA': MDA,
        'Market Risk' : Market_Risk,
        'Financial Statements': Fin_Statements,
        'DEOC': DEOC
    }, index=[0])

    return df_10K.to_csv('text_content_10k.csv')

get_content = content_sections(raw_10k)
