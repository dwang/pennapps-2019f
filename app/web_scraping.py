from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime

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

            # get headline text
            headline = headline_container.find("h3", class_ = "headline").find("a").text
            summary = headline_container.find("div", class_ = "summary-container")

            # only add headline summary if it exists
            if summary:
                headline += ". " + summary.find("p").text

            info.append(headline);


            # get and add formatted publish date of headline
            publish_date = headline_container.find("time", class_ = "date-stamp-container").text
            publish_date_info = publish_date.split()
            formatted_publish_date = datetime.strptime(publish_date_info[0][:3] + " " + publish_date_info[1].rjust(2) + " " + publish_date_info[2], "%b %d, %Y").strftime("%Y-%m-%d")
            print(formatted_publish_date)

            info.append(formatted_publish_date)


            headline_texts.append(info)

        page_number += 1

    return(headline_texts)

def 