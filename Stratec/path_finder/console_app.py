import sys

from domain import Playground
from extra_tools import print_pretty_table

#
# Runs as python console_app.py filepath
# Example filepath: data\Step_One.csv
#

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('Please give as argument a filepath to the csv file.')

    filepath = sys.argv[1]

    try:
        playground = Playground(filepath)
        playground.find_paths()
        playground.save_to_csv('result.csv')

        print('Finished routing')
        print_pretty_table(playground.board)
    except OSError:
        print(f'File given by {filepath} could not be loaded.')

