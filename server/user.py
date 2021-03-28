
class User:
    """ Creates new user object which stores some information about the connected client """

    def __init__(self, SOCKET, IP, USERNAME):
        self.SOCKET = SOCKET
        self.IP = IP
        self.USERNAME = USERNAME
        self.room = "connectROOM"

    def send_string(self, string_data):
        self.SOCKET.send(str(string_data).encode())

    def send(self, data):
        """ Streambyte data """
        self.SOCKET.send(data)

    def kick(self):
        self.SOCKET.close()

    def get_room(self):
        return self.room

    def enter_room(self, room_name):
        self.room = room_name

    def get_username(self):
        return self.USERNAME

    def get_socket(self):
        return self.SOCKET

    def get_IP(self):
        return self.IP
