from newspaper import Article
import sentiment_analysis
def analyze_url(url):
    article = Article(url)
    article.download()
    article.parse()

    result = sentiment_analysis.analyze(article.text)

    return result[0]
