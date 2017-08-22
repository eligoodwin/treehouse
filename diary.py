#this is a simple app that shows how to use a single table database using peewee for database work
#not too bad. 

#native
import datetime
from collections import OrderedDict
import sys

#imported
from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
  #content 
  content = TextField();
  timestamp = DateTimeField(default=datetime.datetime.now)
  #timestamp
  class Meta:
    database = db

def initialize():
  """Creat the database"""
  #connect to the database
  db.connect()
  #create the entries 
  db.create_tables([Entry], safe = True)
  
  
#make a menue
def menu_loop():
  """Show the menu"""
  choice = None
  
  #if the user has not choosen q whihc is equal for quit
  while choice != 'q':
    #prompt the user about quiting 
    print("Enter 'q' to quit.")
    #print out the user choices
    for key, value in menu.items():
      #what is dunder doc? this goes to the function and grabs the 
      #document string abou the function! That's cool
      print('{}) {}'.format(key, value.__doc__))
    
    #get user input and then make a selection on course of action
    choice = input('Action: ').lower().strip() #strip out to lower case
    #possible menu choices
    if choice in menu:
      menu[choice]()
      
  
def add_entry():
  """Add an Entry."""
  print("Enter your entry, Press control+d when finished.")
  #this is about handling system stuff and dealing with stdin we want to get the signal for ctrl+d
  #and process it
  data = sys.stdin.read().strip()

  if data:
    if input("Save entry? [y/n] ").lower() != 'n':
      Entry.create(content=data)
      print("Saved successfully!")



#what we are going to do here is that we are passing the an argumetn for view entries
#that is if the value exists in the db or not. If it does we will display it? How will 
#select it?
def view_entries(search_query=None):
  """view entries"""
  entries = Entry.select().order_by(Entry.timestamp.desc())
  #only return the result that we are looking for
  if search_query:
    entries = entries.where(Entry.content.contains(search_query))

  #print out the entries in the database
  for entry in entries:
    #weekday month day of month year hour on 12 clock minute  amp/pm
    timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M %p')
    print('=' * len(timestamp))
    print(entry.content)
    print('n) next entry')
    print('d) delete entry')
    print('q) retunt to manin menu')

    next_action = input('Action: [n/q/d] ').lower().strip()
    
    if next_action == 'q':
      break

    elif next_action == 'd':
      delete_entry(entry)


def search_entries():
  """Search entries for a string"""
  view_entries(input('Search query: '))



def delete_entry(entry):
  """Delete Entry"""
  if input("Are you sure y/n? ") == 'y':
    entry.delete_instance()
    print('Entry was deleted.')



menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])

if __name__ == '__main__':
  #init the db
  initialize()
  #loop the menu
  menu_loop()
