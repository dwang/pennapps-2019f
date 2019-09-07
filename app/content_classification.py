from google.cloud import language


def classify(text):
    client = language.LanguageServiceClient.from_service_account_json(
        "account.json")

    while len(text.split(" ")) <= 20:
        text += " " + text

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)

    response = client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        result[category.name] = category.confidence

    return result


if __name__ == '__main__':
    result = classify("Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all menare created equal.")
    if result:
        print(result)
