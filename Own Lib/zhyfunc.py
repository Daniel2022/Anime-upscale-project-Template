from functools import partial
from vsutil import *
import vapoursynth as vs
import mvsfunc as mvf
import fvsfunc as fvf
from kagefunc import kirsch
import typing
from typing import Any, Callable, Dict, Iterable, List, Optional
from typing import Sequence, Tuple, TypeVar, Union

core = vs.core

def retinex_edgemask(src: vs.VideoNode, sigma=1, opencl=True) -> vs.VideoNode:
    """
    Use retinex to greatly improve the accuracy of the edge detection in dark scenes.
    sigma is the sigma of tcanny

    Port from kagefunc, add OpenCL
    """
    luma = get_y(src)
    max_value = 1 if src.format.sample_type == vs.FLOAT else (1 << get_depth(src)) - 1
    ret = core.retinex.MSRCP(luma, sigma=[50, 200, 350], upper_thr=0.005)
    if opencl:
        tcanny = ret.tcanny.TCannyCL(mode=1, sigma=sigma).std.Minimum(coordinates=[1, 0, 1, 0, 0, 1, 0, 1])
    else:
        tcanny = ret.tcanny.TCanny(mode=1, sigma=sigma).std.Minimum(coordinates=[1, 0, 1, 0, 0, 1, 0, 1])
    return core.std.Expr([kirsch(luma), tcanny], f'x y + {max_value} min')
