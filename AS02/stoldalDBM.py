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
Insert Function
-"insert into Product valyes(1, 'Gizmo', 19.99);
    -Check if in a database
        -Check if "Product" table exist



Alter select * functionality to show variables instead of schema

Where 

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
        print("-- Using Database " + DBName.split('.')[0] + ".")

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
    if inDataBase():

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
            
                while databaseCopy[i] != "<<\n" :
                    
                    #The buffer will hold the var name and the list of instances it has
                    # The first value in the buffer will be the name of the variable
                    buffer = []

                    #if the current line is a decleration of a variable
                    if databaseCopy[i][0] == '*':
                        #Append the first var decleration to the first postion of the buffer
                        bufferValue = databaseCopy[i].replace('\n','')
                        buffer.append(bufferValue)
                        #Increase the iterator to the next line
                        i += 1

                        #If the current lines first postion is equal to '*' we are on a new variable
                        while databaseCopy[i][0] != '*':
                            #Appened the variable instance to the buffer
                            bufferValue = databaseCopy[i].replace('\n','')
                            buffer.append(bufferValue)
                            i += 1
                            if databaseCopy[i] == "<<\n":
                                break
                        #appened the set of variables to the vars list
                        vars.append(buffer)
                break

        #If the doesTableExist flag is set print out the vars list
        if doesTableExist:
            for i in range(len(vars[0])):
                print("-- ", end = '')
                for j in range(len(vars)):
                    if j != len(vars)-1:
                        print(cleanString(vars[j][i]) + '|',end='')
                    else:
                        print(cleanString(vars[j][i]),end='')
                print()



        #If the doesTableExist flag is not set alert the user that the table does not exist
        else:
            print("-- !Failed to query table " + tableName + " because it does not exist.")

        

    else:
        print("-- !Failed to query table " + tableName + " not currently in a database.")

    #print("select star" + cmd)

def insertInto(cmd):


    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Removing the insert into from the user CMD
    userCommand = cmd.split('insert into')[1]

    #Getting the table that user wants to use
    insertTable = userCommand.split('values')[0]
    insertTable = insertTable.strip()

    #Getting the instances of the diffrent variables to be inserted
    newVars = userCommand.split('values')[1]

    newVars = newVars[1:-1]
    newVars = newVars.replace(' ','')
    newVars = newVars.replace('\t','')
    newVars = newVars.replace('\'','')
    newVars = newVars.replace('\n','')
    newVars = newVars.split(',')

    
    #print("The variables: " + str(newVars) + " is being added to table: " + str(insertTable))

    #The case that the user is not within a database 
    if not inDataBase():
        print("-- !Failed to insert into table " + insertTable + " not currently in a database.")
        return

    #The vase that the user wants to insert into a table that does not exist
    if not doesTableExist(insertTable):
        print("-- !Failed to insert into table " + insertTable + " because it does not exist.")
        return


    #Opening the database 
    fp = open(currentDB,'r')

    #and copying the database to a string arr
    databaseCopy = fp.readlines()

    #close fp 
    fp.close

    #DEBUGGING
    #print("DataBaseCopy: " + str(databaseCopy))


    for i in range(len(databaseCopy)):
        #Checking to see if the current line is the start of the correct database
        if databaseCopy[i] == (">>" + insertTable + '\n'):
            #If it is start a loop to continue through the database copy
            for j in range(i,len(databaseCopy)+len(newVars)):
                #If the current lines first char is a '*' it is the decleration of a variable
                if (databaseCopy[j][0] == '*') and (len(newVars) != 0):
                    j += 1
                    varString = str("$" + newVars.pop(0) + '\n')
                    databaseCopy.insert(j,varString)
                elif databaseCopy[j] == "<<":

                    break

                

            break


    fp = open(currentDB,'w')
    #print("DataBaseCopy: " + str(databaseCopy))

    for line in databaseCopy:
        fp.write(line)

    fp.close()

    print("-- 1 new record inserted.")


def updateWhere(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    cmdList = cmd.split()

    tableName = cmdList[1].strip()

    newValueVar = cmdList[3].strip()
    newValueVar = newValueVar.replace('\'','')

    newValue = cmdList[5].strip()
    newValue = newValue.replace('\'','')
    
    whereVar = cmdList[7].strip()

    whereVarValue = cmdList[9].strip()
    whereVarValue = whereVarValue.replace('\'','')

    """
    update TABLE
    set VAR with VALUE
    where VAR = VALUE

    """



    """
    Find postion of where value
        for find the variable:
            for find the postion n of the specfic variable:
                get n
        for find the variable
            for got to postion n in var list
        

    """

    #The case that the user is not within a database 
    if not inDataBase():
        print("-- !Failed to update table " + tableName + " not currently in a database.")
        return

    #The vase that the user wants to insert into a table that does not exist
    if not doesTableExist(tableName):
        print("-- !Failed to update table " + tableName + " because it does not exist.")
        return


    #Opening the database 
    fp = open(currentDB,'r')

    #and copying the database to a string arr
    databaseCopy = fp.readlines()

    #close fp 
    fp.close

    whereValuePositions = []
    currentCount = 0

    for i in range(len(databaseCopy)):
        #print("Parsing line: " + databaseCopy[i])
        if whereVar in databaseCopy[i]:
            i += 1
            while databaseCopy[i][0] != "*":
                #print("In while")
                #print("Parsing line: " + databaseCopy[i])
                #print("Comparing to: " + ("$" + whereVarValue + '\n'))
                if databaseCopy[i] == ("$" + whereVarValue + '\n'):
                    #print('Breaking on line: ' + databaseCopy[i])
                    whereValuePositions.append(currentCount)
                currentCount += 1
                i += 1
        
    #print("Value postion in " + whereVar + " is " + str(list(whereValuePositions)))

    for i in range(len(whereValuePositions)):
        for j in range(len(databaseCopy)):
        #print("Parsing line: " + databaseCopy[i])
            
            #print("j is: " + str(j))
            if newValueVar in databaseCopy[j]:
                j += 1
                #print("Current Line is: " + databaseCopy[j])
                #print("Var position: " + str(j+whereValuePositions[i]))
                databaseCopy[j+whereValuePositions[i]] = ("$" + newValue + '\n')
                #if databaseCopy[j] 





    fp = open(currentDB,'w')
    #print("DataBaseCopy: " + str(databaseCopy))

    for line in databaseCopy:
        fp.write(line)

    fp.close()

    if len(whereValuePositions) <= 1:
        print("-- " + str(len(whereValuePositions)) + " record modified.")
    else:
        print("-- " + str(len(whereValuePositions)) + " records modified.")


def deleteWhere(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    cmdList = cmd.split('delete from')[1]
    cmdList = cmdList.split(' ')

    tableName = cmdList[1]

    deleteVar = cmdList[3]

    deleteOperator = cmdList[4]


    deleteDomain = cmdList[5]
    deleteDomain = deleteDomain.replace('\'','')
 #print("Table name: " + tableName)

    #print("cmdList size: " + str(cmdList))


    #Opening the database 
    fp = open(currentDB,'r')

    #and copying the database to a string arr
    databaseCopy = fp.readlines()

    #close fp 
    fp.close

    #The case that the user is not within a database 
    if not inDataBase():
        print("-- !Failed to update table " + tableName + " not currently in a database.")
        return

    #The vase that the user wants to insert into a table that does not exist
    if not doesTableExist(tableName):
        print("-- !Failed to update table " + tableName + " because it does not exist.")
        return

    itemsDeletedCount = 0
    deletePosition = []

    if deleteOperator == '=':
        #Loop through database looking first for the correct table
        for i in range(len(databaseCopy)):
            #If the current line is the start of the correct table
                if databaseCopy[i] == (">>" + tableName + "\n"):
                    #counter for variable position
                    variablePositionCount = 0

                    #Move forward one postion into the variable defenetions
                    i += 1
                    #While not a the end of the database
                    while databaseCopy[i] != "<<\n":
                        #Check if the current line is the variable decleration
                        if deleteVar in databaseCopy[i]:
                            #Move forward one postion into the variable instances
                            i += 1
                            while databaseCopy[i] != "<<\n":
                                
                                buffer = cleanString(databaseCopy[i])
                                #print("parsing buffer: " + str(buffer))
                                
                                """
                                The if statment below is what needs to be changed to adjust the operator
                                """

                                #in this case we are checking to see if our domain value 
                                # is equal to the buffer value
                                if buffer == deleteDomain:
                                    #if the delete condition is true at that position to the 
                                    # delete postion array
                                    deletePosition.append(variablePositionCount)
                                    #reset the postion count to 0
                                    variablePositionCount = 0

                                variablePositionCount += 1
                                i += 1
                        i += 1
                        if i > len(databaseCopy)-1:
                            break

        #print("The number of variables found for deletion is: " + str(deletePosition))
        #print("At position(s): ",end="")
        # for val in deletePosition:
        #     print(str(val) + "",end='')
        # print()

        #Deleting the specfied row

        #Repeat below process for each 
        for j in range(len(deletePosition)):
            #Start by looking for the correcttable
            for i in range(len(databaseCopy)):
                #If the current line is the start of the correct table
                    if databaseCopy[i] == (">>" + tableName + "\n"):
                        while databaseCopy[i] != "<<"+"\n":
                            if databaseCopy[i][0] == "*":
                                #print("Deleting line: " + databaseCopy[i+deletePosition[j]+1])
                                #print("position: " + str(i+deletePosition[j]+1))
                                databaseCopy.pop(i+deletePosition[j]+1)
                                #deletePosition = adjustArray(deletePosition)
                            i += 1
                        break
            deletePosition = adjustArray(deletePosition)


    elif deleteOperator == '>':
        #Loop through database looking first for the correct table
        for i in range(len(databaseCopy)):
            #If the current line is the start of the correct table
                if databaseCopy[i] == (">>" + tableName + "\n"):
                    #print("In if")
                    #counter for variable position
                    variablePositionCount = 0

                    #Move forward one postion into the variable defenetions
                    i += 1
                    #While not a the end of the database
                    while databaseCopy[i] != "<<\n":
                        #Check if the current line is the variable decleration
                        if deleteVar in databaseCopy[i]:
                            #Move forward one postion into the variable instances
                            i += 1
                            while databaseCopy[i] != "<<\n":
                                
                                buffer = cleanString(databaseCopy[i])
                                #print("parsing buffer: " + str(buffer))
                                
                                #in this case we are checking to see if our domain value 
                                # is greater then the buffer value
                                if float(buffer) > float(deleteDomain):
                                    deletePosition.append(variablePositionCount)
                                    variablePositionCount = 0

                                variablePositionCount += 1
                                i += 1
                        i += 1
                        if i > len(databaseCopy)-1:
                            break

        # print("The number of variables found for deletion is: " + str(deletePosition))
        # print("At position(s): ",end="")
        # for val in deletePosition:
        #     print(str(val) + "",end='')
        # print()

        #Deleting the specfied row

        #Repeat below process for each 
        for j in range(len(deletePosition)):
            #Start by looking for the correcttable
            for i in range(len(databaseCopy)):
                #If the current line is the start of the correct table
                    if databaseCopy[i] == (">>" + tableName + "\n"):
                        while databaseCopy[i] != "<<"+"\n":
                            if databaseCopy[i][0] == "*":
                                #print("Deleting line: " + databaseCopy[i+deletePosition[j]+1])
                                #print("position: " + str(i+deletePosition[j]+1))
                                databaseCopy.pop(i+deletePosition[j]+1)
                                #deletePosition = adjustArray(deletePosition)
                            i += 1
                        break
            deletePosition = adjustArray(deletePosition)


    elif deleteOperator == '<':
        for i in range(len(databaseCopy)):
            if databaseCopy[i] == ('*' + deleteVar + '\n'):
                while databaseCopy[i] != "<<\n":
                    buffer = databaseCopy.replace('$','')
                    #print("Buffer is: " + str(buffer))
                    #print("Delete domain is: " + str(deleteDomain))
                    if float(buffer) < float(deleteDomain):
                        #print("*****Deleting val: " + databaseCopy[i])
                        databaseCopy.pop(i)
                        itemsDeletedCount += 1
                    i += 1
    elif deleteOperator == '!=':
        pass
    else:
        print("-- Could not delete uknown operator: " + str(deleteOperator))

    fp = open(currentDB,'w')
    #print("DataBaseCopy: " + str(databaseCopy))

    for line in databaseCopy:
        fp.write(line)

    fp.close()

    if itemsDeletedCount <= 1:
        print("-- " + str(len(deletePosition)) + " record deleted.")
    else:
        print("-- " + str(len(deletePosition)) + " records deleted.")


"""
************** Tool Functions **************
"""

def inDataBase():
    global currentDB

    if currentDB == "":
        return False
    else:
        return True

def doesTableExist(tName):
    fp = open(currentDB,'r')

    databaseCopy = fp.readlines()


    for line in databaseCopy:
        #print("CHECKING LINE: " + str(line) + " AGAINST:  >>" + str(tName))
        if line == (">>" + tName +'\n'):
            fp.close()
            return True
    
    fp.close()
    return False

def cleanString(s):
    s = s.strip()
    s = s.replace('\n','')
    s = s.replace('*','')
    s = s.replace('$','')
    
    return s

def adjustArray(ar):
    for i in range(len(ar)):
        ar[i] = ar[i]-1
    return ar











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


        #Retreave users input
        userCommand = input("")

        #userCommand = userCommand.split()


        #In the case on the first enter from the user the command does not end
        # with a ';' keep looping until a command ends in ';'
        if userCommand != '':
            if (userCommand[len(userCommand)-1] != ';') and userCommand != ".EXIT" :
                #print("current line: " + userCommand)
                while True:
                    userCommand += input()
                    if userCommand[len(userCommand)-1] == ';':
                        break
        if userCommand == '':
            #print("NEW LINE")
            pass
        #Strips semicolons from command
        userCommand = userCommand.replace(';','')



        
        # #Retreaving user input
        # #userCommand = input("stoldalDBM-" + currentDB.split('.')[0] +":")
        # userCommand = input()

       
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
        elif "insert into" in userCommand:
            insertInto(userCommand)
        elif "update" in userCommand:
            updateWhere(userCommand)
        elif "delete from" in userCommand:
            deleteWhere(userCommand)
        elif ".EXIT" in userCommand:
            print("-- All done.")
            break

    









opLoop()
