from audio.communication import Communication
from ui.main_page import MainPage


def main():
    """ Starts communication with server
        Start UI    """
    communication = Communication()

    try:
        """ Connect and do its thing """
        MainPage()
        #communication.connect("Atom", "127.0.0.1", 4848)

    finally:
        """ Important for cleanup communication before leaving
            Double safety, server should handle disconnects cleanly already """
        communication.disconnect()

if __name__ == "__main__":
    main()

