import re

def check_for_http(text):
    urls=re.findall('http[s]?://*', text) 
    if not urls:
        return "I couldn't find a link to the article in the analysis. Double check that you have one."
    else:
        return "check"

def responses():
    import random
    r_list=["You've got some interesting information here","Lots of good stuff here",
    "I wish I could read more","This is a very interesting topic"]
    k=random.randint(0,3)
    return r_list[k]

# def gettext(driveid):
#     #convert this to a downloadable text
#     import requests
#     import gdown
#     dparts=driveid.split('/')
#     #ddown=dparts[0]+"//drive.google.com/uc?id="+dparts[5]
#     print(dparts[5])
#     gdown.download(driveid,dparts[5]+".txt")
#     with open(dparts[5]+".txt",'r') as fname:
#         file_data=fname.readlines()
#     print(file_data)
#     return file_data

import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)
    with open(destination,'r') as fname:
        file_data=fname.readlines()
    print(file_data)
    return file_data    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def handler(event, context):
    #this will review submitted articles for link, grammar, and keywords.
    #look for url in the analysis
    driveurl=event['currentIntent']['slots']['slotOne']
    driveparts=driveurl.split('/')
    driveid=driveparts[5]
    text=download_file_from_google_drive(driveid,"test.txt")

    msg="Ok, I've read your article analysis. "+responses()+" Here's what I found:/n"

    return msg
    

