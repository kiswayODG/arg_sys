import sys

from utilities import parse_arguments
from controller import handle_parameters



def main():
    
    args = parse_arguments()
    
    handle_parameters(args)

if __name__ == "__main__":
    main()