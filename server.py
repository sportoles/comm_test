#!/usr/bin/python

import SocketServer

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

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 16522

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

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
