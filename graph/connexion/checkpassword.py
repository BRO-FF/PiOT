import re
import sys
import crypt
import cherrypy
import hashlib
import random
import string
import mysql.connector
from contextlib import closing

def checkpass(username, password):
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="corpus",
          password="toor",
          database="corpus"
        )

        with closing( mydb.cursor() ) as mycursor:
            mycursor.execute("SELECT 1 FROM passwd LIMIT 1;")
            emptyDB = mycursor.fetchall()
            
            mycursor.execute("SELECT pass,salt FROM passwd WHERE user='" + username + "';")
            records = mycursor.fetchall()

            if emptyDB == []:
                return "emptyDB"
            elif records == []:
                return False
            else:
                unlist = records[0]
                passwd = unlist[0]
                salt = unlist[1]
                
                passToHash = password + salt
                m = hashlib.sha256()
                m.update(passToHash.encode('utf8'))
                passHashed = m.hexdigest()

                if passHashed != passwd:
                    return False
                elif passHashed == passwd:
                    return True

    except mysql.connector.errors.ProgrammingError:
        return False
    finally:
        mydb.close()
        pass

def enrollement(username, password):
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="corpus",
          password="toor",
          database="corpus"
        )

        # Salt
        length = 5
        letters = string.ascii_lowercase
        salt = ''.join(random.choice(letters) for i in range(length))

        # Password
        passToHash = password + salt
        m = hashlib.sha256()
        m.update(passToHash.encode('utf8'))
        passHashed = m.hexdigest()

        # Insert creds
        with closing( mydb.cursor() ) as mycursor:
            mycursor.execute("INSERT INTO passwd (user,pass,salt) VALUES ('" + username + "','" + passHashed + "','" + salt + "');")
            mydb.commit()
        return True

    except mysql.connector.errors.ProgrammingError:
        return False
    finally:
        mydb.close()
        pass

def setCookie(ipUser):

    salt2 = "Master Hash"
    stringToHash = ipUser + salt2

    m = hashlib.sha256()
    m.update(stringToHash.encode('utf8'))
    stringHashed = m.hexdigest()

    cookie = cherrypy.response.cookie
    cookie['cookieName'] = stringHashed
    cookie['cookieName']['path'] = '/'
    cookie['cookieName']['max-age'] = 3600
    cookie['cookieName']['version'] = 1

def readCookie(ipUser):

    salt2 = "Master Hash"
    stToHash = ipUser + salt2

    m = hashlib.sha256()
    m.update(stToHash.encode('utf8'))
    stHashed = m.hexdigest()

    cookie = cherrypy.request.cookie
    for name in cookie.keys():
        if name == "cookieName":
            if cookie[name].value == stHashed:
                return True
    return False
