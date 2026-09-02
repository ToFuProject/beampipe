import warnings


import numpy as np
import datastock as ds


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
    # check
    # -----------

    kwd = _check(**locals())

    # -----------
    # transform
    # -----------

    return _transform(
        coll=coll,
        kwd=kwd,
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
    lok = list(coll.dobj.get(wcsys, {}).keys())

    # key_in
    kwd['key_in'] = ds._generic_check._check_var(
        kwd['key_in'], 'key_in',
        types=str,
        allowed=lok,
    )

    # ctype, nd
    ctype = coll.dobj[wcsys][kwd['key_in']]['ctype']
    nd = coll.dobj[wcsys][kwd['key_in']]['nd']
    kcsys0 = coll.dobj[wcsys][kwd['key_in']]['kcsys0']

    # key_out
    lok = [
        kk for kk in lok
        if coll.dobj[wcsys][kk]['ctype'] == ctype
        and coll.dobj[wcsys][kk]['nd'] == nd
        and coll.dobj[wcsys][kk]['kcsys0'] == kcsys0
    ]
    kwd['key_out'] = ds._generic_check._check_var(
        kwd['key_out'], 'key_out',
        types=str,
        allowed=lok,
    )

    # -------------
    # coordinates
    # -------------

    dfail = {}
    size = int(nd[0])
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

    return kwd


# #############################################
# #############################################
#       transform
# #############################################


def _transform(coll=None, kwd=None):

    # ------------
    # basics
    # ------------

    wcsys = coll._which_csys
    ctype = coll.dobj[wcsys][kwd['key_in']]['ctype']
    kcsys0 = coll.dobj[wcsys][kwd['key_in']]['kcsys0']
    nd = coll.dobj[wcsys][kwd['key_in']]['nd']
    size = int(nd[0])

    lx = ['x0', 'x1', 'x2']

    # ------------
    # units
    # ------------

    lunits = [
        coll.ddata[lx[ii]]['units'] for ii in range(size)
        if isinstance(lx[ii], str)
    ]
    if len(set(lunits)) > 1:
        msg = f"Units are different for each coordinates : {lunits}\n"
        warnings.warn(msg)
        units = None
    elif len(set(lunits)) == 1:
        units = lunits[0]
    else:
        units = None

    # ------------
    # ref
    # ------------

    lref = [
        coll.ddata[lx[ii]]['ref'] for ii in range(size)
        if isinstance(lx[ii], str)
    ]
    # TBF

    # ------------
    # values
    # ------------

    dval = {
        lx[ii]: kwd[lx[ii]] if isinstance(lx[ii], np.ndarray)
        else coll.ddata[lx[ii]]['data']
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
    # easy
    # ------------

    if kwd['key_in'] == kwd['key_out']:
        for ii in range(size):
            dout[lx[ii]]['data'] = dval[lx[ii]]

    # ------------
    # cartesian
    # ------------

    if ctype == 'cart':
        trans, rot = coll.get_csys_transform(kwd)
        for ii in range(size):
            dout[lx[ii]]['data'] = (
                trans[lx[ii]]
                + np.sum(
                    [
                        dval[lx[jj]] * rot[f'cos_e{jj}_e{ii}']
                        for jj in range(size)
                    ],
                    axis=0,
                )
            )

    else:
        msg = f"tranform for csys of ctype '{ctype}' not implemented yet!"
        raise NotImplementedError(msg)

    return dout
