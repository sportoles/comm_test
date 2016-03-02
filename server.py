#!/usr/bin/python

import SocketServer
import uuid

class User:
    def __init__(self, name = "Unknown", password = None):
        self.name = name
        self.password = password
        print "User created: " + self.name
        return

    def set_username(self, newName):
        self.name = newName
        return
    def set_password(self, newPassword):
        self.password = newPassword
        return
    def authenticate(self, checkPassword = None):
        if checkPassword == self.password:
            self.say("Authenticated")
            return 1
        else:
            self.say("Fail to authenticate")
            return 0

    def say(self, sentence):
        print "[" + self.name + "]: " + sentence
        return
    def say_hello(self):
        self.say("Hello")
        return

def find_user(user_list, name):
    if name is None:
        print "No user to find"
        return None
    for user in user_list:
        if user.name == name:
            #print "User found: " + name
            return user
    #print "User not found: " + name
    return None

class Session:
    def __init__(self, username):
        self.id = uuid.uuid4()
        self.username = username
    def getUuid(self):
        return self.id
    def getName(self):
        return self.username

def find_session_by_uuid(search_uuid):
    if search_uuid is None:
        print "No uuid given"
    for session in sessions:
        if session.getUuid().hex == search_uuid:
            return session
    return None

def find_session_by_name(search_name):
    if search_name is None:
        print "No name given"
    for session in sessions:
        if session.getName() == search_name:
            return session
    return None

def open_session(session_list, username):
    newSession = Session(username)
    session_list.append(newSession)
    return newSession.getUuid()

def login(data):
    print "Login trial"
    if not len(str.split(data)) == 4:
        print "Bad parameters!"
        return
    login_username = str.split(data)[1]
    if str.split(data)[2] == 'pass':
        login_password = str.split(data)[3]
    else:
        print "Password needed!"
        return
    print "User: " + login_username
    print "Password: " + login_password
    b_authentic = 0
    if not find_user(users,login_username):
        print "User not existing!"
        return
    b_authentic = find_user(users,login_username).authenticate(login_password)
    if b_authentic:
        return open_session(sessions,login_username)
    else:
        return

def create_users():
    users_created = []
    users_created.append(User())
    users_created.append(User("Juan", "ojo11"))
    return users_created

def test_users(user_list):
    user_list[0].say_hello()
    user_list[1].say_hello()
    user_list[0].authenticate()
    user_list[1].authenticate("oja11")
    user_list[1].authenticate("ojo11")
    find_user(user_list, "Juan")
    find_user(user_list, "Pedro")
    find_user(user_list, None)
    find_user(user_list,"Unknown").authenticate()
    find_user(user_list,"Juan").authenticate("ojo11")
    return

class AuthenticateHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        cmd = str.split(self.data)[0]
        if cmd == 'usr':
            resp = login(self.data)
            if resp is not None:
                self.request.sendall("OK " + resp.hex)
            else:
                self.request.sendall("NOK")
            return
        if cmd == 'ses':
            session_uuid = str.split(self.data)[1]
            session = find_session_by_uuid(session_uuid)
            if session is None:
                self.request.sendall("NOK")
                print "Seesion not found"
                return
            print "Session: " + session.getName()
            self.request.sendall("Hello: " + session.getName())
            return
        if cmd == 'exit':
            print "Closing server"
            server.shutdown()
            server.server_close()
            return
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "localhost", 16523

    # Creating users:
    print '--------------'
    print 'Creating users'
    print '--------------'
    users = create_users()

    print '-------------'
    print 'Testing users'
    print '-------------'
    test_users(users)

    print '----------------'
    print 'Seting up server'
    print '----------------'

    sessions = []
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), AuthenticateHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
