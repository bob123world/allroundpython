from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
import base64
from bs4 import BeautifulSoup

class GMail():
    def __init__(self, scopes, credentials, token):
        """Create an instance for a GMail account"""
        if type(scopes) is not list:
            print("Type of scopes should be list containing the GMAIL scopes")
        self.scopes = scopes
        if os.path.exists(token):
            with open(token, 'rb') as token_pickle:
                creds = pickle.load(token_pickle)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing token!")
                creds.refresh(Request())
            else:
                if os.path.exists(credentials):
                    flow = InstalledAppFlow.from_client_secrets_file(credentials, SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print("Credentials file doesn't exist!")
            # Save the token for upcoming runs
            with open(token, 'wb') as token_pickle:
                pickle.dump(creds, token_pickle)

        self.service = build('gmail', 'v1', credentials=creds)
        self.user_id = "me"

    def get_labels(self):
        """Get the available labels in you GMail account"""
        results = service.users().labels().list(userId=self.user_id).execute()
        labels = results.get('labels', [])
        # Use for loop -> label["name"] to get the label names!
        return labels


    def get_messages(self, labels):
        """Get a list of emails for the corresponding labels where each email is in dict format"""
        messages = self.get_labelled_messages(labels)
        messages_list = []

        for message in messages:
            message_dict = {}
            m_id = message['id'] # get id of individual message
            message = self.service.users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
            payload = message['payload'] # get payload of the message 

            for header in payload['headers']: # getting the Subject
                if header['name'] == 'Subject':
                    msg_subject = header['value']
                    message_dict['Subject'] = msg_subject
                if header['name'] == 'Date':
                    date_parse = (parser.parse(header['value']))
                    message_dict['Date'] = str(date_parse.date())
                if header['name'] == 'From':
                    message_dict['Sender'] = header['value']
            message_dict['Snipet'] = message["snippet"]

            try:
                # Fetching message body
                parts = payload['parts'] # fetching the message parts
                part_one  = parts[0] # fetching first element of the part 
                part_body = part_one['body'] # fetching body of the message
                part_data = part_body['data'] # fetching data from the body
                clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean_two , "lxml" )
                message_dict['Body']  = soup.body()
            except :
                pass

            print (message_dict)
            messages_list.append(message_dict)
        
            # This will mark the message as read
            self.service.users().messages().modify(userId=self.user_id, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute()
        
        return messages_list


    def get_labelled_messages(self, labels):
        """Get the emails list containing the labels given to it"""
        messages_list = []
        try:
            messages_dict = service.users().messages().list(userId=self.user_id,labelIds=labels).execute()
            messages_list = messages_dict["messages"]
        except Exception as e:
            print(e)
        return messages_list


# # If modifying these scopes, delete the file token.pickle.
# SCOPES = 'https://www.googleapis.com/auth/gmail.modify' # we are using modify and not readonly, as we will be marking the messages Read

# def main():
#     """Shows basic usage of the Gmail API.
#     Lists the user's Gmail labels.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     service = build('gmail', 'v1', credentials=creds)

#     # Call the Gmail API
#     results = service.users().labels().list(userId='me').execute()
#     labels = results.get('labels', [])

#     if not labels:
#         print('No labels found.')
#     else:
#         print('Labels:')
#         for label in labels:
#             print(label['name'])

#     user_id =  'me'
#     label_id_one = 'INBOX'
#     label_id_two = 'UNREAD'

#     # Getting all the unread messages from Inbox
#     # labelIds can be changed accordingly
#     unread_msgs = service.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two]).execute()

#     # We get a dictonary. Now reading values for the key 'messages'
#     mssg_list = unread_msgs['messages']

#     print ("Total unread messages in inbox: ", str(len(mssg_list)))

#     final_list = [ ]


#     for mssg in mssg_list:
#         temp_dict = { }
#         m_id = mssg['id'] # get id of individual message
#         message = service.users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
#         payld = message['payload'] # get payload of the message 
#         headr = payld['headers'] # get header of the payload


#         for one in headr: # getting the Subject
#             if one['name'] == 'Subject':
#                 msg_subject = one['value']
#                 temp_dict['Subject'] = msg_subject
#             else:
#                 pass


#         for two in headr: # getting the date
#             if two['name'] == 'Date':
#                 msg_date = two['value']
#                 date_parse = (parser.parse(msg_date))
#                 m_date = (date_parse.date())
#                 temp_dict['Date'] = str(m_date)
#             else:
#                 pass

#         for three in headr: # getting the Sender
#             if three['name'] == 'From':
#                 msg_from = three['value']
#                 temp_dict['Sender'] = msg_from
#             else:
#                 pass

#         temp_dict['Snippet'] = message['snippet'] # fetching message snippet


#         try:
            
#             # Fetching message body
#             mssg_parts = payld['parts'] # fetching the message parts
#             part_one  = mssg_parts[0] # fetching first element of the part 
#             part_body = part_one['body'] # fetching body of the message
#             part_data = part_body['data'] # fetching data from the body
#             clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
#             clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
#             clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
#             soup = BeautifulSoup(clean_two , "lxml" )
#             mssg_body = soup.body()
#             # mssg_body is a readible form of message body
#             # depending on the end user's requirements, it can be further cleaned 
#             # using regex, beautiful soup, or any other method
#             temp_dict['Message_body'] = mssg_body

#         except :
#             pass

#         print (temp_dict)
#         final_list.append(temp_dict) # This will create a dictonary item in the final list
        
#         # This will mark the messagea as read
#         service.users().messages().modify(userId=user_id, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute() 
        



#     print ("Total messaged retrived: ", str(len(final_list)))

#     '''

#     The final_list will have dictionary in the following format:

#     {	'Sender': '"email.com" <name@email.com>', 
#         'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
#         'Date': 'yyyy-mm-dd', 
#         'Snippet': 'Lorem ipsum dolor sit amet'
#         'Message_body': 'Lorem ipsum dolor sit amet'}


#     The dictionary can be exported as a .csv or into a databse
#     '''

#     #exporting the values as .csv
#     with open('CSV_NAME.csv', 'w', encoding='utf-8', newline = '') as csvfile: 
#         fieldnames = ['Sender','Subject','Date','Snippet','Message_body']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ',')
#         writer.writeheader()
#         for val in final_list:
#             writer.writerow(val)

# if __name__ == '__main__':
#     main()