
import threading
import pyaudio

class Speaker:
    """ Handles received data, which can be audio or messages """

    def __init__(self, COMMUNICATION, CHUNK_SIZE: int):
        self.COMMUNICATION = COMMUNICATION
        self.CHUNK_SIZE = CHUNK_SIZE

        # audio settings
        self.deaf = False
        self.AUDIO_FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000

        # starting speaker and speaker list
        self.pyaudio = pyaudio.PyAudio()
        #print("[AVAILABLE SPEAKERS]")
        #self.devices_info = self.pyaudio.get_host_api_info_by_index(0)
        #self.amount_speakers = self.devices_info.get('deviceCount')
        #for i in range(0, self.amount_speakers):
            #if self.pyaudio.get_device_info_by_host_api_device_index(0,i).is_format_supported(48000,i,output_format=True) > 0:  # if its a MICROPHONE
        #    print("SPEAKER ID: ", id, self.pyaudio.get_device_info_by_host_api_device_index(0,i).get('name'))
        #print("################")
        self.playing_stream = self.pyaudio.open(format=self.AUDIO_FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)

        # start playing thread
        self.running = True
        threading.Thread(target=self.start_playing).start()


    def start_playing(self):
        """ Receives data which can be audio or messages. If its messages, call communication to interpret it
            If its audio, play it if not deaf """

        print("[SPEAKER] Started receiving data ...")
        while self.running:
            try:
                data = self.COMMUNICATION.receive_data()
                string_data = ""
                try:
                    string_data = data.decode()
                except:
                    pass

                if "DISCONNECT" in string_data or "SWITCHROOM" in string_data or "USERJOIN" in string_data:     # there might be a problem here: if a user sends messages audio may be skipped playing
                    self.COMMUNICATION.handle_message(string_data)                                              # solution maybe: cut out message out of string_data, encode and play data (instead of else)
                else:
                    try:
                        self.playing_stream.write(data)
                    except:
                        pass
            except Exception as e:
                self.running = False
                print("[SPEAKER ERROR] " + str(e))
