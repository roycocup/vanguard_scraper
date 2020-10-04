
import os
import time
import pprint as pp 
import requests
import glob
from basescrapper import BaseScrapper
from bs4 import BeautifulSoup

from slugify import slugify

cached_tables = 'tables'


def p(o):
    pp.pprint(o)


def get_links():
    htmlfilename = 'vanguard_funds.html'

    with open(htmlfilename, "rb") as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")

    raw_links = soup.select("a.linkMargin")

    links = [{'href':ref.get('href'), 'name':ref.text} for ref in raw_links]
    return links

def get_filename(link):
    slug_name = slugify(link['name'])
    filepath = cached_tables + "/" + slug_name + ".html"
    return {"filepath":filepath, "slug_name":slug_name}
    

def run_on_link(link, bs=None):
    filedetails = get_filename(link)
    filepath = filedetails['filepath']
    slug_name = filedetails['slug_name']
    if os.path.isfile(filepath):
        return False
    
    bs.goto(link['href'])
    el = bs.driver.find_element_by_css_selector('a.priceAndPerformance')
    el.click()

    time.sleep(3)
    document_sizes = "let bottom=document.body.scrollHeight;" \
        "let one_third=(bottom/3);" \
        "let half=bottom/2;"
    bs.execute_js(document_sizes + "window.scrollTo(0,one_third);")
    bs.screenshot(cached_tables + "/" + slug_name + ".png")

    table = bs.driver.find_element_by_css_selector('#performanceView')
    tab = table.find_element_by_css_selector('a.quarterly')

    final_table = bs.move(tab).click().perform()

    table = bs.driver.find_element_by_css_selector('div#summaryTotReturnsPerfTab')
    html_table = table.get_attribute('innerHTML')
    
    write_to_cache(html_table, filepath)


def write_to_cache(data, filepath):
    with open(filepath, "w") as f:
        f.write(data)
    
def run(links=None):
    start_at = 0
    num_links = len(links)
    bs = BaseScrapper()
    for i in range(start_at, num_links + start_at):
        try:
            run_on_link(links[i], bs=bs)
        except Exception as e:
            print(e)
    bs.quit()

# run(get_links())


# files = glob.glob(cached_tables + '/*.html')

# for tablefile in files:
#     with open(tablefile, "rb") as f:
#         html = f.read()
#     if len(html) > 7:
#         p(html)
#         quit()
    






