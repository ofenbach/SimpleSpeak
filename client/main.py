import webui.webui


def main():
    """ Start UI """

    try:
        """ Start penis """
        webui.webui.startUI()
    finally:
        """ Important for cleanup communication before leaving
            Double safety, server should handle disconnects cleanly already """
        pass


if __name__ == "__main__":
    main()

