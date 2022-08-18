# how-to-build-a-price-tracker
How to Build a Price Tracker With Python


```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

```bash
$ pip install pandas requests beautifulsoup4 price-parser
```

```python
import smtplib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from price_parser import Price
```

```python
PRODUCT_URL_CSV = "products.csv"
SAVE_TO_CSV = True
PRICES_CSV = “prices.csv"
SEND_MAIL = True
```

```python
def get_urls(csv_file):
    df = pd.read_csv(csv_file)
    return df
```

```python
def process_products(df):
    for product in df.to_dict("records"):
        # product["url"] is the URL
```

```python
def get_response(url):
    response = requests.get(url)
    return response.text
```

```python
def get_price(html):
    soup = BeautifulSoup(html, "lxml")
    el = soup.select_one(".price_color")
    price = Price.fromstring(el.text)
    return price.amount_float
```

```python
def process_products(df):
    updated_products = []
     for product in df.to_dict("records"):
        html = get_response(product["url"])
        product["price"] = get_price(html)
        product["alert"] = product["price"] < product["alert_price"]
        updated_products.append(product)
    return pd.DataFrame(updated_products)
```

```python
if SAVE_TO_CSV:
        df_updated.to_csv(PRICES_CSV, mode="a")
```

```python
def get_mail(df):
    subject = "Price Drop Alert"
    body = df[df["alert"]].to_string()
    subject_and_message = f"Subject:{subject}\n\n{body}"
    return subject_and_message
```

```python
def send_mail(df):
    message_text = get_mail(df)
    with smtplib.SMTP("smtp.server.address", 587) as smtp:
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(mail_user, mail_to, message_text)
```

```python
def main():
    df = get_urls(PRODUCT_URL_CSV)
    df_updated = process_products(df)
    if SAVE_TO_CSV:
        df_updated.to_csv(PRICES_CSV, index=False, mode="a")
    if SEND_MAIL:
        send_mail(df_updated)
```
