"""
Christian Stoldal
Assignment 01
Discription:
Implmenting the basic functionallity of SQL
"""
import os.path
import sys


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

#For debuging
printCommands = False



#This function sets the working scope
def useDB(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("USE ")

    DBName = cmdSplit[1]

    #Adding the extenstion to the DB name
    DBName += ".txt"

    #Check if database exist
    if os.path.isfile(DBName):
        #If the database exist we then change the global scope to be in that directory
        currentDB = DBName
        print("-- Using database " + DBName.split('.')[0] + ".")

    else:
        #IF the database does not exist we prompt the user
        print("-- !Failed to use " +  DBName + " because it does not exist.")

    #print("useDB" + cmd)




#This function will create the database
def createDatabase(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("CREATE DATABASE ")

    DBName = cmdSplit[1]
    DBName = DBName.strip()

    #If the DB already exist tell the user 
    if os.path.isfile(DBName+".txt"):
        print("-- !Failed to create database " + DBName + " because it already exists.")
    #Else if the database does not exist create the datbase(file)
    else:
        open(DBName + ".txt", "x")
        print("-- Database " + DBName + " created.")


    #print("createDatabase" + cmd)



#This function will create a table within the current DB scope
def createTable(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)


    """
    Idea - sepreate each table into a text file
         - Each var is appended to the end of the text file
    """

    """
    Idea 2 - more complicated
           - each database is a textfile
           - each table is listed in the same way as before
           - Special charachters or char set to denote the begining and end of a table
    """

    """
    Database structure

    Database.txt
    ________________________________________________________

    >>Table Name
    *varType name
    col val
    col val
    col val

    *varType name
    col val
    col val
    col val

    <<(EOT)
    ________________________________________________________

    """
    #Check if we are in a database
        #If we are parse the database and see if this table exist
            #If it does exist
                #Prompt user
            #If it does not add it to the database


    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("CREATE TABLE ")

    tableName = cmdSplit[1].split('(')[0]
    tableName = tableName.strip()

    #spliting out the vars
    variableAssignments = cmdSplit[1].split(tableName)[1]

    #removing the '(' and ')'
    variableAssignments = variableAssignments.strip()
    variableAssignments = variableAssignments[1:-1]


    #Checking if we are in a currentDB - this also confirms that the current database exist
    if currentDB != "":

        #Opening a read file pointer so the database can be parsed and checked to see if the specfic table already exist
        fp = open(currentDB,'r')

        #Using a flag to record if the table exist while parsing through the file
        doesTableExist = False

        for row in fp:

            #If the table exist set the flag and break out of the loop
            if (">>" + tableName) in row:
                doesTableExist = True
                break
        #Close the file pointer
        fp.close

        #Now we check the status of the flag to see if the table already exist
        #If the table exist we prompot the user 
        if doesTableExist:
            print("-- !Failed to create table " + tableName + " because it already exists.")
        #If the table does not exist we now start creating the table
        else:

            #We first open a append pointer
            fp = open(currentDB,'a')

            #Defining the start and end of the table for easy writing
            tableStart = ">>" + tableName + "\n"
            tableEnd = "<<\n"

            #The table start is added to the file
            fp.write(tableStart)


            #The vars are added
            #Removing the ')' from the end of the list of vars
            #variableAssignments.replace(')','')
            #variableAssignments.replace('(','')
            

            #Spliting the string of vars into a list
            vars = variableAssignments.split(',')
            #Next we iterate through the list of vars adding them to the list
            for var in vars:
                fp.write('*' + var.strip() + '\n')
            

            #The end of the table is added to the file
            fp.write(tableEnd)
            fp.close()
            print("-- Table " + tableName + " created.")




    #The user is not in a database so the user is prompted
    else:
        print("-- !Failed to create table " + tableName + " not currently in a database.")



    #print("create table" + cmd)

#This function delets a database and all tables within
def dropDatabase(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("DROP DATABASE ")

    DBName = cmdSplit[1]

    DBName += ".txt"

    #If the DB exist the database will be deleted
    #print("DATABASE name is: -" + DBName + "-")
    if os.path.isfile(DBName):

        #Shutil.rmtree is used so that no error is prompted if the database contains tables(files)
        try:
            os.remove(DBName)
        except:
            print("***Failed to remove database***")
        print("-- Database " + DBName.split('.')[0] + " deleted.")
        #Check if the current database is the deleted one
        if DBName == currentDB:
            currentDB = ""
    else:
        print("-- !Failed to delete " + DBName.split('.')[0] + " because it does not exist.")

    #print("dropDatabase")


#This function delets a specfic table within a database
def dropTable(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("DROP TABLE ")

    tableName = cmdSplit[1]

    #Check to see if the user is in a database
    if currentDB != "":
        #Using a flag to record if the table exist while parsing through the file
        doesTableExist = False

        #Open the database file for reading
        fp = open(currentDB,'r+')

        #Read in a copy of the database
        databaseCopy = fp.readlines()

        #Parse through each line of the database looking for the inteded table
        for i in range(len(databaseCopy)):

            #Check if the current line is equal to the start of the specfied table
            if databaseCopy[i] == (">>" + tableName + '\n'):

                #set the flag that the table does exist
                doesTableExist = True

                #Iterate through the databaseCopy deleting lines until we reach the end of the file
                while databaseCopy[i] != "<<\n":
                    databaseCopy.pop(i)

                #Deleting the end of the table
                databaseCopy.pop(i)
            #Break out of the loop if we have confirmed the table exist  
            break
        fp.close()


        #Check the flag to see if the table was succesfully found
        if doesTableExist:
            #Open the file again in write mode
            fp = open(currentDB,"w")

            #Iterate through databaseCopy writing it to the database
            for line in databaseCopy:
                fp.write(line)

            fp.close()
            print("-- Table " + tableName + " deleted.")
        else:
            #Alert the user that the database they wanted to delete does not exist
            print("-- !Failed to delete " + tableName + " because it does not exist.")
    #If not in a database alert user
    else:
        print("-- !Failed to delete " + tableName + " not currently in a database.")
    

    #print("drop table" + cmd)

#This function gives the ability to add a variable to a specfic table
def alterTable(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("ALTER TABLE ")[1]


    tableName = cmdSplit.split(" ADD ")[0]
    var = cmdSplit.split(" ADD ")[1]
    
    if currentDB != "":
        #Using a flag to record if the table exist while parsing through the file
        doesTableExist = False
        
        #Open the database file for reading
        fp = open(currentDB,'r+')

        #Read in a copy of the database
        databaseCopy = fp.readlines()

        #Parse through each line of the database looking for the inteded table
        for i in range(len(databaseCopy)):

            #Check if the current line is equal to the start of the specfied table
            if databaseCopy[i] == (">>" + tableName + '\n'):

                #set the flag that the table does exist
                doesTableExist = True

                #Iterate through the databaseCopy deleting lines until we reach the end of the file
                while databaseCopy[i] != "<<\n":
                    #Moving the iterator to the last line of the table
                    i += 1
                
                #Insert the new variable
                databaseCopy.insert(i, ("*" + var + '\n'))

                #Break out of the loop if we have confirmed the table exist  
                break
        fp.close()

        #Check the flag to see if the table was succesfully found
        if doesTableExist:
            #Open the file again in write mode
            fp = open(currentDB,"w")

            #Iterate through databaseCopy writing it to the database
            for line in databaseCopy:
                fp.write(line)

            fp.close()

            print("-- Table " + tableName + " modified.")

        else:
            #Alert the user that the database they wanted to delete does not exist
            print("-- !Failed to delete " + tableName + " because it does not exist.")

    else:
        print("-- !Failed to alter " + tableName + " not currently in a database.")


#This function allows for the viewing of all of the information within a specfic table
def selectStar(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Seperating the command from the intended database    
    cmdSplit = cmd.split("SELECT * FROM ")

    tableName = cmdSplit[1]

    #List of variables
    vars = []

    #Check to see if the user is inside a database
    if currentDB != "":

        #Open the database file for reading
        fp = open(currentDB,'r')

        #Read in a copy of the database
        databaseCopy = fp.readlines()

        #Using a flag to record if the table exist while parsing through the file
        doesTableExist = False

        #iterating through the databaseCopy looking for the start of the table
        for i in range(len(databaseCopy)):

            #Checking if the current line is the start of table
            #print("Comparing: " + databaseCopy[i] + " to " + (">>" + tableName + "\n"))
            if databaseCopy[i] == (">>" + tableName + "\n"):
            
                doesTableExist = True
                i += 1

                #Looping through the databaseCopy and copying the variable into a seprate list
                while databaseCopy[i] != "<<\n":
                    vars.append(databaseCopy[i][1:])
                    i += 1
                break
        
        #If the doesTableExist flag is set print out the vars list
        if doesTableExist:
            print("-- ", end="")

            #Count for formating the output of variables
            count = 0
            numVars = len(vars)            

            for var in vars:
                count += 1
                #Formating and printing the list of variables the table has
                print((var[:-1]), end ="")
                if(count != numVars):
                     print(" |",end=" ")
            
            print()

        #If the doesTableExist flag is not set alert the user that the table does not exist
        else:
            print("-- !Failed to query table " + tableName + " because it does not exist.")

        

    else:
        print("-- !Failed to query table " + tableName + " not currently in a database.")

    #print("select star" + cmd)




#opLoop() - Operational Loop that makes up the user interface allowing users to input commands until .exit is called
def opLoop():

    userCommand = ""

    #This defines the current scope of the database
    #It is global because the current dierectory needs to be avaliable to all functions 
    global currentDB

    #Checks to see if more then one argurment is passed in at run time
    #If the number of arguments is greater then one it is assumed that the file is the test file
    if len(sys.argv) > 1:
        sys.stdin = open(sys.argv[1],'r')

    


    #print("Number of command line arguments: " + str(len(sys.argv)))

    while True:

        
        #Retreaving user input
        #userCommand = input("stoldalDBM-" + currentDB.split('.')[0] +":")
        userCommand = input()

        #Strips semicolons from command
        userCommand = userCommand.replace(';','')

        #userCommand = userCommand.upper()

        if "--" in userCommand:
            #print("Pass")
            pass
        elif "USE" in userCommand: #Done
            useDB(userCommand)
        elif 'CREATE DATABASE' in userCommand: #Done
            createDatabase(userCommand)
        elif "CREATE TABLE"  in userCommand: #Done
            createTable(userCommand)
        elif "DROP DATABASE" in userCommand: #Done
            dropDatabase(userCommand)
        elif "DROP TABLE"in userCommand: #Done
            dropTable(userCommand)
        elif "ALTER TABLE"in userCommand:
            alterTable(userCommand)
        elif "SELECT *" in userCommand: #Done
            selectStar(userCommand)
        elif ".EXIT" in userCommand:
            break
    print("-- All done.")









opLoop()
