from src.stream.depth_stream import stream
from src.application.config.config import configuration
import argparse

# region Parse Arguments

parser = argparse.ArgumentParser(description="Object detection on IntelSenseD451i for MEVA Project")
parser.add_argument('--resolution', metavar='', nargs=2, default=(768, 540),
                    help='stream resolution', type=int)
parser.add_argument('--interrupt', metavar='', default=15,
                    help='interrupt to lower stream rate for predictions', type=int)
parser.add_argument('--file', metavar='', default='results.csv',
                    help='file to store results', type=str)

args = parser.parse_args()

# endregion

# region Run

model, pipeline = configuration()
stream(
    model=model,
    pipeline=pipeline,
    resolution=tuple(args.resolution),
    counter_interrupt=args.interrupt,
    file=args.file,
    is_web=False,
)

# endregion
