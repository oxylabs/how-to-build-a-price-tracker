# script.py
import pandas as pd
import tracker

def generate_table():
    df = tracker.site_get_df()
    
    return df.to_html()

if __name__ == "__main__":
    html_table = generate_table()
    print(html_table)
