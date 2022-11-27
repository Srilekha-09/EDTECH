from flask import Flask, request
from deep_translator import GoogleTranslator, single_detection
import intentClassifier
import validators
import imghdr
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Welcome to TechFlyers Api"

@app.route('/about')
def index():
    return "This is an api build for AirtelIQ.To have seamless interaction"



@app.route('/query', methods=['POST'])
def response():
    msg = request.form.get('Body')
    lang = single_detection(msg, api_key='bbe1af5f4651c0d5268d420bcfb2b36d')
    translated = GoogleTranslator(source="auto", target="en").translate(msg)
    print(lang, translated)

    resp = intentClassifier.search(translated)

    if type(resp) == list:

        response = MessagingResponse()

        # check for video
        if resp[0] == 'video':
            for _ in resp[1:]:
                message = Message()
                message.body(_)
                response.append(message)
            print(response)
            return str(response)

        # check for document
        if resp[0] == 'pdf':
            index = 0
            for _ in resp[1:]:
                message = Message()
                message.media(_)
                response.append(message)
                index += 1
                if index == 2:
                    break
            print(response)
            return str(response)

        # check for career recommendation
        if resp[0] == 'career':
            for _ in resp[1:]:
                # For image
                try:
                    imghdr.what(_)
                    message = Message()
                    message.media(_)
                    response.append(message)
                except:
                # for list
                    if type(_) == list:
                        concat = ''
                        message = Message()
                        for each in _:
                            concat += '▸ ' + each + '\n'
                        message.body(concat)
                        response.append(message)
                        continue

                    message = Message()
                    message.body(_)
                    response.append(message)

            print(response)
            return str(response)

        # check for job
        if resp[0] == 'job':
            index = 1
            for each in resp[1:]:
                message = Message()
                lst1 = '*Job name* ▸ ' + resp[index]['job_name']
                lst2 = '*Company name* ▸ ' + resp[index]['company_name']
                lst3 = '*Link* ▸ ' + resp[index]['link']
                lst4 = '*Location* ▸ ' + resp[index]['location']

                concat = lst1 + '\n' + lst2 + '\n' + lst3 + '\n' + lst4
                message.body(concat)
                message.media('https://as1.ftcdn.net/v2/jpg/01/87/66/12/1000_F_187661260_WYyJKuZjeN3mL56aZSxqQfbLzpQmLVkh.jpg')
                response.append(message)

                index += 1

                if index == 5:
                    break

            print(response)
            return str(response)


        for _ in resp[:-1]:
            if type(_) == list:

                message = Message()
                concat = ''
                for each in _:
                    if each == _[-1]:
                        concat += '\n'
                    concat += each + '\n'
                message.body(concat)
                response.append(message)

            else:
                # img with info
                # check here if the string is a valid URL
                valid=validators.url(_)
                if valid==True:
                    url = _
                    continue

                if url != None and len(resp) == 3:
                    message = Message()
                    message.body(_)
                    message.media(url)
                    response.append(message)

        related_search = resp[-1]
        try:
            for each in related_search:
                message = Message()
                message.body(each)
                response.append(message)
        except:
            pass

        print(response)
        return str(response)
    # general query
    else:

        response = MessagingResponse()

        result = GoogleTranslator(source="en", target=lang).translate(resp)
        print(result)

        message = Message()
        message.body(result)
        response.append(message)

        print(response)
        return str(response)
    

if __name__=='__main__':
    app.run(debug=True)
