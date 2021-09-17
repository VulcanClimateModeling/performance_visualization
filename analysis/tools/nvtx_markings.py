try:
    import cupy as cp
except ModuleNotFoundError:
    cp = None

from analysis.config import get_analysis_config

def get_class_from_frame(frame):
    try:
        class_name = frame.f_locals["self"].__class__.__name__
    except KeyError:
        class_name = "Err: not an object"
    return class_name


def get_object_wrapper_name(frame, event, args) -> str:
    return get_class_from_frame(frame)


def get_stencil_name(frame, event, args) -> str:
    """Get the name of the stencil from within a
    call to FrozenStencil.__call__"""
    name = getattr(
        frame.f_locals["self"].stencil_object,
        "__name__",
        repr(frame.f_locals["self"].stencil_object.options["name"]),
    )
    return f"{name}.__call__"


def get_name_from_frame(frame, event, args) -> str:
    """Static name from frame object"""
    return frame.f_code.co_name


""" Dictionary of functions to retrieve the name of a marker
following different logic.
"""
name_op = {
    "gt4py_stencil": get_stencil_name,
    "function": get_name_from_frame,
    "wrapper": get_object_wrapper_name,
}


def mark(frame, event, args):
    """Hooks at each function call & exit to record a Mark."""
    config = get_analysis_config()
    if event == "call":
        for fn_desc in config["nvtx_marks"]:
            key = fn_desc["key"]
            if frame.f_code.co_name == key["fn"] and (
                key["file"] is None or key["file"] in frame.f_code.co_filename
            ):
                if "name" in fn_desc:
                    name = fn_desc["name"]
                elif "name_op" in fn_desc:
                    name = name_op[fn_desc["name_op"]](frame, event, args)
                else:
                    raise RuntimeError("Unrecognized name operator")
                cp.cuda.nvtx.RangePush(name)
    elif event == "return":
        for fn_desc in config["nvtx_marks"]:
            key = fn_desc["key"]
            if frame.f_code.co_name == key["fn"] and (
                key["file"] is None or key["file"] in frame.f_code.co_filename
            ):
                cp.cuda.nvtx.RangePop()
