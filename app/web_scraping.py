from bs4 import BeautifulSoup as bs
import requests
import datetime

def get_headlines(ticker):
    page_number = 1

    headline_texts = []

    # find number of pages
    page_link = f"https://www.wsj.com/search/term.html?KEYWORDS={ticker}&min-date=2012/07/01&max-date=2017/07/01&isAdvanced=true&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,press,newswire,wsjpro&page=1"
    page_response = requests.get(page_link, timeout=5)
    page_content = bs(page_response.content, "lxml")
    page_count = int(page_content.find_all("li", class_ = "results-count")[1].text[3:])

    # iterate through each page to get their headers
    while (page_number <= page_count):
        page_link = f"https://www.wsj.com/search/term.html?KEYWORDS={ticker}&min-date=2012/07/01&max-date=2017/07/01&isAdvanced=true&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,press,newswire,wsjpro&page={page_number}"

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

    return(headline_texts)
