import eel
import threading
from client.audio.communication import Communication


def startUI():
    """ NEW HTML BASED UI """

    # where is the html located?
    eel.init('new_web_ui/buildings/dashboard')
    eel.start('index.html', block=False)
    communication = Communication()

    ################ BEGIN UI ################

    # DEFINE BUTTON FUNCTIONS LIKE THIS: (what happens when a button is pressed)
    @eel.expose                             # bridge between javascript and python
    def connect_button_pressed():
        if not communication.connected:
            threading.Thread(target=communication.connect, args=("ATOM", "135.125.207.61", 4848)).start()

    @eel.expose
    def enter_room(room_name):
        communication.send_message("ROOMSWITCH_"+communication.USERNAME+"_"+str(room_name)+"_END")

    @eel.expose
    def mute_button_pressed():
        communication.microphone.muted = not communication.microphone.muted
        print("MUTE BUTTON" + str(communication.microphone.muted))

    @eel.expose
    def deaf_button_pressed():
        communication.speaker.deaf = not communication.speaker.deaf
        print("DEAF BUTTON" + str(communication.speaker.deaf))

    ################  END UI  ################

    # keep refreshing UI
    while True:
        eel.sleep(10)