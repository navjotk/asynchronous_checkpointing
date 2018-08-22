import sys
import os
import itertools
import json
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_args(entry):
    assert(entry[1].startswith("{"))
    return json.loads(entry[1])
    
def depth(entry):
    args = get_args(entry)
    depth = args['depth']
    return depth

def timings(entry):
    times = None
    for l in entry:
        try:
            if l.startswith("[["):
                times = json.loads(l)
                break
        except json.decoder.JSONDecodeError:
            pass
    return times

def fwtime(entry):
    times = timings(entry)
    if times is not None:
        times = min(times[0])
    return times

def revtime(entry):
    times = timings(entry)
    if times is not None:
        times = min(times[1])
    return times

def mem(entry):
    line = list(filter(lambda x:'maximum resident set size' in x, entry))[0]
    d = list(filter(lambda x: len(x)>0, line.split(" ")))
    return int(d[0])

def filternones(l):
    r = []
    for sl in l:
        if not any(x is None for x in sl):
          r.append(sl)
    return r

def plottimings(depths_cp, fwtimes_cp, revtimes_cp, depths_nocp, fwtimes_nocp, revtimes_nocp):
    ttimes_cp = [x+y for x, y in zip(fwtimes_cp, revtimes_cp)]
    ttimes_nocp = [x+y for x, y in zip(fwtimes_nocp, revtimes_nocp)]
    fig, ax = plt.subplots()
    ax.plot(depths_cp, ttimes_cp, label="Total time (Checkpointed)")
    ax.plot(depths_cp, fwtimes_cp, label="Time for Forward (Checkpointed)")
    ax.plot(depths_cp, revtimes_cp, label="Time for backward (Checkpointed)")
    ax.plot(depths_nocp, ttimes_nocp, label="Total time (Not Checkpointed)")
    ax.plot(depths_nocp, fwtimes_nocp, label="Time for Forward (Not Checkpointed)")
    ax.plot(depths_nocp, revtimes_nocp, label="Time for backward (Not Checkpointed)")
    ax.set(xlabel='layers (n)', ylabel='execution time (ms)',
    title='Execution times by model size')
    ax.grid()
    ax.legend()
    fig.savefig("timings.pdf")

def plotmemory(depths_cp, mems_cp, depths_nocp, mems_nocp):
    mems_cp = [x/2**20 for x in mems_cp]
    mems_nocp = [x/2**20 for x in mems_nocp]
    fig, ax = plt.subplots()
    ax.plot(depths_cp, mems_cp, label="Checkpointed")
    ax.plot(depths_nocp, mems_nocp, label="Not Checkpointed")
    ax.set(xlabel="layers", ylabel='Memory (mb)',
    title='Memory consumption by model size')
    ax.set_ylim(ymin=0)
    ax.grid()
    ax.legend()
    fig.savefig("memory.pdf")

def extract(data):
    depths = [depth(x) for x in data]
    mems = [mem(x) for x in data]
    fwtimes = [fwtime(x) for x in data]
    revtimes = [revtime(x) for x in data]
    depths, fwtimes, revtimes, mems = zip(*filternones(zip(depths, fwtimes, revtimes, mems)))
    return depths, fwtimes, revtimes, mems
    
def splitoutput(lines):
    spl = []
    for x, y in itertools.groupby(lines, lambda z: z.startswith("***Start***")):
        if x: spl.append([])
        spl[-1].extend(y)
    return spl


files = [sys.argv[1], sys.argv[2]]


raw_data = []
for file in files:
    assert(os.path.isfile(file))
    with open(file) as f:
        lines = f.readlines()
    raw_data.append(lines)
split_data = [splitoutput(x) for x in raw_data]

cpdata = None
nocpdata = None

for d in split_data:
    args = get_args(d[0])
    if args['checkpoint']:
        cpdata = d
    else:
        nocpdata = d

assert(cpdata is not None)
assert(nocpdata is not None)

depths_cp, fwtimes_cp, revtimes_cp, mems_cp = extract(cpdata)
depths_nocp, fwtimes_nocp, revtimes_nocp, mems_nocp = extract(nocpdata)

plottimings(depths_cp, fwtimes_cp, revtimes_cp, depths_nocp, fwtimes_nocp, revtimes_nocp)
plotmemory(depths_cp, mems_cp, depths_nocp, mems_nocp)
