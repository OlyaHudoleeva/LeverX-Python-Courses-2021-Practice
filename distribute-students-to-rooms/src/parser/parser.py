import argparse
from ..config import SUPPORTED_OUTPUT_FORMAT

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('students', nargs='?')
    parser.add_argument('rooms', nargs='?')
    parser.add_argument('format', nargs='?', choices=SUPPORTED_OUTPUT_FORMAT)

    return parser
