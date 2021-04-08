import threading
import pyaudio


class Speaker:
    """ Handles received data, which can be audio or messages """

    def __init__(self, COMMUNICATION, PYAUDIO, CHUNK_SIZE: int, AUDIO_FORMAT, CHANNELS, RATE):
        self.COMMUNICATION = COMMUNICATION
        self.pyaudio = PYAUDIO
        self.CHUNK_SIZE = CHUNK_SIZE

        # audio settings TODO: channels = 2? Caused some bugs
        self.deaf = False
        self.AUDIO_FORMAT = AUDIO_FORMAT
        self.CHANNELS = 2
        self.RATE = RATE

        # starting speaker and speaker list
        self.playing_stream = self.pyaudio.open(format=self.AUDIO_FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                                output=True, frames_per_buffer=self.CHUNK_SIZE)

        # start playing thread
        threading.Thread(target=self.start_playing).start()


    def start_playing(self):
        """ Receives data which can be audio or messages. If its messages, call communication to interpret it
            If its audio, play it if not deaf """

        print("[SPEAKER] Started receiving data ...")
        self.running = True
        while self.running:
            try:
                if not self.deaf:
                    data = self.COMMUNICATION.receive_data()
                    string_data = ""

                    try:
                        string_data = data.decode('utf-8', 'ignore')
                    except Exception as e:
                        pass    # there are some errors here, fix later

                if "DISCONNECT" in string_data or "SWITCHROOM" in string_data or "USERJOIN" in string_data:  # there might be a problem here: if a user sends messages audio may be skipped playing
                    self.COMMUNICATION.handle_message(string_data)  # solution maybe: cut out message out of string_data, encode and play data (instead of else)
                else:
                    try:
                        self.playing_stream.write(data)
                    except Exception as e:
                        print("[PLAYING ERROR] " + str(e))
                        self.COMMUNICATION.disconnect()
                        self.running = False

            except Exception as e:
                print("[SPEAKER ERROR] " + str(e))
                self.COMMUNICATION.disconnect()
                self.running = False
                break
