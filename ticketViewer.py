import requests
import json
from tabulate import tabulate
import pandas as pd


#simpe check whether response is valid
def ErrorCheck(response):
    if response.status_code != 200:
        print('status: ', response.status_code, 'Problem with request, exiting')
        exit()

#return data of a single page in dictionary format
def GetPageData(url, user, pwd):
    # HTTP get request
    response = requests.get(url, auth = (user, pwd))
    ErrorCheck(response)

    #decode json response into a dictionary and use the data
    return (response.json())

#print the subset information 
def showInfo(df, start = 0,end = 1):
    df_sub = df[start:end]
    h = ['ticket_id','time_created', 'time_updated', 'subject']
    print(tabulate(df_sub, headers=h, tablefmt='psql', showindex=False))

def convertData(ticketData):
    keys_to_extract = ['id','created_at','updated_at','subject']
    ticket_subset = {key:[] for key in keys_to_extract}

    for ticket in ticketData['tickets']:
        for key in keys_to_extract:
            ticket_subset[key].append(ticket[key])
    
    return(pd.DataFrame(ticket_subset))

def updateData(s, e, user_input):
    status = True
    if user_input == '1': 
        s += 25
        e += 25
    elif user_input == '2': 
        s -= 25
        e -= 25
    elif user_input == 'home' or  user_input == 'quit':
        status = False
    return s, e, status

def main():
    #set request params
    url = 'https://zccnaron.zendesk.com/api/v2/incremental/tickets/cursor.json?&start_time=0'
    user = 'naron.chen@richmond.edu'
    pwd = 'blank'

    #Get the data of all tickets, convert to pandas dataframe
    ticketData = GetPageData(url, user, pwd) #Empty Data Exception
    df = convertData(ticketData)
    quit = False

    while quit == False:
        print("")
        print("----------------HOME PAGE-----------------")
        print("     *Enter 1 to view all tickets")
        print("     *Enter 2 to view one ticket ")
        print("     *Enter quit to quit Program")
        user_input = input()

        if user_input == '1':
            start, end = 0, 25
            status = True

            while status:
                showInfo(df, start, end)
                print("----------------VIEW ALL TICKETS-----------------")
                print("     *Enter 1 to go to the Next Page")
                print("     *Enter 2 to go to the Previous Page")
                print("     *Enter home to Exit to home page")
                print("     *Enter quit to Quit Program")
                user_input = input()
                start, end, status = updateData(start, end, user_input)
        
        if user_input == '2':
            status = True
            while status:
                ticket_num = int(input("Enter Ticket Number: "))
                showInfo(df.loc[df['id'] == ticket_num])
                print("----------------VIEW ONE TICKET-----------------")
                print("     *Enter 1 to search for another ticket")
                print("     *Enter home to go to Home Page")
                print("     *Enter quit to quit Program")
                # if ticket_num > count or ticket_num < count:

                user_input = input()
                if user_input == 'home' or  user_input == 'quit':
                    status = False

        if user_input == 'quit':
            quit = True
        
        # else:
        #     print("Oops, you just entered sth invalid, please try again")


main()