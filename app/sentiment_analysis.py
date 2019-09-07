from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def analyze(text):
    client = language.LanguageServiceClient.from_service_account_json(
        "account.json")

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(
        document=document).document_sentiment.score

    return sentiment


if __name__ == '__main__':
    print('"{}" has a sentiment score of {}'.format("Four score and seven years ago our fathers broughtforth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.",
                                                    analyze("Four score and seven years ago our fathers broughtforth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.")))
