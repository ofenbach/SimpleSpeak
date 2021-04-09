import socket
import ast
import pyaudio

from audio.microphone import Microphone
from audio.speaker import Speaker


class Communication:
    """ Communication between Server and Client
        Data:   AUDIO (PyAudio Stream)
                MESSAGE (Strings starting with MESSAGE_ ending with _END)
                        Messages:   USERJOIN_username_END
                                    DISCONNECT_username_END
                                    ROOMSWITCH_username_room_END """


    def __init__(self):
        """ Sets default values
            @value connected:       info if the client is connected
            @value socket:          communication socket between server/client
            @value CHUNK_SIZE:      amount of bytes per transmission between server/client
            @value usernames_rooms: dictionairy that displays which user is in what room
                                    Example:    {"JoeRogan": "Room1"} """
        self.connected = False
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CHUNK_SIZE = 512
        self.usernames_rooms = {}
        self.pyaudio = pyaudio.PyAudio()


    def connect(self, USERNAME: str, IP: str, PORT: int):
        """ Connects to the give IP and PORT
            @param USERNAME:    Username to connect to server
            @param IP:          IP of the Server to connect to
            @param PORT:        PORT the server docks to """
        self.USERNAME = USERNAME
        self.SERVER = (IP,PORT)

        # connecting ...
        try:
            self.SOCKET.connect(self.SERVER)
            self.SOCKET.send(self.USERNAME.encode())                            # send username
            self.usernames_rooms = self.SOCKET.recv(self.CHUNK_SIZE).decode('utf-8', 'ignore')   # receives usernames
            print(self.usernames_rooms)
            self.usernames_rooms = ast.literal_eval(self.usernames_rooms)       # convert string representation of dict to dict
            self.connected = True
            print("[CONNECTED] " + str(self.SERVER))
            print("[USERS/ROOMS] ", self.usernames_rooms)
        except Exception as e:
            self.connected = False
            print("[CONNECTION ERROR] " + str(e))
            return self.connected

        # starting devices (start their own threads)
        self.AUDIO_FORMAT = pyaudio.paInt16  # alternative: pyInt32
        self.CHANNELS = 1
        self.RATE = 20000
        self.microphone = Microphone(self, self.pyaudio, self.CHUNK_SIZE, self.AUDIO_FORMAT, self.CHANNELS, self.RATE)
        self.speaker = Speaker(self, self.pyaudio, self.CHUNK_SIZE, self.AUDIO_FORMAT, self.CHANNELS, self.RATE)


    def disconnect(self):
        """ Disconnects from the server without leaving traces """
        self.connected = False
        try:
            self.SOCKET.send(("DISCONNECT_" + str(self.USERNAME) + "_END").encode())
            self.SOCKET.close()
        except Exception as e:
            self.SOCKET.close()
            print("[DISCONNECTION ERROR] " + str(e))


    def send_data(self, data):
        """ Sends data to server
            @param data:    bytestring object to send """
        try:
            self.SOCKET.sendall(data)
        except Exception as e:
            print("[DATASEND ERROR] " + str(e))
            self.disconnect()


    def receive_data(self):
        """ Call to start receiving data from server """
        try:
            return self.SOCKET.recv(self.CHUNK_SIZE)
        except Exception as e:
            print("[DATARECV ERROR] " + str(e))
            self.disconnect()


    def send_message(self, string_data):
        """ Probably gets called by UI """
        if "ROOMSWITCH" in string_data:
            print("[MESSAGE] ROOMSWITCH")
            message_end = string_data.find("_END")
            message_content = string_data[len("ROOMSWITCH_"):message_end]
            username = message_content.split("_")[0]
            room = message_content.split("_")[1]
            self.usernames_rooms[username] = room
            self.SOCKET.send(string_data.encode())


    def handle_message(self, string_data):
        """ Interprets the messages inside the string_data """
        if "DISCONNECT" in string_data:
            print("disconecct")
        if "ROOMSWITCH" in string_data:
            print("Roomswtich")
        if "USERJOIN" in string_data:
            print("Userjoin")
