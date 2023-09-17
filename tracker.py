import smtplib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from price_parser import Price

PRODUCT_URL_CSV = "products.csv"
SAVE_TO_CSV = True
PRICES_CSV = "prices.csv"
SEND_MAIL = True

# for cloudflare check to bypass
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def get_urls(csv_file):
    df = pd.read_csv(csv_file)
    return df

def get_response(url):
    response = requests.get(url, headers=HEADERS)
    # print(url)
    # print(response.text)
    return response.text

def get_price(html):
    soup = BeautifulSoup(html, "html.parser")

    # el = soup.select_one(".price_color")
    # price = Price.fromstring(el.text)

    price_object = soup.find('span', {'class': 'product__price'})
    return float(price_object.text.strip("$"))
    # return price.amount_float

def process_products(df):
    updated_products = []
    for product in df.to_dict("records"):
        html = get_response(product["url"])
        product["price"] = get_price(html)
        product["alert"] = product["price"] < product["alert_price"]
        updated_products.append(product)
    return pd.DataFrame(updated_products)

def get_mail(df):
    subject = "Price Drop Alert"
    body = df[df["alert"]].to_string()
    subject_and_message = f"Subject:{subject}\n\n{body}"
    return subject_and_message

def send_mail(df):
    message_text = get_mail(df)
    with smtplib.SMTP("smtp.server.address", 587) as smtp:
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(mail_user, mail_to, message_text)

"""return pandas dataframe"""
def site_get_df():
    df = get_urls(PRODUCT_URL_CSV)
    df_updated = process_products(df)
    return df_updated

def main():
    df = get_urls(PRODUCT_URL_CSV)
    df_updated = process_products(df)
    if SAVE_TO_CSV:
        df_updated.to_csv(PRICES_CSV, index=False, mode="a")
    if SEND_MAIL:
        pass
        # send_mail(df_updated)

if __name__ == "__main__":
    main()