"""
Script for utility functions
"""

def longest_negative_streak(hourly_data):
    """
    hourly_data: query as a list
    return result: dictionary of all dates with the 
    got help from here https://www.geeksforgeeks.org/python-program-to-count-positive-and-negative-numbers-in-a-list/
    and from chatgpt
    """
    grouped_data = {}
    result = {}

    for row in hourly_data:
        date = row.date
        if date not in grouped_data:
            grouped_data[date] = []
        grouped_data[date].append((row.startTime, row.hourlyPrice))

    for date, records in grouped_data.items():
        longest_streak = 0
        current_streak = 0

        for _, price in records:
            if price != None:
                if price < 0:
                    current_streak += 1
                else:
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 0
        
        longest_streak = max(longest_streak, current_streak)
        result[date] = longest_streak

    return result
