from kindle.parser import parse
import csv
path_to_clippings = "My Clippings.txt"
clippings = parse(path_to_clippings)
# print(clippings)
f = open('out.csv', 'w')
fieldnames = ['Highlight', 'Title', 'Author', 'Location', 'Date']
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()
for clipping in clippings:
    writer.writerow(clipping)
f.close()