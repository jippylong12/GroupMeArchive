# README #

Generates files for a given GroupMe user. 

### What is this repository for? ###
Create a file with a list of all your GroupMe's and the datetime they were created. 

Given a group, 
* Create a file with all messages. 
* Create a file with a count of each user's messages
* Create a file with every user's names they have used. 

For the historic messages we are given:
* User ID
* Name at the time of message creation
* Actual Message
* Attachments if any
* Created At TimeStamp

For the message count file:
* User ID
* Number of Messages

For unique names file:
* User ID
* List of names they have used. 

### How do I get set up? ###

There are only two function to worry about. 
1) group_created - lists all groups and timestamps
2) group_archive - the other three files

The current repo is set up for group archive.

Before all that make sure to go to the groupme developer website and log in and get an access token. Then you must create a file called 'token.txt' in the same directory.
Then paste that token into the first line. That is where the program will read the token.

To use group_created just create a script that imports group_created and feed it the token. You can also just copy the token directly into the function. 

For group archive it is the same thing but you need the group id and the client. 

You can obtain the group id by client.groups.list() and then looking for the group you want and getting their id. 

Feed those into the function and it will do the rest. 

### Contribution guidelines ###

Do whatever you want with it just credit me. 

### Who do I talk to? ###

Marcus Salinas
markysalinas12@gmail.com