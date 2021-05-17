import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('students', nargs='?')
    parser.add_argument('rooms', nargs='?')
    parser.add_argument('format', nargs='?', choices=['xml', 'json'])

    return parser
