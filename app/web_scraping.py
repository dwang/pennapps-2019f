from bs4 import BeautifulSoup as bs
import requests
import datetime
from datetime import timedelta

def get_headlines(ticker, date=None, range=10):
    """
    date should be passed in as a string in following format 'yyyy/mm/dd'
    range will cause search to be the given number of days up 
    and down from given date
    """
    page_number = 1

    headline_texts = []

    page_link = ""

    # find number of pages, give option of searching within a range
    if date == None:
        page_link = f"https://www.wsj.com/search/term.html?KEYWORDS={ticker}&min-date=2012/07/01&max-date=2017/07/01&isAdvanced=true&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,press,newswire,wsjpro&page=1"
    else:
        date = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
        max_date = date + timedelta(days=range)
        min_date = date - timedelta(days=range)

        max_date = max_date.strftime("%m/%d/%Y")
        min_date = min_date.strftime("%m/%d/%Y")

        page_link = f"https://www.wsj.com/search/term.html?KEYWORDS={ticker}&min-date={min_date}&max-date={max_date}&isAdvanced=true&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,press,newswire,wsjpro&page=1"

    
    page_response = requests.get(page_link, timeout=5)
    page_content = bs(page_response.content, "lxml")
    
    page_count = 0
    try:
        page_count = int(page_content.find_all("li", class_ = "results-count")[1].text[3:])
    except:
        pass

    # iterate through each page to get their headers
    while (page_number <= page_count):
        page_link = page_link[:-1] + str(page_number)

        page_response = requests.get(page_link, timeout=5)

        page_content = bs(page_response.content, "lxml")

        headline_containers = page_content.find_all("div", class_ = "headline-container")

        for headline_container in headline_containers:
            info = []

            # get headline informationn
            headline = headline_container.find("h3", class_ = "headline").find("a").text
            publish_date = headline_container.find("time", class_ = "date-stamp-container").text
            summary = headline_container.find("div", class_ = "summary-container")

            info.append(headline)
            info.append(publish_date)

            # only add headline summary if it exists
            if summary:
                info.append(summary.find("p").text)

            headline_texts.append(info)

        page_number += 1

    return headline_texts
