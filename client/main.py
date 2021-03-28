from audio.communication import Communication
from ui.main_page import MainPage


def main():
    """ Start UI """

    try:
        """ Start UI """
        MainPage()

    finally:
        """ Important for cleanup communication before leaving
            Double safety, server should handle disconnects cleanly already """
        pass


if __name__ == "__main__":
    main()

