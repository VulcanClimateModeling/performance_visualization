"""Adding semantic marking to external profiler.

Usage: python external_profiler.py <PYTHON SCRIPT>.py <ARGS>

Works with nvtx (via cupy) for now.
"""

import sys
import json
from argparse import ArgumentParser

from tools import nvtx_markings, stencil_reproducer


try:
    import cupy as cp
except ModuleNotFoundError:
    cp = None


def parse_args():
    usage = "usage: python %(prog)s <--nvtx> <--stencil=STENCIL_NAME> <--call_number=N> <CMD TO PROFILE>"  # noqa: E501
    parser = ArgumentParser(usage=usage)
    parser.add_argument(
        "--config",
        type=str,
        action="store",
        help="mandatory configuration file",
    )
    parser.add_argument(
        "--nvtx",
        action="store_true",
        help="enable NVTX marking",
    )
    parser.add_argument(
        "--stencil",
        type=str,
        action="store",
        help="create a small reproducer for the stencil",
    )
    parser.add_argument(
        "--call_number",
        type=int,
        default=0,
        help="which stencil call to reproduce. If 0 or less, collects all calls",  # noqa: E501
    )
    return parser.parse_known_args()


def profile_hook(frame, event, args):
    if cmd_line_args.nvtx and nvtx_markings.mark is not None:
        nvtx_markings.mark(frame, event, args)
    if (
        cmd_line_args.stencil
        and stencil_reproducer.field_serialization is not None  # noqa: E501
    ):
        _ = stencil_reproducer.field_serialization(frame, event, args)


cmd_line_args = None
CONFIG = None
if __name__ == "__main__":
    # Parse arguments and check validity
    cmd_line_args, unknown = parse_args()
    print(f"{cmd_line_args}")
    print(f"{unknown}")
    if cmd_line_args.nvtx and cp is None:
        if cmd_line_args.stencil is not None:
            print("WARNING: cupy isn't available, NVTX marking deactivated.")
        else:
            raise RuntimeError(
                "FAILED: cupy isn't available, NVTX marking can't be run."
            )
        cmd_line_args.nvtx = False
    # Read config file
    if cmd_line_args.config is None:
        raise RuntimeError("FAILED: No configuration file.")
    CONFIG = json.load(cmd_line_args.config)
    # Operations
    if cmd_line_args.stencil is not None:
        stencil_reproducer.collect_stencil_candidate(
            cmd_line_args.stencil, cmd_line_args.call_number
        )
    if cmd_line_args.nvtx or cmd_line_args.stencil:
        sys.setprofile(profile_hook)
    # Fowarding the execution of the APP & ARGS
    filename = unknown[0]
    sys.argv = unknown[0:]
    exec(compile(open(filename, "rb").read(), filename, "exec"))
