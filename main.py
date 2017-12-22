from groupy.client import Client
import datetime


# given a group return when it is created at
def created_at(groupme_group):
    time_created = groupme_group.data['created_at']
    return datetime.datetime.fromtimestamp(int(time_created)).strftime('%m-%d-%Y %H:%M:%S')

# get a list of all the groups and print out the time created at
def group_created():
    client = Client.from_token(token)
    groups = client.groups.list_all()

    group_created_times = {}
    for group in groups:
        group_created_times[group.name] = created_at(group)

    with open('Groups Created At.txt', 'w', encoding='utf8') as output:
        for name, timestamp in group_created_times.items():
            output.write(name + ': ' + timestamp + '\n')


token = ''
with open('token.txt', 'r') as token_file:
    token = token_file.readline()


print('here')
