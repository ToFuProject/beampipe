import warnings


import numpy as np


# #############################################
# #############################################
#       main
# #############################################


def main(
    coll=None,
    key_in=None,
    key_out=None,
    # coordinates
    x0=None,
    x1=None,
    x2=None,
    # unused
    **kwdargs,
):

    # -----------
    # get transform
    # -----------

    dtrans = coll.get_csys_transform(key_in=key_in, key_out=key_out)

    # -----------
    # check
    # -----------

    kwd = _check(**locals())

    # -----------
    # transform
    # -----------

    return _transform(
        coll=coll,
        kwd=kwd,
        dtrans=dtrans,
    )


# #############################################
# #############################################
#       check
# #############################################


def _check(**kwd):

    # -----------
    # key_in vs key_out
    # -----------

    coll = kwd['coll']
    wcsys = coll._which_csys

    # ctype, nd
    nd = coll.dobj[wcsys][kwd['key_in']]['nd']
    size = int(nd[0])

    # -------------
    # coordinates
    # -------------

    dfail = {}
    lx = ['x0', 'x1', 'x2']
    for ii in range(size):

        # None
        if kwd[lx[ii]] is None:
            dfail[lx[ii]] = "is None"

        # str
        elif isinstance(kwd[lx[ii]], str):
            if kwd[lx[ii]] not in coll.ddata.keys():
                dfail[lx[ii]] = f"not found in ddata ({kwd[lx[ii]]})"

        # array
        else:
            try:
                kwd[lx[ii]] = np.atleast_1d(kwd[lx[ii]])
            except Exception:
                dfail[lx[ii]] = (
                    f"not convertible to np.ndarray ({type(kwd[lx[ii]])})"
                )

    # errors
    if len(dfail) > 0:
        lstr = [f"\t- {kk}: vv" for kk, vv in dfail.items()]
        msg = (
            "Coordinates are not valid:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # clean-up
    for ii in range(size, 3):
        kwd[lx[ii]] = None

    # -------------
    # broadcastable coordinates
    # -------------

    dshapes = {
        lx[ii]: kwd[lx[ii]].shape if isinstance(kwd[lx[ii]], np.ndarray)
        else coll.ddata[lx[ii]]['data'].shape
        for ii in range(size)
    }

    try:
        _ = np.broadcast_shapes(*list(dshapes.values()))
    except Exception:
        lstr = [f"\t- {kk}: vv" for kk, vv in dshapes.items()]
        msg = (
            "All coordinates must be broadcastable!\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # -------------
    # clean
    # -------------

    lok = ['key_in', 'key_out', 'x0', 'x1', 'x2']
    lout = [kk for kk in kwd.keys() if kk not in lok]
    for kk in lout:
        del kwd[kk]
    for ii in range(size, 3):
        del kwd[f"x{ii}"]

    return kwd


# #############################################
# #############################################
#       transform
# #############################################


def _transform(coll=None, kwd=None, dtrans=None):

    # ------------
    # basics
    # ------------

    wcsys = coll._which_csys
    ctype = coll.dobj[wcsys][kwd['key_in']]['ctype']
    nd = coll.dobj[wcsys][kwd['key_in']]['nd']
    size = int(nd[0])

    lx = ['x0', 'x1', 'x2']

    # ------------
    # ref
    # ------------

    lref = [
        coll.ddata[kwd[lx[ii]]]['ref'] for ii in range(size)
        if isinstance(kwd[lx[ii]], str)
    ]

    if len(lref) > 0:
        if len(set(lref)) > 1:
            msg = "Coordinates do not share the same ref!"
            warnings.warn(msg)
            ref = None
        else:
            ref = lref[0]
    else:
        ref = None

    # ------------
    # units
    # ------------

    units = coll.dobj[wcsys][kwd['key_in']]['e0']['units']

    lunits = [
        coll.ddata[kwd[lx[ii]]]['units'] for ii in range(size)
        if isinstance(kwd[lx[ii]], str)
    ]

    if len(lunits) > 0:

        if len(set(lunits)) > 1:
            msg = "Coordinates do not share the same units!"
            raise Exception(msg)

        elif lunits[0] != units:
            msg = "Coordinates do not share the same units as unit vectors!"
            raise Exception(msg)


    # ------------
    # values
    # ------------

    dval = {
        lx[ii]: kwd[lx[ii]] if isinstance(kwd[lx[ii]], np.ndarray)
        else coll.ddata[kwd[lx[ii]]]['data']
        for ii in range(size)
    }

    # ------------
    # dout
    # ------------

    dout = {
        lx[ii]: {
            'data': None,
            'units': units,
            'ref': ref,
        }
        for ii in range(size)
    }

    # ------------
    # cartesian
    # ------------

    if ctype == 'cart':
        for ii in range(size):
            dout[lx[ii]]['data'] = (
                dtrans[f"d{lx[ii]}"]['data']
                + np.sum(
                    [
                        dval[lx[jj]] * dtrans[f'cos_e{jj}_e{ii}']['data']
                        for jj in range(size)
                    ],
                    axis=0,
                )
            )

    else:
        msg = f"tranform for csys of ctype '{ctype}' not implemented yet!"
        raise NotImplementedError(msg)

    return dout
