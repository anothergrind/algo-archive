# Task: Build a tool to parse dates into counts within dictionaries

# Example 
# Input: dates = [05/03/2021, 05/04/2021, 05/03/2021]
# Output

## Key Takeaways
# Clarify before you build
# Define "correct" up front
# Hunt for edge cases
# Test, don't trust
# Own the solution
#   if you can't explain how it works, you don't understand it, and you cant verify its correctness

def parse_dates(dates):
    """
    Parses a list of date strings and returns a dictionary with counts of each unique date.

    Args:
        dates (list): A list of date strings in the format 'MM/DD/YYYY'.

    Returns:
        dict: A dictionary where keys are unique date strings and values are their counts.
    """
    date_counts = {}
    
    for date in dates:
        if date in date_counts:
            date_counts[date] += 1
        else:
            date_counts[date] = 1
            
    return date_counts