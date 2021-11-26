import requests
import json
from tabulate import tabulate
import pandas as pd
# import getpass
import stdiomask

#simpe check whether response is valid
def ResponseCheck(response):
    if response.status_code != 200:
        print('*********** Status:', response.status_code, ', Problem with request, Exiting ***********')
        if response.status_code == 401:
            print("*********** Error Detail: It seemed like you entered an invalid email or password ***********")
        exit()

#return data of a single page in dictionary format
def GetPageData(url, user, pwd):
    # HTTP get request
    response = requests.get(url, auth = (user, pwd))
    ResponseCheck(response)

    #decode json response into a dictionary and use the data
    return (response.json())

#print the subset information 
def showInfo(df, start = 0,end = 1):
    df_sub = df[start:end]
    h = ['ticket_id','time_created', 'time_updated', 'subject']
    print(tabulate(df_sub, headers=h, tablefmt='psql', showindex=False))



def convertData(ticketData):
    keys_to_extract = ['id','created_at','updated_at','subject'] #information to abstract
    ticket_subset = {key:[] for key in keys_to_extract}

    for ticket in ticketData['tickets']:
        for key in keys_to_extract:
            ticket_subset[key].append(ticket[key])
    
    return(pd.DataFrame(ticket_subset))

def updateData(s, e, user_input, df):
    status = True

    if user_input == '1': 
        if checkPageLimit(df,s-1):
            s -= 25
            e -= 25
        else: print('\n****************************** You have reached the Start of the All Tickets ******************************\n')
    elif user_input == '2': 
        if checkPageLimit(df,e):
            s += 25
            e += 25
        else: print('\n****************************** You have reached the End of the All Tickets ******************************\n')
    else:
        invalid()
    return s, e

def invalid():
    print('*********** Oops, you just entered sth invalid, please try again ***********\n')

def checkPageLimit(df, i):
    return True if i >= 0 and i <= len(df.index) else False 



def main():

    #set request params
    url = 'https://zccnaron.zendesk.com/api/v2/incremental/tickets/cursor.json?&start_time=0'
    user = 'naron.chen@richmond.edu'
    pwd = 'blank'
    
    # user = input("--Please Enter Your Email: ")
    # pwd = stdiomask.getpass("--Please Enter Your Password: ") # It will ask to enter password and display * on the screen
    
    #Get the data of all tickets, convert to pandas dataframe

    ticketData = GetPageData(url, user, pwd) #Empty Data Exception
    df = convertData(ticketData)
    print("--Connected!")



    while True:
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
                print("--You are at Page:", end//25 )
                print("")
                print("----------------VIEW ALL TICKETS-----------------")
                print("     *Enter 1 to go to the Previous Page")
                print("     *Enter 2 to go to the Next Page")
                print("     *Enter home to exit to home page")
                print("     *Enter quit to quit Program")
                user_input = input()

                if user_input == 'home': status = False
                if user_input == 'quit': exit()

                print("="*100, "\n"*2) #format
                start, end = updateData(start, end, user_input, df) 

                
        
        elif user_input == '2':
            status, invalidInput = True, False
            while status:
                if invalidInput == False: 
                    try:
                        ticket_num = int(input("--Enter Ticket Number: "))
                        if ticket_num == 0 or checkPageLimit(df, ticket_num) == False:
                            print("** ID Entered Out of Range, Please Enter a Valid ID **")
                            continue
                    except ValueError:
                        print("** Please Enter a valid Integer **")
                        continue

                showInfo(df.loc[df['id'] == ticket_num])
                print("----------------VIEW ONE TICKET-----------------")
                print("     *Enter 1 to search for another ticket")
                print("     *Enter home to go to Home Page")
                print("     *Enter quit to quit Program")
                # if ticket_num > count or ticket_num < count:

                user_input = input()
                if user_input == '1': invalidInput = False
                elif user_input == 'home': status = False
                elif user_input == 'quit': exit()
                else:
                    invalid()
                    invalidInput = True
    
        elif user_input == 'quit': exit()
        
        else:
            print("="*100, "\n"*2) #format
            invalid()


main()