import csv
import tweet_scraping
import web_scraping
import time

with open("marquee.csv") as csvfile:
  with open("marquee_output.csv", "w") as csvresult:
    reader = csv.reader(csvfile, delimiter=",")
    writer = csv.writer(csvresult, lineterminator='\n')

    i = 0

    for row in reader:
      if not row[0][0].isdigit():
        continue

      if (i % 60 == 0):
        date = row[0].split("/")
        fixed_date = date[2] + "-" + date[0] + "-" + date[1]
        new_date = date[2] + "-" + date[0] + "-" + str((int(date[1]) + 1))
        twitter_sentiment = tweet_scraping.get_tweets(row[len(row) - 1], fixed_date, new_date)
        row.append(twitter_sentiment)
        writer.writerow(row)
        print(row)
        time.sleep(1)

      i += 1


