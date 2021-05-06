import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('students', nargs='?')
    parser.add_argument('rooms', nargs='?')
    parser.add_argument('format', nargs='?')

    return parser
