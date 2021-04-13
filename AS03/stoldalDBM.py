"""
Christian Stoldal
Assignment 02
Discription:
Implmenting the functions insert delete modift and query on the basic table
"""
import os.path
import sys


"""
Encoding Table

Symbol  |    Meaning
----------------------
  >>    | Start of a table
----------------------
   *    | Variable definition
----------------------
   $    | Variable instance
----------------------
  <<    | End of a table
"""

"""
Possible solutions for select * from table(s) condition conditionExpression

Command breakdown 

| select  * from| 
 
| "Table name" "Table Var" |

| join type |

| "Table name" "Table Var" |

| on |

| "Table Var.Table Var Def" = "Table Var.Table Var Def" |


- Get nesecary tables 
    -Load into a arr such as [[table0],[table1]]

- get the condtion



I need to find the format of the statments 

"""


currentDB = ""

#For debuging
printCommands = False



"""
************** Tool Functions **************
"""
#Function to check if the user is within a database
def inDataBase():
    global currentDB

    if currentDB == "":
        return False
    else:
        return True

#Function to check if the requested table exist
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


"""
************** Custom Objs **************
"""

class tableVarRep:
    def __init__(self, TableName, TableNameVar):

        #print("Table name is: " + TableName)
        #print("Table name var is: " + TableNameVar)

        self.TableName = TableName
        self.TableNameVar = TableNameVar
    def setItem(self,TableItem):
        self.TableItem = TableItem
    
    TableName = ""
    TableNameVar = ""
    TableItem = ""


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

    if cmd.split(' ')[0].isupper():  
        #print("splitting on upper")
        #print("cmd.split[0]: " + str(cmd.split((' ')[0])) )
        cmdSplit = cmd.split("CREATE TABLE ")
    else:
        #print("splitting on upper")
        cmdSplit = cmd.split("create table ")

    tableName = cmdSplit[1].split('(')[0]
    tableName = tableName.strip()
    if tableName[0].islower():
        tableName = tableName[0].upper() + tableName[1:]

    if tableName[0].islower():
        tableName[0] = tableName[0].upper()
    

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
    if tableName[0].islower():
        tableName = tableName[0].upper() + tableName[1:]
    

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
    if tableName[0].islower():
            tableName = tableName[0].upper() + tableName[1:]

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
    if cmd.split(' ')[0].isupper():
        cmdSplit = cmd.split("SELECT * FROM ")
        Tables = cmdSplit[1].split("WHERE")[0]
        if "," in Tables:
            selectStarVar(cmd)
            return
    else:
        cmdSplit = cmd.split("select * from ")
        Tables = cmdSplit[1].split("WHERE")[0]
        if "," in Tables:
            selectStarVar(cmd)
            return

        


    tableName = cmdSplit[1]
    if tableName[0].islower():
        tableName = tableName[0].upper() + tableName[1:]

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


#This function takes in a string consisting with values table and new variable instances
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

    #Cleaning the new vars 
    newVars = newVars[1:-1]
    newVars = newVars.replace(' ','')
    newVars = newVars.replace('\t','')
    newVars = newVars.replace('\'','')
    newVars = newVars.replace('\n','')
    newVars = newVars.split(',')

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

    k = 0

    #parse through database adding the amount of new variables to the total length of the database
    for i in range(len(databaseCopy)+len(newVars)):
        #If the current line is the start of the correct table
        #print("Checking line: " + str(databaseCopy[i]))
        #print("Against: " + (">>" + insertTable + "\n"))
        if databaseCopy[i] == (">>" + insertTable + "\n"):
            #j = i
            #print("\tPASSED J: " + str(j) + " I: " + str(i))
            #parse theought the variable instances
            for j in range(i,len(databaseCopy)+len(newVars)):
                #if the current line is a variable
                #print("J:" + str(j))
                if databaseCopy[j][0] == "*":
                    k = j + 1 
                    #Parse until we reach a diffrent bariable
                    while databaseCopy[k][0] != "*":
                        #make sure we are not at the end of the database
                        if databaseCopy[k] == "<<\n":
                            break
                        k += 1
                    #Add encoding to the new variable
                    if len(newVars) > 0:
                        #print("K is: " +  str(k))
                        buffer = "$" +  newVars.pop(0) + '\n'
                        #append the new variable
                        databaseCopy.insert(k,buffer)
        i = k
    #Write the database copy to file
    fp = open(currentDB,'w')

    for line in databaseCopy:
        fp.write(line)

    fp.close()
    #alert the user of the update
    print("-- 1 new record inserted.")

#updateWhere takes in a user command and updates the table based on the 
# condition within the user command
def updateWhere(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Parsing the users command
    cmdList = cmd.split()

    tableName = cmdList[1].strip()
    if tableName[0].islower():
        tableName = tableName[0].upper() + tableName[1:]

    newValueVar = cmdList[3].strip()
    newValueVar = newValueVar.replace('\'','')

    newValue = cmdList[5].strip()
    newValue = newValue.replace('\'','')
    
    whereVar = cmdList[7].strip()

    whereVarValue = cmdList[9].strip()
    whereVarValue = whereVarValue.replace('\'','')

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

    #parse through the database
    for i in range(len(databaseCopy)):
        #If the current line in the database contains the variable defined in where
        if whereVar in databaseCopy[i]:
            i += 1
            #look at the lines until we reach a variable definition
            while databaseCopy[i][0] != "*":
                #If the current line satisfys the where condition
                if databaseCopy[i] == ("$" + whereVarValue + '\n'):
                    #Add its position to the list of positions
                    whereValuePositions.append(currentCount)
                currentCount += 1
                i += 1

    #Parse through the positions to be updated
    for i in range(len(whereValuePositions)):
        #Parse through the database for each position to be corrected
        for j in range(len(databaseCopy)):
            if newValueVar in databaseCopy[j]:
                j += 1
                #Adjust the needed variable
                databaseCopy[j+whereValuePositions[i]] = ("$" + newValue + '\n')

    #Write databaseCopy to file
    fp = open(currentDB,'w')

    for line in databaseCopy:
        fp.write(line)

    fp.close()

    #Update user
    if len(whereValuePositions) <= 1:
        print("-- " + str(len(whereValuePositions)) + " record modified.")
    else:
        print("-- " + str(len(whereValuePositions)) + " records modified.")

#deleteWhere takes in a command from a user and deletes the tuple based on a conditon form the user
def deleteWhere(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    #Parsing the user command for needed data
    cmdList = cmd.split('delete from')[1]
    cmdList = cmdList.split(' ')

    tableName = cmdList[1]
    if tableName[0].islower():
        tableName = tableName[0].upper() + tableName[1:]

    
    deleteVar = cmdList[3]

    deleteOperator = cmdList[4]

    deleteDomain = cmdList[5]
    deleteDomain = deleteDomain.replace('\'','')

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

        #Repeat below process for each 
        for j in range(len(deletePosition)):
            #Start by looking for the correcttable
            for i in range(len(databaseCopy)):
                #If the current line is the start of the correct table
                    if databaseCopy[i] == (">>" + tableName + "\n"):
                        while databaseCopy[i] != "<<"+"\n":
                            if databaseCopy[i][0] == "*":
                                databaseCopy.pop(i+deletePosition[j]+1)
                                
                            i += 1
                        break
            deletePosition = adjustArray(deletePosition)


    elif deleteOperator == '>':
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
        #Deleting the specfied row

        #Repeat below process for each 
        for j in range(len(deletePosition)):
            #Start by looking for the correcttable
            for i in range(len(databaseCopy)):
                #If the current line is the start of the correct table
                    if databaseCopy[i] == (">>" + tableName + "\n"):
                        while databaseCopy[i] != "<<"+"\n":
                            if databaseCopy[i][0] == "*":  
                                databaseCopy.pop(i+deletePosition[j]+1)

                            i += 1
                        break
            deletePosition = adjustArray(deletePosition)


    elif deleteOperator == '<':
        for i in range(len(databaseCopy)):
            if databaseCopy[i] == ('*' + deleteVar + '\n'):
                while databaseCopy[i] != "<<\n":
                    buffer = databaseCopy.replace('$','')
                    if float(buffer) < float(deleteDomain):
                        databaseCopy.pop(i)
                        itemsDeletedCount += 1
                    i += 1
    else:
        print("-- Could not delete uknown operator: " + str(deleteOperator))


    #Write to file
    fp = open(currentDB,'w')

    for line in databaseCopy:
        fp.write(line)

    fp.close()

    #Update user
    if len(deletePosition) <= 1:
        print("-- " + str(len(deletePosition)) + " record deleted.")
    else:
        print("-- " + str(len(deletePosition)) + " records deleted.")

#selectWhere takes in a user command of variable the user wants to see and 
#the condition under they will be seen
def selectWhere(cmd):
    
    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    


    #Seperating the command from the intended database    
    if cmd.split(' ')[0].isupper():
        cmdSplit = cmd.split("SELECT")[1]
    else:
        cmdSplit = cmd.split("select")[1]

        cmdSplit = cmdSplit.split("where")

        condition = cmdSplit[1]
        condition = condition.split(' ')
        condition.pop(0)

        cmdSplit = cmdSplit[0]

        cmdSplit = cmdSplit.split("from")

        tableName = cmdSplit[1]
        tableName = tableName.strip()
        if tableName[0].islower():
            tableName = tableName[0].upper() + tableName[1:]

        cmdSplit = cmdSplit[0]

        printArguments = cmdSplit.split(',')
        for i in range(len(printArguments)):
            printArguments[i] = cleanString(printArguments[i])
        #printArguments = printArguments.strip()

    #Opening the database 
    fp = open(currentDB,'r')

    #and copying the database to a string arr
    databaseCopy = fp.readlines()

    #close fp 
    fp.close

    #The case that the user is not within a database 
    if not inDataBase():
        print("-- !Failed to search table " + tableName + " not currently in a database.")
        return

    #The vase that the user wants to insert into a table that does not exist
    if not doesTableExist(tableName):
        print("-- !Failed to search table " + tableName + " because it does not exist.")
        return


    vars = []
    #Loading the variables into seperate arrays
    for i in range(len(databaseCopy)):
        #If the current line is equal to the user selected database
        if databaseCopy[i] == ">>" + tableName + "\n":
            j = i
            for j in range(len(databaseCopy)):
                buffer = []
                #if we are looking at a new variable
                if databaseCopy[j][0] == "*":
                    #Append the variable defenetion to the first position of the list
                    buffer.append(databaseCopy[j])
                    k = j + 1
                    #Keep steping through until we are looking at a new variable
                    while databaseCopy[k][0] != "*":
                        #Append each instace of it to a list
                        buffer.append(cleanString(databaseCopy[k]))
                        #Make sure we are not at the end of the database
                        if databaseCopy[k] =="<<\n":
                            break
                        k += 1
                    vars.append(buffer)
                    if databaseCopy[j] == "<<\n":
                        break
    #Clean the vars of extra charachters
    for i in range(len(vars)):
        vars[i][0] = vars[i][0].replace('\n','')
        vars[i][0] = vars[i][0].strip()
        vars[i][0] = vars[i][0].replace('*','')


    printPosition = 0
    printPositionList = []

    #Get the positions of all of the values that meet thr condition
    for i in range(len(vars)):
        if condition[0] in vars[i][0]:
            #print("in here")
            if condition[1] == '!=':
                for j in range(1,len(vars[i])):
                    if vars[i][j] != condition[2]:
                        printPositionList.append(printPosition)
                    printPosition += 1
    

            

    masterPrintArguments = []

    for i in range(len(printArguments)):
        for j in range(len(vars)):
            if printArguments[i] in vars[j][0]:
                masterPrintArguments.append(vars[j])
    
    
    #Formated printing
    #First printing the variable defenetions
    print("-- ",end="")
    for i in range(len(masterPrintArguments)):
        print(masterPrintArguments[i][0],end="")
        if i != len(masterPrintArguments)-1:
                print("|",end="")
    print()

    #Second printing the variable instances
    for i in range(len(printPositionList)):
        print("-- ",end="")
        for j in range(len(masterPrintArguments)):
            print(masterPrintArguments[j][printPositionList[i]+1],end="")
            if j != len(masterPrintArguments)-1:
                print("|",end="")
        print()

def selectStarVar(cmd): 

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    whereCondition = ""

    #Seperating the command from the intended database    
    if cmd.split(' ')[0].isupper():
        cmdSplit = cmd.split("SELECT * FROM ")
        Tables = cmdSplit[1].split("WHERE")[0]
        whereCondition = cmdSplit[1].split("WHERE")[1]
        Tables = Tables.split(",")

        TablesList = []

        for i in range(len(Tables)):
            Tables[i] = Tables[i].strip()
            #print("Reading line: " + Tables[i])
            tableName = Tables[i].split(" ")[0]
            tableVar = Tables[i].split(" ")[1]
            bufferTableVar = tableVarRep(tableName,tableVar)
            TablesList.append(bufferTableVar)

    else:
        cmdSplit = cmd.split("select * from ")
        Tables = cmdSplit[1].split("where")[0]
        whereCondition = cmdSplit[1].split("where")[1]
        Tables = Tables.split(",")

        TablesList = []

        #Loading the table variables into a tableVarRep custom obj
        for i in range(len(Tables)):
            Tables[i] = Tables[i].strip()
            #print("Reading line: " + Tables[i])
            tableName = Tables[i].split(" ")[0]
            tableVar = Tables[i].split(" ")[1]
            bufferTableVar = tableVarRep(tableName,tableVar)
            TablesList.append(bufferTableVar)
    

    #Getting the where condition from the command
    whereCondition = whereCondition.strip()
    whereCondition = whereCondition.split(" ")
    whereConditionL = whereCondition[0]
    whereConditionR = whereCondition[2]
    whereConditionEvaluator = whereCondition[1]

    #Getting the Table that we are trying to search an item for the LHS
    leftTableVar = whereConditionL.split(".")[0]
    leftTableItem = whereConditionL.split(".")[1]

    #Getting the Table that we are trying to search an item for the RHS
    rightTableVar = whereConditionR.split(".")[0]
    rightTableItem = whereConditionR.split(".")[1]

    #print("LHS TableVar: " + leftTableVar + " TableItem: " + leftTableItem)
    #print("RHS TableVar: " + rightTableVar + " TableItem: " + rightTableItem)


    #assining the custom objs their table Item
    #LHS
    for i in range(len(TablesList)):
        if TablesList[i].TableNameVar == leftTableVar:
            TablesList[i].setItem(leftTableItem)

    #RHS
    for i in range(len(TablesList)):
        if TablesList[i].TableNameVar == rightTableVar:
            TablesList[i].setItem(rightTableItem)

    #Opening the database 
    fp = open(currentDB,'r')

    #and copying the database to a string arr
    databaseCopy = fp.readlines()

    #close fp 
    fp.close

    #The case that the user is not within a database 
    if not inDataBase():
        print("-- !Failed to search table " + tableName + " not currently in a database.")
        return

    #The vase that the user wants to insert into a table that does not exist

    LHSVarsInstances = []
    RHSVarsInstances = []

    currentSide = "L"

    for i in range(len(TablesList)):
        
        #Search for the current TabesList[i].TableName
        for j in range(len(databaseCopy)):

            #Check if the current line is the start of the table
            if databaseCopy[j] == (">>" + TablesList[i].TableName + "\n"):
                
                #If the line has been found we now start searching for the correct table item
                for k in range(j,len(databaseCopy)):
                    
                    #Check if the current line is equal to the table item
                    if TablesList[i].TableItem in databaseCopy[k]:
                        
                        #Start a loop at one position past where we found the variable def
                        l = k+1
                        #While we are not at a new variable append the items to the LHSVarsInstances List
                        while databaseCopy[l][0] != "*":
                            if currentSide == "L":
                                buffer = databaseCopy[l].replace('$','')
                                buffer = buffer.replace('\n','')
                                LHSVarsInstances.append(buffer)
                            elif currentSide == "R":
                                buffer = databaseCopy[l].replace('$','')
                                buffer = buffer.replace('\n','')
                                RHSVarsInstances.append(buffer)
                            l += 1
                        if currentSide == "L":
                            currentSide = "R"
    #print("LHS Var instances: " + str(LHSVarsInstances))
    #print("RHS Var instances: " + str(RHSVarsInstances))

    #Find the matches
    matchPositions = []
    #Loop through the right hand side
    for i in range(len(LHSVarsInstances)):
        #For each right hand side
        for j in range(len(RHSVarsInstances)):
            if LHSVarsInstances[i] == RHSVarsInstances[j]:
                buffer = []
                buffer.append(i)
                buffer.append(j)
                matchPositions.append(buffer)
    
    #print("Match Positions")
    #print(matchPositions)


    #Get the list of vars
    varDefs = "-- "
    for i in range(len(TablesList)):
        #Loop through the databasecopy
        for j in range(len(databaseCopy)):
            #Check if the current line is equal to the table
            if databaseCopy[j] == (">>" + TablesList[i].TableName + "\n"):
                #Loop through the table
                #starting at one postion pas the start of the table
                k = j+1
                while databaseCopy[k] != "<<\n":
                    #If the current line is a variable defenetion
                    if databaseCopy[k][0] == "*":
                        #print("Found line: " + databaseCopy[k])
                        buffer = databaseCopy[k]
                        buffer = buffer.replace("*",'')
                        buffer = buffer.replace("\n",'')
                        buffer += "|"
                        varDefs += buffer
                    k += 1
    varDefs = varDefs[:-1]
    print(varDefs)

    #Get a string for each matched position
    varInstancePrint = "-- "
    LHSPrint = ""
    RHSPrint = ""
    varPosition = 0
    for i in range(len(matchPositions)):
        #Find the start of the first table
        for j in range(len(databaseCopy)):
            #Check if the current line is equal to the LHS table
            if databaseCopy[j] == (">>" + TablesList[0].TableName + "\n"):
                #Loop through the table
                k = j+1
                while databaseCopy[k] != "<<\n":
                    #Check if we are at a variable defnetion
                    if databaseCopy[k][0] == "*":
                        #print("Found line: " + databaseCopy)
                        #Loop through the variable defenetions
                        l = k +1
                        varPosition = l + matchPositions[i][0]
                        while databaseCopy[l][0] != "*":
                            if l == varPosition:
                                buffer = databaseCopy[l]
                                buffer = buffer.replace("$","")
                                buffer = buffer.replace("\n","")
                                buffer += "|"
                                LHSPrint += buffer
                            l += 1
                    k += 1
                k = 0
                l = 0
            #Check if the current line is equal to the RHS table
            elif databaseCopy[j] == (">>" + TablesList[1].TableName + "\n"):
                #Loop through the table
                k = j+1
                while databaseCopy[k] != "<<\n":
                    #Check if we are at a variable defnetion
                    if databaseCopy[k][0] == "*":
                        #print("Found line: " + databaseCopy)
                        #Loop through the variable defenetions
                        l = k +1
                        varPosition = l + matchPositions[i][1]
                        while databaseCopy[l][0] != "*" and databaseCopy[l] != "<<\n":
                            #print("DatabaseCopy at " + str(l) + ": " + databaseCopy[l])
                            if l == varPosition:
                                buffer = databaseCopy[l]
                                buffer = buffer.replace("$","")
                                buffer = buffer.replace("\n","")
                                buffer += "|"
                                LHSPrint += buffer
                            l += 1
                        #print("Broke at end of variable")
                    k += 1
                k = 0
                l = 0
        varInstancePrint += LHSPrint
        varInstancePrint += RHSPrint  
        varInstancePrint = varInstancePrint[:-1]    
        print(varInstancePrint)
        varInstancePrint = "-- "
        LHSPrint = ""
        RHSPrint = ""

        
        
def selectWhereJoin(cmd):

    #For debuging
    global printCommands
    if printCommands:
        print(cmd)

    global currentDB

    Tables = []

    isLeftOuterJoin = False

    if cmd.split(' ')[0].isupper():

        cmdSplit = cmd.split("SELECT * FROM ")

        if "INNER JOIN" in cmd:
            buffer = cmdSplit[1].split("INNER JOIN")[0]
            buffer = buffer.strip()
            Tables.append(buffer)
            secondTable = cmdSplit[1].split("INNER JOIN")[1]
            buffer = secondTable.split("ON")[0]
            buffer = buffer.strip()
            Tables.append(buffer)

            condition = cmd.split("ON")[1]
            condition = condition.strip()
            condition = condition.split(" ")

            #print("Condition statment: " + str(condition))

            conditionL = condition[0]
            conditionEvaluator = condition[1]
            conditionR = condition[2]

    else:
        cmdSplit = cmd.split("select * from ")

        if "inner join" in cmd:
            buffer = cmdSplit[1].split("inner join")[0]
            buffer = buffer.strip()
            Tables.append(buffer)
            secondTable = cmdSplit[1].split("inner join")[1]
            buffer = secondTable.split("on")[0]
            buffer = buffer.strip()
            Tables.append(buffer)

            condition = cmd.split("on")[1]
            condition = condition.strip()
            condition = condition.split(" ")

            #print("Condition statment: " + str(condition))

            conditionL = condition[0]
            conditionEvaluator = condition[1]
            conditionR = condition[2]
        elif "left outer join" in cmd:
            isLeftOuterJoin = True
            buffer = cmdSplit[1].split("left outer join")[0]
            buffer = buffer.strip()
            Tables.append(buffer)
            secondTable = cmdSplit[1].split("left outer join")[1]
            buffer = secondTable.split("on")[0]
            buffer = buffer.strip()
            Tables.append(buffer)

            condition = cmd.split("on")[1]
            condition = condition.strip()
            condition = condition.split(" ")

            #print("Condition statment: " + str(condition))

            conditionL = condition[0]
            conditionEvaluator = condition[1]
            conditionR = condition[2]


    #print("Condition L: " + conditionL)
    #print("Condition R: " + conditionR)

    #Getting the Table that we are trying to search an item for the LHS
    leftTableVar = conditionL.split(".")[0]
    leftTableItem = conditionL.split(".")[1]
    
    #Getting the Table that we are trying to search an item for the RHS
    rightTableVar = conditionR.split(".")[0]
    rightTableItem = conditionR.split(".")[1]

    #print("LHS TableVar: " + leftTableVar + " TableItem: " + leftTableItem)
    #print("RHS TableVar: " + rightTableVar + " TableItem: " + rightTableItem)

    TablesList = []

    for i in range(len(Tables)):
            Tables[i] = Tables[i].strip()
            #print("Reading line: " + Tables[i])
            tableName = Tables[i].split(" ")[0]
            tableVar = Tables[i].split(" ")[1]
            bufferTableVar = tableVarRep(tableName,tableVar)
            TablesList.append(bufferTableVar)


    #assining the custom objs their table Item
    #LHS
    for i in range(len(TablesList)):
        if TablesList[i].TableNameVar == leftTableVar:
            TablesList[i].setItem(leftTableItem)

    #RHS
    for i in range(len(TablesList)):
        if TablesList[i].TableNameVar == rightTableVar:
            TablesList[i].setItem(rightTableItem)

    #Opening the database 
    fp = open(currentDB,'r')

    #and copying the database to a string arr
    databaseCopy = fp.readlines()

    #close fp 
    fp.close

    #The case that the user is not within a database 
    if not inDataBase():
        print("-- !Failed to search table " + tableName + " not currently in a database.")
        return

    #The vase that the user wants to insert into a table that does not exist

    LHSVarsInstances = []
    RHSVarsInstances = []

    currentSide = "L"

    for i in range(len(TablesList)):
        
        #Search for the current TabesList[i].TableName
        for j in range(len(databaseCopy)):

            #Check if the current line is the start of the table
            if databaseCopy[j] == (">>" + TablesList[i].TableName + "\n"):
                
                #If the line has been found we now start searching for the correct table item
                for k in range(j,len(databaseCopy)):
                    
                    #Check if the current line is equal to the table item
                    if TablesList[i].TableItem in databaseCopy[k]:
                        
                        #Start a loop at one position past where we found the variable def
                        l = k+1
                        #While we are not at a new variable append the items to the LHSVarsInstances List
                        while databaseCopy[l][0] != "*":
                            if currentSide == "L":
                                buffer = databaseCopy[l].replace('$','')
                                buffer = buffer.replace('\n','')
                                LHSVarsInstances.append(buffer)
                            elif currentSide == "R":
                                buffer = databaseCopy[l].replace('$','')
                                buffer = buffer.replace('\n','')
                                RHSVarsInstances.append(buffer)
                            l += 1
                        if currentSide == "L":
                            currentSide = "R"
    #print("LHS Var instances: " + str(LHSVarsInstances))
    #print("RHS Var instances: " + str(RHSVarsInstances))

    #Find the matches
    matchPositions = []
    matchFound = False
    #Loop through the right hand side
    for i in range(len(LHSVarsInstances)):
        #For each right hand side
        for j in range(len(RHSVarsInstances)):
           #print("Checking: " + LHSVarsInstances[i])
            if LHSVarsInstances[i] == RHSVarsInstances[j]:
                matchFound = True
                buffer = []
                buffer.append(i)
                buffer.append(j)
                matchPositions.append(buffer)
        if matchFound == False and  isLeftOuterJoin == True:
            buffer = []
            buffer.append(i)
            buffer.append(-1)
            matchPositions.append(buffer)
        elif matchFound == True:
            matchFound = False
    
    #print("Match Positions")
    #print(matchPositions)


    #Get the list of vars
    varDefs = "-- "
    for i in range(len(TablesList)):
        #Loop through the databasecopy
        for j in range(len(databaseCopy)):
            #Check if the current line is equal to the table
            if databaseCopy[j] == (">>" + TablesList[i].TableName + "\n"):
                #Loop through the table
                #starting at one postion pas the start of the table
                k = j+1
                while databaseCopy[k] != "<<\n":
                    #If the current line is a variable defenetion
                    if databaseCopy[k][0] == "*":
                        #print("Found line: " + databaseCopy[k])
                        buffer = databaseCopy[k]
                        buffer = buffer.replace("*",'')
                        buffer = buffer.replace("\n",'')
                        buffer += "|"
                        varDefs += buffer
                    k += 1
    varDefs = varDefs[:-1]
    print(varDefs)

    #Get a string for each matched position
    varInstancePrint = "-- "
    LHSPrint = ""
    RHSPrint = ""
    varPosition = 0
    for i in range(len(matchPositions)):
        #Find the start of the first table
        for j in range(len(databaseCopy)):
            #Check if the current line is equal to the LHS table
            if databaseCopy[j] == (">>" + TablesList[0].TableName + "\n"):
                #Loop through the table
                k = j+1
                while databaseCopy[k] != "<<\n":
                    #Check if we are at a variable defnetion
                    if databaseCopy[k][0] == "*":
                        #print("Found line: " + databaseCopy)
                        #Loop through the variable defenetions
                        l = k +1
                        varPosition = l + matchPositions[i][0]
                        while databaseCopy[l][0] != "*":
                            if l == varPosition:
                                buffer = databaseCopy[l]
                                buffer = buffer.replace("$","")
                                buffer = buffer.replace("\n","")
                                buffer += "|"
                                LHSPrint += buffer
                            l += 1
                    k += 1
                k = 0
                l = 0
            #Check if the current line is equal to the RHS table
            elif databaseCopy[j] == (">>" + TablesList[1].TableName + "\n"):
                #Loop through the table
                k = j+1
                while databaseCopy[k] != "<<\n":
                    #Check if we are at a variable defnetion
                    if databaseCopy[k][0] == "*":
                        #print("Found line: " + databaseCopy)
                        #Loop through the variable defenetions
                        l = k +1
                        varPosition = l + matchPositions[i][1]
                        while databaseCopy[l][0] != "*" and databaseCopy[l] != "<<\n":
                            #print("DatabaseCopy at " + str(l) + ": " + databaseCopy[l])
                            if l == varPosition and matchPositions[i][1] != -1:
                                buffer = databaseCopy[l]
                                buffer = buffer.replace("$","")
                                buffer = buffer.replace("\n","")
                                buffer += "|"
                                RHSPrint += buffer
                            elif matchPositions[i][1] == -1:
                                RHSPrint += "|"
                                break
                            l += 1
                        #print("Broke at end of variable")
                    k += 1
                k = 0
                l = 0
        varInstancePrint += LHSPrint
        varInstancePrint += RHSPrint  
        varInstancePrint = varInstancePrint[:-1]    
        print(varInstancePrint)
        varInstancePrint = "-- "
        LHSPrint = ""
        RHSPrint = ""




                



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

        if ".EXIT" in userCommand or ".exit" in userCommand:
            print("-- All done.")
            break


        #In the case on the first enter from the user the command does not end
        # with a ';' keep looping until a command ends in ';'
        if userCommand != '' and "--" not in userCommand:
            if (userCommand[len(userCommand)-1] != ';') and userCommand != (".EXIT" or ".exit") :
                while True:
                    userCommand += input()
                    if userCommand[len(userCommand)-1] == ';':
                        break
        if userCommand == '':
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
        elif 'CREATE DATABASE' in userCommand or "create database " in userCommand: #Done
            createDatabase(userCommand)
        elif "CREATE TABLE"  in userCommand or "create table" in userCommand: #Done
            createTable(userCommand)
        elif "DROP DATABASE" in userCommand: #Done
            dropDatabase(userCommand)
        elif "DROP TABLE"in userCommand: #Done
            dropTable(userCommand)
        elif "ALTER TABLE"in userCommand:
            alterTable(userCommand)
        elif "on" in userCommand or "ON" in userCommand:
            selectWhereJoin(userCommand)
        elif ("SELECT" in userCommand or "select " in userCommand) and "*" not in userCommand:
            selectWhere(userCommand)
        elif "SELECT *" in userCommand or "select *" in userCommand: #Done
            selectStar(userCommand)
        elif "insert into" in userCommand:
            insertInto(userCommand)
        elif "update" in userCommand:
            updateWhere(userCommand)
        elif "delete from" in userCommand:
            deleteWhere(userCommand)
        elif ".EXIT" in userCommand or ".exit" in userCommand:
            print("-- All done.")
            break



opLoop()
