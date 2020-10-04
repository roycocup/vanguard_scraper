import requests
import os
import pprint as pp 
from basescrapper import BaseScrapper
from bs4 import BeautifulSoup
import time

def p(o):
    pp.pprint(o)


htmlfilename = 'vanguard_funds.html'

with open(htmlfilename, "rb") as f:
    data = f.read()


soup = BeautifulSoup(data, "html.parser")

raw_links = soup.select("a.linkMargin")

links = [ref.get('href') for ref in raw_links]
num_links = len(links)


bs = BaseScrapper()

selected_link = links[0]

p(selected_link)

bs.goto(selected_link)
el = bs.driver.find_element_by_css_selector('a.priceAndPerformance')
el.click()

time.sleep(5)
document_sizes = "let bottom=document.body.scrollHeight;" \
    "let one_third=(bottom/3);" \
    "let half=bottom/2;"
bs.execute_js(document_sizes + "window.scrollTo(0,one_third);")



table = bs.driver.find_element_by_css_selector('#performanceView')
tab = table.find_element_by_css_selector('a.quarterly')

final_table = bs.move(tab).click().perform()


# scrollElementIntoMiddle = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0); var elementTop = arguments[0].getBoundingClientRect().top; window.scrollBy(0, elementTop-(viewPortHeight/2));"
# bs.driver.execute_script(scrollElementIntoMiddle, e)

bs.screenshot()


final_table.
bs.quit()

# html = bs.driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# pp.pprint(soup.prettify)





