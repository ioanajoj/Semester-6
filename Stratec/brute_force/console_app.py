from brute_force.domain import Playground
from brute_force.printing_tools import print_pretty_table

filepath = '..\\2020_Internship_Challenge_Software\\Step_One-2.csv'

playground = Playground(filepath)
playground.find_paths()
playground.save_to_csv('output')

print('Finished routing')

print_pretty_table(playground.board)
