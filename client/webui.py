import eel
import threading
from client.audio.communication import Communication


def startUI():
    """ NEW HTML BASED UI """
    communication = Communication()
    threading.Thread(target=communication.connect, args=("Tim", "135.125.207.61", 4747)).start()
    # communication.connect("Tim", "135.125.207.61", 4747)

    # where is the html located?
    eel.init('webui')
    eel.start('server_view/server_view.html', block=False)

    ################ BEGIN UI ################

    # DEFINE BUTTON FUNCTIONS LIKE THIS: (what happens when a button is pressed)
    @eel.expose                             # bridge between javascript and python
    def connect_button_pressed():
        if not communication.connected:
            threading.Thread(target=communication.connect, args=("Tim!", "135.125.207.61", 4848)).start()

    @eel.expose
    def enter_room(room_name):
        eel.update_room_selection(room_name)
        # communication.send_message("ROOMSWITCH_"+communication.USERNAME+"_"+str(room_name)+"_END")

    @eel.expose
    def update_users():

        # get users online
        users_online = communication.usernames_rooms

        # what user is in what room
        users_room1_test = []
        users_room2_test = []
        users_room3_test = []
        users_connect_room = [k for k, v in users_online.items() if
                              str(v) == "connectROOM"]  # convert user dict to acutal ip list
        users_connect_room.append("AlwaysOnlineTestUser")
        users_room1 = [k for k, v in users_online.items() if str(v) == "room1"]  # convert user dict to acutal ip list
        for user in users_room1:
            user.replace("", "User")
            users_room1_test.append(user)
        users_room2 = [k for k, v in users_online.items() if str(v) == "room2"]  # convert user dict to acutal ip list
        for user in users_room2:
            user.replace("", "User")
            users_room2_test.append(user)

        users_room3 = [k for k, v in users_online.items() if str(v) == "room3"]  # convert user dict to acutal ip list
        for user in users_room3:
            user.replace("", "User")
            users_room3_test.append(user)

        print(users_connect_room, users_room1_test, users_room2_test, users_room3_test)
        eel.update_users_view(str(users_connect_room), users_room1_test, users_room2_test, users_room3_test)

        # todo: call javascript function to dynamically display users

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
        try:
            pass
            #update_users()
        except:
            pass
        eel.sleep(100)