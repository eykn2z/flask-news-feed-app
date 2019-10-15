from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options

from flask_blog import feedMaxCount

options = Options()
options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=options)
    # webdriver.Chrome(executable_path=chromedriver_binary,chrome_options=options)

# TODO:以下追加
# https://natalie.mu/music/news/list/artist_id/93039

def keyaki_official():

    kayaki_official_link='http://www.keyakizaka46.com/s/k46o/news/list'
    browser.get(kayaki_official_link)

    elems=browser.find_element_by_class_name('box-news').find_elements_by_tag_name('li')

    keyaki=[]
    try:
        for n,elem in enumerate(elems):
            if n>feedMaxCount:
                break
            title=elem.find_element_by_class_name('text').text
            link=elem.find_element_by_tag_name("a").get_attribute("href")
            published=elem.find_element_by_class_name('date').text #2019.10.10
            #TODO:処理
            print(title)
            print(link)
    except:
        import traceback
        traceback.print_exc()
    finally:
        browser.quit()
