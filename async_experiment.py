from dummyoperator import DummyCheckpoint
from ast import literal_eval as make_tuple
from pyrevolve import Checkpointer
import numpy as np
import argparse
import json
from util import Timer, measure
from devitooperators import DevitoOperator


parser = argparse.ArgumentParser(description='Run an asynchronous checkpointing timing experiment')
parser.add_argument('size', type=int, nargs='?', default="100", help='size of domain')

parser.add_argument('interval',  type=int, nargs='?', default=7, 
                   help='checkpointing interval')
parser.add_argument('num_steps',  type=int, nargs='?', default=100, 
                   help='number of checkpoints for reverse')
parser.add_argument('order', type=int, nargs='?', default=2, help="spatial order for operator")
cp_parser = parser.add_mutually_exclusive_group(required=False)
cp_parser.add_argument('--checkpoint', dest='checkpoint', action='store_true')
cp_parser.add_argument('--no-checkpoint', dest='checkpoint', action='store_false')
parser.set_defaults(checkpoint=True)
wf_parser = parser.add_mutually_exclusive_group(required=False)
wf_parser.add_argument('--write-files', dest='write_files', action='store_true')
wf_parser.add_argument('--no-write-files', dest='write_files', action='store_false')
parser.set_defaults(write_files=True)
parser.add_argument('--file-prefix', type=str, default="./tmp", help="Prefix for the directory to use to store temp files")

args = parser.parse_args()
print("***Start***")
print(json.dumps(vars(args)))
size = args.size
order = args.order
interval = args.interval
num_steps = args.num_steps
checkpoint = args.checkpoint
write_files = args.write_files
file_prefix = args.file_prefix

sym = np.zeros((size,))
fwd_op = DevitoOperator((70, 70), order)

wrp = Checkpointer(fwd_op, None, 10000, num_steps, DummyCheckpoint({'sym': sym}), DummyCheckpoint({'sym': sym}), interval=interval, nrevcp=4, file_prefix=file_prefix, write_files=write_files)

args = []
kwargs={}
if checkpoint:
    testing_callable = wrp.apply_forward
    args = [sym]
else:
    testing_callable = fwd_op.apply
    kwargs = {'t_start': 0, 't_end': num_steps}

timings = measure(testing_callable, *args, **kwargs)
print(timings)
print(min(timings))
