import threading
import socket

from user import User


class Server:
    """ Server saves users and sends audio to each one inside a room """


    def __init__(self):
        """ Set default server values and wait for connections """
        self.users = []
        self.CHUNK_SIZE = 2048
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.SOCKET.bind(("0.0.0.0", 4747))
        self.SOCKET.listen()

        while True:
            # waiting for connection ...
            print("[STARTED] Listening ...")

            # connection received
            user_socket, user_ip = self.SOCKET.accept()
            username = user_socket.recv(self.CHUNK_SIZE).decode('utf-8','ignore')
            new_user = User(user_socket, user_ip, username, self.CHUNK_SIZE)

            # start communication
            if not "bot" in username:
                self.users.append(new_user)
                usernames = {}
                for user in self.users:                 # send user connected users and new user to connected users
                    usernames[user.get_username()] = user.get_room()
                new_user.send_string(usernames)         # send users

                # update terminal info
                print("[CONNECTED] ", new_user.get_username())
                print("[USERS ONLINE]")
                for user in self.users:
                    if user != new_user:
                        user.send_string("USERJOIN_" + str(username) + "_END")
                    print(user.get_username())

                # start thread
                threading.Thread(target=self.receive_data, args=(new_user,)).start()

            else:
                print("[CONNECTION] BOT CONNECTED")
                if "musicbot" in username:              # which kind of bot?
                    threading.Thread(target=self.receive_music, args=(new_user,)).start()


    def receive_data(self, user):
        """ Receives data of user in parameter.
            Gets started as a thread """

        while True:
            try:
                data = user.receive()
                string_data = data.decode('utf-8', 'ignore')

                if "DISCONNECT" in string_data or "ROOMSWITCH" in string_data or "USERJOIN" in string_data:
                    self.handle_message(user, string_data)
                else:
                    self.handle_audio(user, data)

            except Exception as e:
                print("RECEIVE ERROR: ", e)
                self.disconnect_user(user)
                break

    def receive_music(self, user):
        """ Receives data of user in parameter.
            Gets started as a thread """
        print("Started playing music")
        while True:
            try:
                data = user.get_socket().recv(self.CHUNK_SIZE)
                self.handle_audio(user, data)
            except Exception as e:
                print("[MUSICBOT ERROR RECEIVING] ", e)
                break

    def handle_audio(self, sender, data):
        """ Sends audio only to users who are in the same room """

        for user in self.users:
            try:

                # I     Do not send audio to server (self)
                # II    Do not send to sender again (speaking client) (ERROR?!) and user.get_socket() != sender.get_socket()
                # III   Do only send to users in same room #and user.get_room() == sender.get_room()
                if user.get_socket() != self.SOCKET and user.get_socket() != sender.get_socket() and user.get_room() == sender.get_room():   # not server, not himself and same room
                    user.send(data)

            except Exception as e:
                print("[SENDING ERROR] " + str(e))
                user.kick()
                self.users.remove(user)
                break

    def handle_message(self, sender, string_data):
        """ Handle messages received """

        if "DISCONNECT" in string_data:
            print("[MESSAGE] DISCONNECT")
            sender.kick()
            self.users.remove(sender)
            for user in self.users:
                user.send_string("DISCONNECT_" + str(sender.get_username()) + "_END")
        if "ROOMSWITCH" in string_data:
            print("[MESSAGE] ROOMSWITCH")
            message_begin = string_data.find("ROOMSWITCH_")+len("ROOMSWITCH_")
            message_end = string_data.find("_END")
            message_content = string_data[message_begin:message_end]
            room = message_content.split("_")[1]
            sender.enter_room(room)
            print(self.users)
            for user in self.users:
                user.send_string("ROOMSWITCH_" + str(sender.get_username()) + "_" + str(room) + "_END")


    def disconnect_user(self, user):
        """ Kick specific user out of server """

        print("USER KICKED! ", user.get_username())
        user.kick()
        self.users.remove(user)
        for user in self.users:
            user.send_string("DISCONNECT_" + str(user.get_username()) + "_END")

        print("[USERS ONLINE]")
        for user_ in self.users:
            print(user_.get_username())


Server()
