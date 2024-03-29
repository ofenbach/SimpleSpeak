import threading
import pyaudio


class Microphone:

    def __init__(self, COMMUNICATION, CHUNK_SIZE: int):
        """ Initialize default values for recording
            TODO: Microphone selection """

        # audio settings
        self.COMMUNICATION = COMMUNICATION
        self.CHUNK_SIZE = CHUNK_SIZE        # good value: 2048
        self.muted = False
        self.AUDIO_FORMAT = pyaudio.paInt16 # alternative: pyInt32
        self.CHANNELS = 1                   # TODO: look into mono / stereo bugs
        self.RATE = 48000

        # Starting microphone and microphone list
        self.pyaudio = pyaudio.PyAudio()
        print("[AVAILABLE MICS]")
        self.devices_info = self.pyaudio.get_host_api_info_by_index(0)
        self.amount_microphones = self.devices_info.get('deviceCount')
        for i in range(0, self.amount_microphones):
            if self.pyaudio.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels') > 0:  # if its a MICROPHONE
                print("MIC ID: ", id, self.pyaudio.get_device_info_by_host_api_device_index(0,i).get('name'))
        print("################")
        self.recording_stream = self.pyaudio.open(format=self.AUDIO_FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                                    input=True, frames_per_buffer=self.CHUNK_SIZE)

        # start recording thread
        self.running = True
        threading.Thread(target=self.start_recording).start()


    def start_recording(self):
        """ Starts recording the microphone and sending the data to the Server """

        print("[MICROPHONE] Started sending data ...")
        while self.running:
            try:
                data = self.recording_stream.read(self.CHUNK_SIZE)      # OPTIONAL: exception_on_overflow=False
                if not self.muted:
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
