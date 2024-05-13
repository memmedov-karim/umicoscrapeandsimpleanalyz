print("hello fardi.")
import csv
import re
import requests
from bs4 import BeautifulSoup

def get_page_data(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
        # print(page.content)
        return page.content
    except requests.RequestException as e:
        print("error", e)

def get_html_page_from_content(content):
    html_parser = BeautifulSoup(content,"html.parser")
    return html_parser

def get_job_title(one_product_block):
    title = one_product_block.find("h3",class_="results-i-title").getText()
    return title

def get_company_name(one_product_block):
    price_new = one_product_block.find("a",class_="results-i-company")
    if price_new:
        return price_new.getText().strip()
    return None
def get_job_salary(one_product_block):
    price_old = one_product_block.find("div",class_="results-i-salary")
    if price_old:
        return price_old.getText().strip()
    return None
def get_location_category(one_product_block):
    location_category = one_product_block.find("div",class_="results-i-secondary")
    if location_category:
        return location_category.getText().strip()
    return None
def get_products_data(html_page):
    data = []
    jobss_wrapper = html_page.find("div", class_="results")
    if jobss_wrapper:
        jobs = jobss_wrapper.find_all("div", class_="results-i") 
        for job in jobs:
            title = get_job_title(job)
            company = get_company_name(job)
            salary = get_job_salary(job)
            locationctg = get_location_category(job)
            d = {}
            d["title"] = title
            d["company"] = company
            d["salary"] = salary
            s = split_string(locationctg)
            if(len(s)==3):
                [city,category,subcategory] = s
                d["city"] = city
                d["category"] = category
                d["subcategory"] = subcategory
            else:
                d["city"] = None
                d["category"] = None
                d["subcategory"] = None
            f = extract_numbers_from_string(salary)
            if(len(f)==2):
                [minsalary,maxsalary] = f
                d["minimumsalary"] = minsalary
                d["maximumsalary"] = maxsalary
            else:
                d["minimumsalary"] = None
                d["maximumsalary"] = None
            data.append(d)
    return data
def split_string(s):
    parts = s.split('/')
    result = []
    for part in parts:
        words = re.findall('[A-Z][^A-Z]*', part)
        result.extend([word.capitalize() for word in words])
    return result

def extract_numbers_from_string(s):
    if not s.strip(): 
        return [None, None]
    pattern = r'\d+'
    numbers = re.findall(pattern, s)
    numbers = [int(num) for num in numbers]
    if len(numbers) == 1:
        numbers.append(None)
    return numbers


def get_one_data(page):
    base_url = "https://boss.az/vacancies?action=index&controller=vacancies&only_path=true&page="+str(page)+"&search%5Bcategory_id%5D=133&type=vacancies"
    html_page = get_html_page_from_content(get_page_data(base_url))
    return get_products_data(html_page)
def get_all_products_to_last_page(page):
    data = []
    for i in range(1,page+1):
        data.extend(get_one_data(i))
    return data



def write_data_to_file(filename,datas):
    csv_file = filename+'.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas) 
    print(f"Data has been written to {csv_file}")




def main():
    while True:
        page_number = input("Enter page number (q to quit): ")
        if page_number.lower() == "q":
            break
        datas = get_all_products_to_last_page(int(page_number))
        write_data_to_file("scrapeddata",datas)
        # for product in get_all_products_to_last_page(int(page_number)):
        #     print(product)

if __name__ == "__main__":
    main()

