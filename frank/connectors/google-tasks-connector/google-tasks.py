from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ### TASKSLISTS
# # Overview Structure
# {
#   "kind": "tasks#taskList",
#   "id": string,
#   "etag": string,
#   "title": string,
#   "updated": datetime,
#   "selfLink": string
# }

# # List
# tasklists = service.tasklists().list().execute()

# for tasklist in tasklists['items']:
#     print tasklist['title']

# # Get
# tasklist = service.tasklists().get(tasklist='tasklistID').execute()

# print tasklist['title']

# # Insert
# tasklist = {
#   'title': 'New Task List'
#   }

# result = service.tasklists().insert(body=tasklist).execute()
# print result['id']

# # Update
# # First retrieve the tasklist to update.
# tasklist = service.tasklists().get(tasklist='taskListID').execute()
# tasklist['title'] = 'New Task List Name'

# result = service.tasklists().update(tasklist=tasklist['id'], body=tasklist).execute()
# print result['title']

# # Delete
# service.tasklists().delete(tasklist='taskListID').execute()

# ### TASKS
# # Overview Structure
# {
#   "kind": "tasks#task",
#   "id": string,
#   "etag": etag,
#   "title": string,
#   "updated": datetime,
#   "selfLink": string,
#   "parent": string,
#   "position": string,
#   "notes": string,
#   "status": string,
#   "due": datetime,
#   "completed": datetime,
#   "deleted": boolean,
#   "hidden": boolean,
#   "links": [
#     {
#       "type": string,
#       "description": string,
#       "link": string
#     }
#   ]
# }

# # List 
# tasks = service.tasks().list(tasklist='@default').execute()

# for task in tasks['items']:
#   print task['title']

# # List Response
# {
#   "kind": "tasks#tasks",
#   "etag": string,
#   "nextPageToken": string,
#   "items": [
#     tasks Resource
#   ]
# }

# # Get
# task = service.tasks().get(tasklist='@default', task='taskID').execute()

# print task['title']

# # Insert
# task = {
#   'title': 'New Task',
#   'notes': 'Please complete me',
#   'due': '2010-10-15T12:00:00.000Z'
#   }

# result = service.tasks().insert(tasklist='@default', body=task).execute()
# print result['id']

# # Update
# # First retrieve the task to update.
# task = service.tasks().get(tasklist='@default', task='taskID').execute()
# task['status'] = 'completed'

# result = service.tasks().update(tasklist='@default', task=task['id'], body=task).execute()
# # Print the completed date.
# print result['completed']

# # Delete
# service.tasks().delete(tasklist='@default', task='taskID').execute()

# # Clear
# service.tasks().clear(tasklist='taskListID').execute()

# # Move
# service.tasks().clear(tasklist='taskListID').execute()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])
    


    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))

if __name__ == '__main__':
    main()