import requests
from bs4 import BeautifulSoup

def get_page_data(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
        # print(page.content)
        return page.content
    except requests.RequestException as e:
        print("Error fetching page:", e)

def get_html_page_from_content(content):
    html_parser = BeautifulSoup(content,"html.parser")
    return html_parser

def get_product_title(one_product_block):
    title = one_product_block.find("span",class_="MPTitle").getText()
    return title

def get_product_price_new(one_product_block):
    price_new = one_product_block.find("span",class_="text-[#ff4b81]")
    if price_new:
        return price_new.getText().strip()
    return None
def get_product_price_old(one_product_block):
    price_old = one_product_block.find("span",class_="text-[13px]")
    if price_old:
        return price_old.getText().strip()
    return None
def get_price_difference(one_product_block):
    new_price_value = get_product_price_new(one_product_block)
    old_price_value = get_product_price_old(one_product_block)
    if new_price_value and old_price_value:
        new_price = float(new_price_value.replace('₼', '').replace(" ","").strip())
        old_price = float(old_price_value.replace('₼', '').replace(" ","").strip())
        price_difference = old_price - new_price
        return price_difference
    else:
        return None
def get_products_data(html_page):
    data = []
    products_wrapper = html_page.find("div", class_="MPProductsListBannersWrapper")
    if products_wrapper:
        products = products_wrapper.find_all("div", class_="MPProductItem") 
        for product in products:
            title = get_product_title(product)
            pricenew = get_product_price_new(product)
            priceold = get_product_price_old(product)
            d = {}
            d["title"] = title
            d["pricenew"] = pricenew
            d["priceold"] = priceold
            d["endirim"] = get_price_difference(product)
            data.append(d)
    return data



def main():
    base_url = "https://umico.az/categories/3-mobil-telefonlar-ve-smartfonlar?page={}"
    while True:
        page_number = input("Enter page number (q to quit): ")
        if page_number.lower() == "q":
            break
        url = base_url.format(page_number)
        print("Requesting URL:", url)
        html_page = get_html_page_from_content(get_page_data(url))
        for product in get_products_data(html_page):
            print(product)

if __name__ == "__main__":
    main()

