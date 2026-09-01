import numpy as np
import datastock as ds


from . import _utils_csys


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
    # cent
    cent=None,
    # vect
    e0=None,
    e1=None,
    e2=None,
    # vecto options
    norm=None,
    direct=None,
    # ref csys
    kcsys0=None,
    # unused
    **kwdargs,
):

    # ---------------
    # check inputs
    # ---------------

    kwd = _check(**locals())

    # ---------------
    # dref
    # ---------------

    # ---------------
    # ddata
    # ---------------

    # ---------------
    # dobj
    # ---------------

    return


#############################################
#############################################
#       check
#############################################


def _check(
    **kwdargs,
):

    # ------------
    # key
    # ------------

    wcsys = coll._which_csys
    lout = list(coll.dobj.get(wcsys, {}).keys())
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=lout,
    )

    # ------------
    # kcsys0
    # ------------

    # ------------
    # clean
    # ------------

    lok = ['key', 'cent', 'e0', 'e1', 'e2', 'norm', 'direct', 'kcsys0']
    lout = [kk for kk in kwdargs.keys() if kk not in lok]
    for kk in lout:
        del kwdargs[kk]

    return {}
