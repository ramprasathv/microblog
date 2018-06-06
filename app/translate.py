from boto3.session import Session

def translate(text='', source='en', target='es'):

    try:
        session = Session(profile_name='translate')
        client = session.client('translate')
        response = client.translate_text(Text=text,
                                         SourceLanguageCode=source,
                                         TargetLanguageCode=target)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return('Error: the translation service failed')
        else:
            return response['TranslatedText']

    except Exception as e:
        return('Error: the translation service failed')
