from exchangelib import Credentials, Account, Configuration, DELEGATE

# credentials = Credentials('deboeure.s@hotmail.com', 'xh-2-FD~5dKL8rZ-x3g6-WtL2BzuCx~Oc5')
# account = Account('deboeure.s@hotmail.com', credentials=credentials, autodiscover=True)

# for item in account.inbox.all().order_by('-datetime_received')[:100]:
#     print(item.subject, item.sender, item.datetime_received)

def main():
    # Connection details
    server = 'outlook.office365.com'
    email = 'deboeure.s@hotmail.com'
    username = 'deboeure.s@hotmail.com'
    password = ''
    account = connect(server, email, username, password)

    for item in account.inbox.all().order_by('-datetime_received')[:100]:
        print(item.subject, item.sender, item.datetime_received)

def connect(server, email, username, password):
    """
    Get Exchange account connection with server
    """
    creds = Credentials(username=username, password=password)
    config = Configuration(server=server, credentials=creds)
    return Account(primary_smtp_address=email, autodiscover=False, config = config, access_type=DELEGATE)

if __name__ == "__main__":
    main()