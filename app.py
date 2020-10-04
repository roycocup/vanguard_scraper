import requests
import os
import pprint as pp 
from basescrapper import BaseScrapper
from bs4 import BeautifulSoup
import time
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


def run_on_link(link):
    slug_name = slugify(link['name'])
    filepath = cached_tables + "/" + slug_name + ".html"
    if os.path.isfile(filepath):
        return False

    selected_link = link['href']
    bs = BaseScrapper()
    bs.goto(selected_link)
    el = bs.driver.find_element_by_css_selector('a.priceAndPerformance')
    el.click()

    time.sleep(3)
    document_sizes = "let bottom=document.body.scrollHeight;" \
        "let one_third=(bottom/3);" \
        "let half=bottom/2;"
    bs.execute_js(document_sizes + "window.scrollTo(0,one_third);")



    table = bs.driver.find_element_by_css_selector('#performanceView')
    tab = table.find_element_by_css_selector('a.quarterly')

    final_table = bs.move(tab).click().perform()

    bs.screenshot()

    table = bs.driver.find_element_by_css_selector('div#summaryTotReturnsPerfTab')
    html_table = table.get_attribute('innerHTML')
    
    with open(filepath, "w") as f:
        f.write(html_table)

    bs.quit()
    



links = get_links()

def run():
    start_at = 0
    num_links = 26
    for i in range(start_at, num_links + start_at):
        try:
            run_on_link(links[i])
        except Exception as e:
            print(e)

run()
# run_on_link(links[0])





