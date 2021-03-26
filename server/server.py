import socket
import threading


class Server:
    """ Server saves which user (socket) has what username
        usernames are associated with rooms
        So to get from a socket to a room, you need to access users->usernames->rooms """


    def __init__(self):
        """ Set default server values and wait for connections """
        self.users_usernames = {}       # sockets:usernames
        self.usernames_rooms = {}       # only one default room: connectROOM
        self.CHUNK_SIZE = 2048
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.SOCKET.bind(("127.0.0.1", 4848))
        self.SOCKET.listen()

        print("[STARTED] Listening ...")
        while True:
            # waiting for connection ...

            user, addr = self.SOCKET.accept()
            username = user.recv(self.CHUNK_SIZE).decode('utf-8','ignore')
            if username in self.users_usernames.values():    # username already taken?
                user.close()
                print("USERNAME " + str(username) + " ALREADY EXISTS, KICKED!")
            else:
                # send user join to everyone else
                for server_user in self.users_usernames.keys():
                    server_user.send(("USERJOIN_" + str(username) + "_END").encode('utf-8','ignore'))

                # update own userbase
                self.users_usernames[user] = username
                self.usernames_rooms[username] = "connectROOM"
                user.send(str(self.usernames_rooms).encode())
                print("[CONNECTED] ", username)
                print("[USERS ONLINE] ", self.users_usernames)

                # start threads
                threading.Thread(target=self.receive_data, args=(user,)).start()


    def receive_data(self, user):
        """ Receives data of user in parameter.
            Gets started as a thread """

        while True:
            try:
                data = user.recv(self.CHUNK_SIZE)
                string_data = data.decode('utf-8', 'ignore')

                if "DISCONNECT" in string_data or "ROOMSWITCH" in string_data:
                    self.handle_message(user, string_data)
                else:
                    self.handle_audio(user, data)

            except:
                self.disconnect_user(user)
                break

    def handle_audio(self, sender, data):
        """ Sends audio only to users who are in the same room """
        sender_username = self.users_usernames[sender]
        sender_room = self.usernames_rooms[sender_username]
        for user in self.users_usernames:
            try:
                if user != self.SOCKET and user != sender and self.usernames_rooms[self.users_usernames[user]] == sender_room:   # not server, not himself and same room
                    user.send(data)

            except Exception as e:
                print("[SENDING ERROR] " + str(e))


    def handle_message(self, sender, string_data):
        """ Handle messages received """
        print("Message received! Todo!")
        if "DISCONNECT" in string_data:
            disconnect_user(sender)
        if "ROOMSWITCH" in string_data:
            message_begin = string_data.find("ROOMSWITCH_")+len("ROOMSWITCH_")
            message_end = string_data.find("_END")
            message_content = string_data[message_begin:message_end]
            username = message_content.split("_")[0]
            room = message_content.split("_")[1]
            self.usernames_rooms[username] = room
            # todo send to everyone else this message


    def disconnect_user(self, user):
        """ Kick specific user out of server """

        username = self.users_usernames[user]
        user.close()
        del self.users_usernames[user]
        del self.usernames_rooms[username]
        print("[USER DISCONNECT] ", username)
        for server_user in self.users_usernames.keys():
            server_user.send(("DISCONNECT_" + str(username) + "_END").encode('utf-8','ignore'))
        print("[USERS ONLINE]", self.users_usernames)


Server()
