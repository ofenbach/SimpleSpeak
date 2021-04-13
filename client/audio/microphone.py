import threading

class Microphone:

    def __init__(self, COMMUNICATION, PYAUDIO, CHUNK_SIZE: int, AUDIO_FORMAT, CHANNELS, RATE):
        """ Initialize default values for recording """

        # audio settings
        self.COMMUNICATION = COMMUNICATION
        self.pyaudio = PYAUDIO
        self.CHUNK_SIZE = CHUNK_SIZE            # good value: 2048
        self.muted = False
        self.AUDIO_FORMAT = AUDIO_FORMAT     # alternative: pyInt32
        self.CHANNELS = CHANNELS
        self.RATE = RATE

        # Starting microphone and microphone list
        self.display_mics()
        self.recording_stream = self.pyaudio.open(format=self.AUDIO_FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK_SIZE,  input_device_index=1)

        # start recording thread
        threading.Thread(target=self.start_recording).start()


    def start_recording(self):
        """ Starts recording the microphone and sending the data to the Server """

        print("[MICROPHONE] Started sending data ...")
        self.running = True
        while self.running:
            try:
                if not self.muted:
                    data = self.recording_stream.read(self.CHUNK_SIZE, exception_on_overflow = False)
                    self.COMMUNICATION.send_data(data)
            except Exception as e:
                print("[MICROPHONE ERROR] " + str(e))
                self.COMMUNICATION.disconnect()
                self.running = False
                break

    def switch_mute(self):
        """ Simple mute switch, probably gets called by UI
            Problem: How will UI access this? Pass microphone object as parameter to UI, like did with communication passed to microphone? """
        self.mute = not self.mute


    def display_mics(self):
        print()
        print("[AVAILABLE MICS]")
        devices_info = self.pyaudio.get_host_api_info_by_index(0)
        amount_microphones = devices_info.get('deviceCount')
        for i in range(0, amount_microphones):
            if self.pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
                print("MIC ID: ", str(id), self.pyaudio.get_device_info_by_host_api_device_index(0, i).get('name'))
        print("################")
