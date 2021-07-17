To run this project, run: <br>
    <b>python TCPserver.py</b>
    
Of course, you need python installed

The server is ran by default on port 6789, so to get to the homepage of the app, on your browser, go to: <br>
    <b>localhost:6789</b>


Suggestion for testing the project:

1. Go to the Sign Up tab from the homepage and sign up for 2 different accounts.
    (If you don't want to sign up, go to the "database" folder inside the project folder,
    open the file "users.yaml", and pick 2 accounts that were pre-created)

2. Once you have your 2 accounts, go to the <b>Send Message</b> page and try to send a message
    from one account to the other. You will need to specify the username and password
    of the account sending the message as well as the username of the receiving account.

3. If the message is sent successfully, you will see one of the following messages (depends on whether
    it's the first time the 2 accounts send messages to each other:
    - "Message Sent Successfully! Check out your conversations!"
    - "Message Sent Successfully! New conversation created!"

4. At this point, to confirm that the message is received, go to the <b>Conversation</b> page,
    type in the credential of the receiving account. After you click <b>"Get Correspondents"</b>,
    the dropdown button will be filled with accounts that the current account corresponds with.
    Changing this dropdown will switch the current conversation to the conversation with the selected account.

5. Confirm that the message sent by the first account shows up in the conversations of the second account.
    As a side note, in a conversation, the message sent by your account shows up in BLUE.
    The message sent by the other account to you shows up in GREY.


Thank you! Good luck!<br>
Jeremy Duong.
