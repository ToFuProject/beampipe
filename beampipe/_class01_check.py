import numpy as np
import datastock as ds


#############################################
#############################################
#       DEFAULT VALUES
#############################################


#############################################
#############################################
#       main
#############################################


def main(
    coll=None,
    key=None,
    key_csys=None,
    # circle
    center=None,
    radius=None,
    # polygon
    outline_x0=None,
    outline_x1=None,
    # unused
    **kwdargs,
):

    # ---------------
    # check inputs
    # ---------------

    kwd = _check(**locals())

    # ---------------
    # dref, ddata
    # ---------------

    dref = None
    ddata = None

    # ---------------
    # dobj
    # ---------------

    wout2d = coll._which_outline2d
    dobj = {wout2d: {kwd['key']: kwd}}

    return dref, ddata, dobj


#############################################
#############################################
#       check
#############################################


def _check(kwd):

    # ----------
    # key
    # ----------

    return kwd
