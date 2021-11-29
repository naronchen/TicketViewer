#In this unit test I tested three most important components for exception handling
#one testing for log_in's exception handling which is mainly the function Response Check
#one testing for view all function's exception handling which is mainly the function updatePage
#last one testing for view one ticket function's exception handling which is mainly the function checkTicketNum

#I will be changing my admin password used here for testing

import unittest
from unittest.mock import patch
from ticketViewer import ticketViewer


import requests
import json
from tabulate import tabulate
import pandas as pd
# import getpass
import stdiomask


# fake_input = iter(['1', 'zmm', 'naron.chen@richmond.edu', '12345', 'quit']).__next__
class TestTicketViewer(unittest.TestCase):
    # @patch('ticketViewer.input', fake_input)
    def test_ResponseCheck(self):

        p1 = ticketViewer('1', 'google', 'naron.chen@richmond.edu', '12345') #invalid subdomain example 
        response = requests.get(p1.url, auth = (p1.user, p1.pwd))
        self.assertEqual(p1.ResponseCheck(response), "** Error Detail: It seemed like server can't find the requested resource, check your subdomain name **")

        p2 = ticketViewer('1', 'zccnaron', 'naron.chen@.edu', '12345') #invalid username example
        response = requests.get(p2.url, auth = (p2.user, p2.pwd))
        self.assertEqual(p2.ResponseCheck(response), "** Error Detail: It seemed like you entered an invalid email or password/api token **")

        p3 = ticketViewer('1', 'zccnaron', 'naron.chen@richmond.edu', '12345') #correct information example
        response = requests.get(p3.url, auth = (p3.user, p3.pwd))
        self.assertEqual(p3.ResponseCheck(response), "No Error")


    @patch('builtins.print')
    def test_updatePage(self, mock_print):
        p1 = ticketViewer('1', 'zccnaron', 'naron.chen@richmond.edu', '12345')
        p1.GetPageData() #update self.df which is used in updatePage -> checkPageLimit

        r = p1.updatePage(50, 75, '1') # test for going to previous page
        self.assertEqual(r,(25,50))

        r = p1.updatePage(0, 25, '2') # test for going to next page
        self.assertEqual(r, (25,50))


        r = p1.updatePage(0,25, '1') # test for hitting the boundaries of the start of the dataset
        mock_print.assert_called_with('\n****************************** You have reached the Start of the All Tickets ******************************\n')
        self.assertEqual(r, (0,25)) #page number should not be updated in this case

        r = p1.updatePage(100,125, '2') # test for hitting the boundaries of the end of the dataset
        mock_print.assert_called_with('\n****************************** You have reached the End of the All Tickets ******************************\n')
        self.assertEqual(r, (100,125)) #page number should not be updated in this case

    
    @patch('builtins.print')
    def test_checkTicketNum(self, mock_print):
        p1 = ticketViewer('1', 'zccnaron', 'naron.chen@richmond.edu', '12345')
        p1.GetPageData() #update self.df which is used in updatePage -> checkPageLimit
        self.assertTrue(p1.checkTicketNum('1')) #test for a working ticket_num

        self.assertFalse(p1.checkTicketNum('0')) #test for a ticket_num out of range
        self.assertFalse(p1.checkTicketNum('9999')) #test for a ticket_num out of range
        self.assertFalse(p1.checkTicketNum('-1')) #test for a ticket_num out of range

        mock_print.assert_called_with("** ID Entered Out of Range, Please Enter a Valid ID **") # check if the error message is printed correctly

        self.assertFalse(p1.checkTicketNum('1.00')) #test for a ticket_num out of range
        self.assertFalse(p1.checkTicketNum('asdb')) #test for a ticket_num out of range
        self.assertFalse(p1.checkTicketNum('quit')) #test for a ticket_num out of range

        mock_print.assert_called_with("** Please Enter a valid Integer **") # check if the error message is printed correctly







if __name__ == '__main__':
    unittest.main()