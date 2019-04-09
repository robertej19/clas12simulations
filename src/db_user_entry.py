from __future__ import print_function
from utils import utils, file_struct, scard_helper
import sqlite3, time, os, argparse

argparser = argparse.ArgumentParser()
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
args = argparser.parse_args()
file_struct.DEBUG = getattr(args,file_struct.debug_long)

#This function prompts the user to enter in information. In the future this will not run out of the command line, so this will change
def manual_data():
  username = raw_input("Enter JLab username: ")
  email = raw_input("Enter email address: ")
  return username, email

#This function is not really necessary, I just didn't want to have this long string repeated in the code
def command_writer(user,email):
  strn = """INSERT INTO Users(User, Email, JoinDateStamp, Total_Batches,
          Total_Jobs, Total_Events, Most_Recent_Active_Date)
          VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");""".format(
          user,email,int(time.time()),0,0,0,"Null")
  return strn

#The code will try to submit a defualt user to the DB. If the default user already exists,
#then the prompt will come up at the command line asking for a new user
# IF the username that is returned already exists in the command line, another error will be returned and program will quit.
try:
  conn = sqlite3.connect(file_struct.DB_path + file_struct.DBname)
  c = conn.cursor()
  c.execute('PRAGMA foreign_keys = ON;')
  strn = command_writer(file_struct.default_user,file_struct.default_email)
  c.execute(strn)
  if int(file_struct.DEBUG) == 2:
    utils.printer('Executing SQL Command: {}'.format(strn)) #Turn this on for explict printing of all DB write commands
  conn.commit()
  c.close()
  conn.close()
  utils.printer("Record added to DB for User")
except sqlite3.IntegrityError:
  try:
    c.close()
    conn.close()
    utils.printer("Default user '{0}' is already in Users table. Please enter a new, unique user".format(file_struct.default_user))
    user, email = manual_data()
    strn = command_writer(user,email)
    utils.sql3_exec(strn)
    utils.printer("Record added to DB for User")
  except sqlite3.IntegrityError:
    utils.printer("User {0} also already exists in the Users table. Please run the program again, and enter a UNIQUE user".format(user))
    utils.printer("To see users already in DB, execute 'sqlite3 {}', 'SELECT * FROM Users;'".format(file_struct.DBname))
