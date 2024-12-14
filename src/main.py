#!/usr/bin/env python3

from weather import *

def main() -> None:
    '''
    Main entry point - Start QApplication, Call Controller Class
    :return: None
    '''
    application = QApplication([])
    Controller()
    application.exec_()

if __name__ == "__main__":
    main()