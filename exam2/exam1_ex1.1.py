import re
import pandas as pd


def find_email_in_text(text):
    all_emails = re.findall(r'\b[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}\b', text)
    valid_emails = []
    for email in all_emails:
        if not re.search(r'\.{2,}|_{2,}|-{2,}|\._|_\.|\.-|-\.|-_|_-', email):
            valid_emails.append(email)
    return valid_emails


def read_csv_to_df(file_path):
    df = pd.read_csv(file_path)
    return df.dropna()


if __name__ == '__main__':
    content = None
    with open('text.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    emails = find_email_in_text(content)
    print(emails)

    print()

    df_without_gaps = read_csv_to_df('train.csv')
    print(df_without_gaps.head())
