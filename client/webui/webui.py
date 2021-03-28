import eel

def startUI():
    """ NEW HTML BASED UI """

    # where is the html located?
    eel.init('')
    eel.start('index.html', block=False)

    ################ BEGIN UI ################

    # DEFINE BUTTON FUNCTIONS LIKE THIS: (what happens when a button is pressed)
    @eel.expose                             # bridge between javascript and python
    def connect_button_pressed():
        print("Connect button pressed!")    # just prints out on console

    ################  END UI  ################

    # keep refreshing UI
    while True:
        eel.sleep(10)

startUI()