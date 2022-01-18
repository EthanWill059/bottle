
##### Imports #####
import sqlite3
from bottle import *
from time import sleep
from os import system, remove
from sqlite3 import *
from random import randint
###################

# setup for server
app = Bottle()
##

## Database
def connectdb(): # for reuse
    print('Attemping to connect to Database...')
    global db
    db = connect('users.db')
connectdb()



#### Utilities ####

def check_login(name, passw): # confirms the password
    try:
        cur = db.execute("SELECT password FROM USERS WHERE username = ?", (name,))
        row = cur.fetchone()
        if row[0] == passw:
            return True
        else:
            raise DatabaseError
    except:
        return False

def authAdmin(name):
    cur = db.execute("SELECT admin FROM USERS WHERE username = ?", (name,))
    row = cur.fetchone()
    if row[0] == True:
        return True
    else:
        return False

def isAdmin():
    status = request.get_cookie("isAdmin", secret=123)
    if status:
        return True
    else:
        return False

#####################

## Backend and frontend, ie the majority of code ##


@route('/') #redirect based on cookies, logged in users can skip login page
def movedaguy():
    loggedin = request.get_cookie("loggedin", secret="secretvalue")
    if loggedin: 
        redirect('/home')
    else:
        redirect('/login')



### Login and sign up Page ###
@get('/login') 
def login():
        return '''
        <html>
        <body>

        <style>
        body {
            background-color: lightblue;
        } 
        h1 {
            color: navy;
            margin-left: 20px;
        }
        </style>
        
        <h1><center> Login </h1>
        <form action="/login" method="post" autocomplete="off"><center> <br> <br> <br>
        Username: <input name="username" type="text" required/> <br> <br>
        Password: <input name="password" type="password" required/> <br> <br>
        <input value="Login" type="submit" />
        </form>

        
        </body>
        </html>
        '''

@post('/login') 
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if check_login(username, password) == True:
        response.set_cookie("loggedin", username, secret="secretvalue")
        if authAdmin(username) == True:
            response.set_cookie("isAdmin", True, secret=123)
        redirect('/home')
    else:
        return redirect('/')


takenusr = False
trieduser = "NULL"
@get('/signup')
def signupform():
    if takenusr == False:
        return '''
            <html>
            <body>

            <style>
            body {
                background-color: lightblue;
            } 
            h1 {
                color: navy;
                margin-left: 20px;
            }
            </style>

            

            <h1><center> Sign Up </h1>
            <form action="/signup" method="post" autocomplete="off"><center> <br> <br> <br>
            Username: <input name="username" id="username" type="text" required/> <br> <br>
            Password: <input name="password" id="password" type="password" required  /> <br> <br>
            Password: <input id="password-repeat" type="password" placeholder="confirm" required /> <br> <br>
            <input value="Sign Up" type="submit" />
            </form>

            <script>
            var password = document.getElementById("password");
            var confirm_password = document.getElementById("password-repeat");
            
            function validatePassword(){
            if(password.value != confirm_password.value) {
            confirm_password.setCustomValidity("Passwords Don't Match");
            } else {
            confirm_password.setCustomValidity('');
            }
            }
            
            password.onchange = validatePassword;
            confirm_password.onkeyup = validatePassword;
            </script>

            </body>
            </html>    
        '''
    else:
        return '''
        <html>
        <body>

        <style>
        body {
            background-color: lightblue;
        } 
        h1 {
            color: navy;
            margin-left: 20px;
        }
        p {
            color: red
        }
        </style>

            

        <h1><center> Sign Up </h1>
        <p> Username '{}' already taken! </p>
        <form action="/signup" method="post" autocomplete="off"><center> <br> <br> <br>
        Username: <input name="username" id="username" type="text" required/> <br> <br>
        Password: <input name="password" id="password" type="password" required  /> <br> <br>
        Password: <input id="password-repeat" type="password" placeholder="confirm" required /> <br> <br>
        <input value="Sign Up" type="submit" />
        </form>

        <script>
        var password = document.getElementById("password");
        var confirm_password = document.getElementById("password-repeat");
            
        function validatePassword(){
        if(password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Passwords Don't Match");
        } else {
        confirm_password.setCustomValidity('');
        }
        }
            
        password.onchange = validatePassword;
        confirm_password.onkeyup = validatePassword;
        </script>

        </body>
        </html>    
        '''.format(trieduser)

@post('/signup')
def SignUpFormPost():
    if isAdmin():
        global takenusr
        global trieduser
        username = request.forms.get('username')
        password = request.forms.get('password')
        print(username)
        print(password)
        cur = db.execute('SELECT username FROM users WHERE username=?', (username,))
        checkUsername = cur.fetchone() # sets the result of SQL query to a varible, str
        if checkUsername != 0:
            db.execute("INSERT INTO USERS (username, password, admin) VALUES (?, ?, False)", (username, password))
            db.commit()
            takenusr = False
            trieduser = "NULL"
            redirect('/login')
        else:
            takenusr = True
            trieduser = username
            redirect('/signup')
### ###




@route('/home')
def home(): # the main page of the app

    ### requesting cookies
    loggedin = request.get_cookie("loggedin", secret="secretvalue")
    auth = isAdmin()
    ###

    if auth == True:
        ################# HTML FOR HOME PAGE ####################
        return """
        <!DOCTYPE html>
        <html>
        <style>
        body {
            background-color: lightblue;
        } 
        h1 {
            color: navy;
            margin-left: 20px;
        }
        .titletext {
            text-align: center; 
            color: darkblue;
        }

        form{
            text-align: center;   
        }

        input{
            padding: 10px 20px
        }

        .btncontain{
            text-align: center;
        }
        </style>
        <body>

        <h1 class = titletext>Home Page</h1>
        <h2> Repair Ticketing Checklist </h2>
        <p> - Get to record all information <br> 
            - Ask for Name and phone number if unknown <br>
            - Ask if they would like to be contacted by phone, if not get another form of contact <br><br>
            - NOW, get information about the device and whats wrong with it <br>
            - After recording this give them an estimate of cost from <a href='https://gatech.co.nz/' target="_blank">GATECH</a> <br>
            - Organise how you are going to get the phone and how you'll give it back
            - Say your Goodbye formalites and hang up
        </p>

        <div class="btncontain">
        <button onclick="window.location.href='https://gatech.co.nz/';">
        Parts
        </button>
        <button onclick="window.location.href='/createticket';">
        Create Ticket
        </button>
        </div>

        <br> <br>
        <form action="/home" method="post">
        Server Admin: <input name="input_box" type="text">
        <input value="submit text" type="submit" />
        </form>

        </body>
        </html>
        """
        #############################################

    elif loggedin: # displays home page without command box
        ################# HTML FOR HOME PAGE ####################
        return """
        <!DOCTYPE html>
        <html>
        <style>
        body {
            background-color: lightblue;
        } 
        h1 {
            color: navy;
            margin-left: 20px;
        }
        .titletext {
            text-align: center; 
            color: darkblue;
        }
        </style>
        <body>

        <h1 class = titletext>Home Page</h1>
        <h2> Repair Ticketing Checklist </h2>
        <p> - Get to record all information <br> 
            - Ask for Name and phone number if unknown <br>
            - Ask if they would like to be contacted by phone, if not get another form of contact <br><br>
            - NOW, get information about the device and whats wrong with it <br>
            - After recording this give them an estimate of cost from <a href='https://gatech.co.nz/' target="_blank">GATECH</a> <br>
            - Organise how you are going to get the phone and how you'll give it back
            - Say your Goodbye formalites and hang up
        </p>

        </body>
        </html>
        """
        #############################################
    else:
        return redirect('/')
    
@post('/home') # post request to get data from command input box on home page
def getinputs():
    auth = isAdmin()
    if auth == True:
        input = request.forms.get('input_box')
        print("\n\n  !!! EXECUTING FRONTEND ISSUED COMMAND !!!: ", input, end='\n \n')
        system(input)
        return redirect('/home')

@get('/createticket')
def createticket():
    loggedin = request.get_cookie("loggedin", secret="secretvalue")
    if loggedin:
        return '''
        <h1><center> Create Ticket </h1>
        <form action="/createticket" method="post"><center> <br> <br> <br>
        NAME: <input name="name" type="text" required/> <br> <br>
        DATE: <input name="date" type="date" required/> <br> <br>
        DEVICE: <input name="device" type="text" required/> <br> <br>
        DETAILS: <input name="details" type="text" required placeholder="Go into detail"/> <br> <br>
        <input value="Submit Ticket" type="submit" />
        </form>
        '''

@post('/createticket')
def getticket():
    name = request.forms.get('name')
    date = request.forms.get('date')
    device = request.forms.get('device')
    details = request.forms.get('details')
    print(name, date, device, details)
    conn = sqlite3.connect('tickets.db')
    conn.execute("INSERT INTO TICKETS (name, datelogged, device, details, openstatus) VALUES (?, ?, ?, ?, True)", (name, date, device, details,))
    conn.commit()
    redirect('/tickets')

@get('/tickets')
def showtickets():
    loggedin = request.get_cookie("loggedin", secret="secretvalue")
    if loggedin:
        conn = sqlite3.connect('tickets.db')
        c = conn.cursor()
        c.execute("SELECT id, name, datelogged, device FROM tickets WHERE openstatus LIKE '1'")
        result = c.fetchall()
        c.close()
        output = template('table', rows=result)
        return output

@get('/ticket/<ticketid>')
def ticketdetail(ticketid):
    loggedin = request.get_cookie("loggedin", secret="secretvalue")
    if loggedin:
        conn = sqlite3.connect('tickets.db')
        c = conn.cursor()
        c.execute("SELECT id, name, datelogged, device, details FROM tickets WHERE id LIKE '{}'".format(ticketid))
        result = c.fetchall()
        return str(result) 

### ADMIN UTILS ###
@route('/closeserver')
def auth():
    auth = isAdmin()
    if auth == True:
        return "server shutting off...", sleep(0.5), redirect('/')
    else:
        return redirect('/')

@route('/wipeuserdb')
def wipe():
    auth = isAdmin()
    if auth == True:
        os.remove('users.db')
        connectdb()
        db.execute('''CREATE TABLE USERS
         (USERNAME          TEXT    NOT NULL,
         PASSWORD          TEXT    NOT NULL,
         ADMIN             BOOL    NOT NULL);''')
        sleep(1)
        db.execute("INSERT INTO USERS (username, password, admin) VALUES (admin, admin, True)")
        return redirect('/')

@route('/makeadmin')
def makeadmin():
    user = request.get_cookie("loggedin", secret="secretvalue")
    print("!!REQUEST RECIVED FROM {} TO BE MADE ADMIN!!".format(user))
    key = randint(0000, 9999)
    print('Key = ', key)
    if input("TYPE KEY TO CONFIRM >> ") == str(key):
        db.execute("UPDATE USERS SET admin = True WHERE username = ?", (user,))
        db.commit()
        response.delete_cookie("loggedin", secret="secretvalue")
        redirect('/login')
    else:
        print('AUTH FAILED, REJECTED')

        

## HTTP Errors ##
@error(404)
@error(403)
def mistake(code):
    return '''
    <html>
    <body>

    <style>
    body {
        background-color: lightcoral;
    } 
    h1 {
        color: red;
        margin-left: 20px;
    }
    </style>
    
    <h1><center> ERROR 403/404</h1>
    
    <p><center> Either theres nothing here or you aren't allowed to see what is </p> 
    <br>
    <form><center>
      <input type="button" onclick="window.location.href='http://localhost:8080';" value="home" />
    </form>
    </body>
    </html> 
    '''

##  ##


run(host='localhost', port=8080, debug=True, reloader=True) 
