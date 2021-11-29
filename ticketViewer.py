import requests
import json
from tabulate import tabulate
import pandas as pd
# import getpass
import stdiomask




class ticketViewer:

    #for the convinience of testing differet components, allowed construction of class to have parameters
    #In a regular running of the program, no params needed
    def __init__(self, sin_1 = None, subDomain = None, user = None, pwd = None):
        self.sin_1 = sin_1 #sore first user input, convinient for testing log in page
        self.url = f"https://{subDomain}.zendesk.com/api/v2/incremental/tickets/cursor.json?&start_time=0"
        self.user = user
        self.pwd = pwd
        self.df = None

    #check whether response is valid
    def ResponseCheck(self, response):
        if response.status_code != 200:
            print(f"** Status: {response.status_code}, Problem with request, Please try again **")
            if response.status_code == 401:
                return("** Error Detail: It seemed like you entered an invalid email/password/api token **")
            if response.status_code == 404:
                return("** Error Detail: It seemed like server can't find the requested resource, check your subdomain name **")
        else:
            return "No Error" #None would mean none error 

    def convertData(self, ticketData):
        keys_to_extract = ['id','created_at','updated_at','subject'] #information to abstract
        ticket_subset = {key:[] for key in keys_to_extract}

        for ticket in ticketData['tickets']:
            for key in keys_to_extract:
                ticket_subset[key].append(ticket[key])
        
        return(pd.DataFrame(ticket_subset))

    
    def GetPageData(self):
        # HTTP get request
        try:
            response = requests.get(self.url, auth = (self.user, self.pwd))
        except requests.exceptions.ConnectionError:
            print("** API unavailable, please check your internet connection **")

        ErrorMessage = self.ResponseCheck(response)
        if  ErrorMessage != "No Error": 
            print(ErrorMessage)
            return False

        #decode json response into a dictionary and use the data
        ticketData = response.json()
        self.df = self.convertData(ticketData) #Get the data of all tickets, convert to pandas dataframe
        print("--Connected!")
        return True



    #print the subset information 
    def showInfo(self, thisdf, start = 0,end = 1):
        df_sub = thisdf[start:end]
        h = ['ticket_id','time_created', 'time_updated', 'subject']
        print(tabulate(df_sub, headers=h, tablefmt='psql', showindex=False))



    def updatePage(self, s, e, user_input):
        status = True

        if user_input == '1': 
            if self.checkPageLimit(s-1):
                s -= 25
                e -= 25
            else: print('\n****************************** You have reached the Start of the All Tickets ******************************\n')
        elif user_input == '2': 
            if self.checkPageLimit(e):
                s += 25
                e += 25
            else: print('\n****************************** You have reached the End of the All Tickets ******************************\n')
        else:
            self.invalid()
        return s, e



    def checkPageLimit(self, i):
        return True if i >= 0 and i <= len(self.df.index) else False 

    def invalid(self): 
        print('\n*********** Oops, you just entered sth invalid, please try again ***********\n')

    def checkTicketNum(self,num):
        try:
            num = int(num)
            if num == 0 or self.checkPageLimit(num) is False:
                print("** ID Entered Out of Range, Please Enter a Valid ID **")
                return False
        except ValueError:
            print("** Please Enter a valid Integer **")
            return False
        return True




    def logIn(self):
        while True:
            print("\n----------------Log In-----------------")
            print("Enter 1 to use password to log in")
            print("Enter 2 to use API token to log in")
            print("Enter quit to quit program")       

            self.sin_1 = input()
            if self.sin_1 == 'quit': exit()

            print("\nNote: sub domain name would be whatever is in the blank of ''https://_______.zendesk.com'' ")
            subDomain = input("--Please Enter Your sub domain Name: ")
            self.url = f"https://{subDomain}.zendesk.com/api/v2/incremental/tickets/cursor.json?&start_time=0"
            self.user = input("--Please Enter Your Email: ")

            if self.sin_1 == '1':
                self.pwd = stdiomask.getpass("--Please Enter Your Password: ") 
                if self.GetPageData() : break #if the subdomain, url and user is valid, continue
                else: continue #else try again
            elif self.sin_1 == '2':
                self.user += '/token'
                self.pwd = stdiomask.getpass("--Please Enter Your API Token: ")
                if self.GetPageData() : break
                else: continue
            else:
                self.invalid()


    def viewAll(self):
        start, end = 0, 25
        status = True

        while status:
            self.showInfo(self.df, start, end) 
            print(f"--You are at Page: {end//25}" )
            print("")
            print("----------------VIEW ALL TICKETS-----------------")
            print("     *Enter 1 to go to the Previous Page")
            print("     *Enter 2 to go to the Next Page")
            print("     *Enter home to exit to home page")
            print("     *Enter quit to quit Program")
            user_input = input().lower()

            if user_input == 'home': status = False
            elif user_input == 'quit': exit()
            else:
                print("="*100, "\n"*2) #format
                start, end = self.updatePage(start, end, user_input) 


    def viewOne(self):
        status, invalidInput = True, False
        while status:
            if invalidInput is False: 
                ticket_num = input("--Enter Ticket Number: ")
                if self.checkTicketNum(ticket_num) is False: continue #if user input for ticketnum is invalid, then let user try input again
            
            thisData = self.df.loc[self.df['id'] == int(ticket_num)]
            self.showInfo(thisData)
            print("----------------VIEW ONE TICKET-----------------")
            print("     *Enter 1 to search for another ticket")
            print("     *Enter home to go to Home Page")
            print("     *Enter quit to quit Program")

            user_input = input().lower()
            if user_input == '1': invalidInput = False
            elif user_input == 'home': status = False
            elif user_input == 'quit': exit()
            else:
                self.invalid()
                invalidInput = True


    def home(self):
        while True:
            print("\n----------------HOME PAGE-----------------")
            print("     *Enter 1 to view all tickets")
            print("     *Enter 2 to view one ticket ")
            print("     *Enter quit to quit Program")
            user_input = input().lower()

            #View All Tickets
            if user_input == '1': self.viewAll()
 
            #View One Ticket
            elif user_input == '2': self.viewOne()
        
            elif user_input == 'quit': exit()
            
            else:
                print("="*100, "\n"*2) #format
                self.invalid()

    def run(self):
        self.logIn()
        self.home()




def main():
    p1 = ticketViewer()
    p1.run()

    




if __name__ == "__main__":
    main()