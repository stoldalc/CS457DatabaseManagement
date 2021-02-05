"""
Christian Stoldal
Assignment 01
Discription:
Implmenting the basic functionallity of SQL
"""
import os.path
from os import path
import shutil


"""
Needed functionallity
-Create a database
-Delete a database

-Create a table within a database
-Delete a table from a database

-being within a scope of a database

-altering a table

-getting specfic ifnormation from tables

"""

currentDB = ""

#This function sets the working scope
def useDB(cmd):

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("USE ")

    DBName = cmdSplit[1]

    #Check if database exist
    if os.path.isdir(DBName):
        #If the database exist we then change the global scope to be in that directory
        currentDB = DBName

    else:
        #IF the database does not exist we prompt the user
        print("!Failed to use " + DBName +  " because it does not exist.")




#This function will create the database
def createDatabase(cmd):

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("CREATE DATABASE ")

    DBName = cmdSplit[1]

    #If the DB already exist tell the user 
    if os.path.isdir(DBName):
        print("!Failed to create database " + DBName + " because it already exists.")
    #Else if the database does not exist create the datbase(dir)
    else:
        os.mkdir(DBName)
    


#This function will create a table within the current DB scope
def createTable(cmd):
    print("create table" + cmd)

#This function delets a database and all tables within
def dropDatabase(cmd):

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("DROP DATABASE ")

    DBName = cmdSplit[1]

    #If the DB exist the database will be deleted
    if os.path.isdir(DBName):
        #Shutil.rmtree is used so that no error is prompted if the database contains tables(files)
        shutil.rmtree(DBName)
    else:
        print("!Failed to delete " + DBName + " because it does not exist.")


#This function delets a specfic table within a database
def dropTable(cmd):
    print("drop table" + cmd)

#This function gives the ability to add a variable to a specfic table
def alterTable(cmd):
    print("alter table" + cmd)

#This function allows for the viewing of all of the information within a specfic table
def selectStar(cmd):
    print("select star" + cmd)




#opLoop() - Operational Loop that makes up the user interface allowing users to input commands until .exit is called
def opLoop():

    userCommand = ""

    #This defines the current scope of the database
    #It is global because the current dierectory needs to be avaliable to all functions 
    global currentDB

    while True:

        #Retreaving user input
        userCommand = input("stoldalDBM-" + currentDB +":")

        #Strips semicolons from command
        userCommand = userCommand.replace(';','')

        if "USE" in userCommand:
            useDB(userCommand)
        elif 'CREATE DATABASE' in userCommand:
            createDatabase(userCommand)
        elif "CREATE TABLE"  in userCommand:
            createTable(userCommand)
        elif "DROP DATABASE" in userCommand:
            dropDatabase(userCommand)
        elif "DROP TABLE"in userCommand:
            dropTable(userCommand)
        elif "ALTER TABLE"in userCommand:
            alterTable(userCommand)
        elif "SELECT *" in userCommand:
            selectStar(userCommand)
        elif ".EXIT" in userCommand:
            break
    print("Goodbye")









opLoop()
