from audio.communication import Communication


def main():
    """ Starts communication with server
        Start UI    """
    communication = Communication()
    try:
        """ Connect and do its thing """
        communication.connect("PyCharm", "127.0.0.1", 4848)
    finally:
        """ Important for cleanup communication before leaving
            Double safety, server should handle disconnects cleanly already """
        communication.disconnect()

if __name__ == "__main__":
    main()
