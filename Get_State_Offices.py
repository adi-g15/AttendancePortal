"""FUTURE - 1. Find out some way of finding names of district offices (maybe not possible without automating the browser) - https://nyks.nic.in/compile/namken.aspx
				Possibilities - There is a javascript command(1 liner) that executes whenever an option is clicked, Find some way to know what all commands does a browser execute after we click... search for it
"""

from html_table_parser import parser_functions as parse
import urllib.request
from bs4 import BeautifulSoup

target = 'https://nyks.nic.in/compile/zdaddress.aspx'

req = urllib.request.Request( url = target)
f = urllib.request.urlopen(req)	#The actual HTTP Response
xhtml = f.read()
soup = BeautifulSoup( xhtml, 'html.parser' )
state_offices = soup.find( 'table', { 'datakeysname' : 'nykcode', 'id' : 'gridview1' } )
#soup = BeautifulSoup(html_table, 'html.parser')	#FAILED, since html_table is NoneType
twoD_table = parse.make2d(state_offices)