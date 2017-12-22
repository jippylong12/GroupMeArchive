from groupy.client import Client
import datetime
from collections import defaultdict
import csv


# given a group return when it is created at
def created_at(groupme_group):
    time_created = groupme_group.data['created_at']
    return datetime.datetime.fromtimestamp(int(time_created)).strftime('%m-%d-%Y %H:%M:%S')


# get a list of all the groups and print out the time created at
def group_created(token):
    client = Client.from_token(token)
    groups = client.groups.list_all()

    group_created_times = {}
    for group in groups:
        group_created_times[group.name] = created_at(group)

    with open('Groups Created At.txt', 'w', encoding='utf8') as output:
        for name, timestamp in group_created_times.items():
            output.write(name + ': ' + timestamp + '\n')


# only return image attachments
def list_attachments(attachments):
    return_string = ''
    for each in attachments:
        if each['type'] == 'image':
            if return_string == '':
                return_string += each['url']
            else:
                return_string += ',' + each['url']

    return return_string


# given the message we need to get the information we want to print it out and use later
# attachments
# created_at
# name
# text
# user_id
def historic_message(message):
    return [message.data['user_id'],
            message.data['name'],
            message.data['text'],
            list_attachments(message.data['attachments']),
            datetime.datetime.fromtimestamp(int(message.data['created_at'])).strftime('%m-%d-%Y %H:%M:%S')]


# count of messages for each person
def message_count(message, dict):
    user_id = message.data['user_id']

    # if the user exists we just increment by one
    if user_id in dict:
        dict[user_id] += 1
    # otherwise we will set it as one
    else:
        dict[user_id] = 1
    # always increase the total count
    dict['Total'] += 1


# people change their names and this will keep track because the user_id stays the same
def unique_names(message, dict):
    user_id = message.data['user_id']
    name = message.data['name']
    # if we haven't added the name yet add the name
    if name not in dict[user_id]:
        dict[user_id].append(name)


# given a group id, create files for all messages, message count, unique names
def group_archive(group_id, client):
    group = client.groups.get(group_id)

    # all messages with formatted information
    messages_list = []

    # number of messages for each user
    message_count_dict = {
        'Total': 0
    }

    # names we've had
    unique_names_dict = defaultdict(list)

    for message in group.messages.list_all():
        # add to historic information
        messages_list.append(historic_message(message))
        # add message count
        message_count(message, message_count_dict)
        unique_names(message, unique_names_dict)
        if message_count_dict['Total'] % 1000 == 0:
            print('Total: ' + str(message_count_dict['Total']))

    # output historic messages
    with open('historic_messages.csv', 'w', newline='', encoding="utf-8") as historic_file:
        writer = csv.writer(historic_file)
        for message in messages_list:
            writer.writerow(message)

    # output message count
    with open('message_count.csv', 'w', newline='', encoding="utf-8") as message_count_file:
        writer = csv.writer(message_count_file)
        for id, count in message_count_dict.items():
            writer.writerow([id, count])

    # output unique names
    with open('unique_names.csv', 'w', newline='', encoding="utf-8") as unique_names_file:
        writer = csv.writer(unique_names_file)
        for id, list_of_names in unique_names_dict.items():
            writer.writerow([id] + list_of_names)


token = ''
with open('token.txt', 'r') as token_file:
    token = token_file.readline()

client = Client.from_token(token)
groups = client.groups.list()
group_id = groups[0].data['group_id'] # loop to find your id
group_archive(group_id, client)

print('here')
