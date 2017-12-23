import csv
import os
import urllib.request


# load messages from the historic_message csv file
def load_messages():
    messages = []
    with open('historic_messages.csv', 'r', newline='', encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        for line in reader:
            messages.append(line)

    return messages


# given messages return all urls
def urls(messages):
    url_list = []
    for message in messages:
        if not message[3] == '':
            url_list.append((message[3], message[4]))
    return url_list

def download_images(group_name):
    messages = load_messages()
    url_list = urls(messages)

    directory = os.getcwd() + '\\Images\\' + group_name
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)

    url_count = 1
    for url in url_list:
        print('File Number: ' + str(url_count))
        filename = 'Frands ' + url[1].replace(':','-').replace(' ','@') + '.gif'
        urllib.request.urlretrieve(url[0], filename=filename)
        url_count+=1
