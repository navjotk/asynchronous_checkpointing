import argparse
import matplotlib.pyplot as plt
from util import parse_data_file


parser= argparse.ArgumentParser(prog='make_graph.py', usage='python %(prog)s -f Filename Series_name -f Filename2 Series_name2 ')
parser.add_argument ('-f', '--file', nargs=2, action='append', help="Data file to plot from", required=True)
parser.add_argument('-t', '--title', nargs=1, type=str, help="Chart Title", required=True)
parser.add_argument('-x', '--x', type=str, help="X dimension", required=True)
parser.add_argument ('-b', '--baseline', nargs=1, action='append', help="Data file to read baseline", required=True)
parser.add_argument('-o', '--output-file', help="Name of the output chart", required=True)

args = parser.parse_args()
files = args.file
title = args.title
x_label = args.x
baseline = args.baseline[0]
output_file = args.output_file

assert(len(baseline) == 1 or len(baseline) == len(files))

if len(baseline) == 1:
    baseline = baseline * len(files)

for i, (filename, series_name) in enumerate(files):
    base_xs, base_ys = parse_data_file(baseline[i], x_label)
    xs, ys = parse_data_file(filename, x_label)
    assert(base_xs == xs)
    change_ys = [(y-base_y)/base_y for y, base_y in zip(ys, base_ys)]
    plt.plot(xs, change_ys, label=series_name)
plt.xlabel('Interval')
plt.ylabel('Execution time (ms)')
plt.legend(loc='lower right')
plt.savefig(output_file, bbox_inches='tight')
    
    
