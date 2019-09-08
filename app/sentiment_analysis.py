from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def analyze(text):
    client = language.LanguageServiceClient.from_service_account_json(
        "account.json")

    encoding_type = enums.EncodingType.UTF8

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(
        document=document).document_sentiment

    entity_type = enums.Entity.Type(client.analyze_entities(document, encoding_type=encoding_type).entities[0].type).name

    return (sentiment, entity_type)


if __name__ == '__main__':
    print('"{}" has a sentiment score of {}'.format("Four score and seven years ago our fathers broughtforth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.",
                                                    analyze("Four score and seven years ago our fathers broughtforth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.")))
