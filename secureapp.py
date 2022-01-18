
##### Imports #####
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

        <button onclick="window.location.href='/signup';">
        Sign Up
        </button>
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
    global takenusr
    global trieduser
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username)
    print(password)
    cur = db.execute('SELECT username FROM users WHERE username=?', (username,))
    checkUsername = cur.fetchone()
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
        </style>
        <body>

        <h1 class = titletext>Home Page</h1>
        <p>Welcome to worlds most protected and worst looking calculator</p>

 
        <form name="calculator">
        <input type="button" value="1" onClick="document.calculator.ans.value+='1'">
        <input type="button" value="2" onClick="document.calculator.ans.value+='2'">
        <input type="button" value="3" onClick="document.calculator.ans.value+='3'"><br>
        <input type="button" value="4" onClick="document.calculator.ans.value+='4'">
        <input type="button" value="5" onClick="document.calculator.ans.value+='5'">
        <input type="button" value="6" onClick="document.calculator.ans.value+='6'"><br>
        <input type="button" value="7" onClick="document.calculator.ans.value+='7'">
        <input type="button" value="8" onClick="document.calculator.ans.value+='8'">
        <input type="button" value="9" onClick="document.calculator.ans.value+='9'"><br>
        <input type="button" value="0" onClick="document.calculator.ans.value+='0'"><br>
        <input type="button" value="-" onClick="document.calculator.ans.value+='-'">
        <input type="button" value="+" onClick="document.calculator.ans.value+='+'">
        <input type="button" value="*" onClick="document.calculator.ans.value+='*'">
        <input type="button" value="/" onClick="document.calculator.ans.value+='/'"><br>
        <input type="reset" value="Reset">
        <input type="button" value="EXE" onClick="document.calculator.ans.value=eval(document.calculator.ans.value)">
        <br><input type="textfield" name="ans" value="">
        </form>

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
        <p>You've reached the homepage</p>

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
        print("EXECUTING FRONTEND ISSUED COMMAND: ", input, end='\n \n')
        system(input)
        return redirect('/home')


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
