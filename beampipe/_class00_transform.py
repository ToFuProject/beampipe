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
):

    # -----------
    # check
    # -----------

    kwd = _check(coll=coll, key_in=key_in, key_out=key_out)

    # -----------
    # transform
    # -----------

    return _get_transform(
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
        if kk != kwd['key_in']
        if coll.dobj[wcsys][kk]['ctype'] == ctype
        and coll.dobj[wcsys][kk]['nd'] == nd
        and coll.dobj[wcsys][kk]['kcsys0'] == kcsys0
    ]
    kwd['key_out'] = ds._generic_check._check_var(
        kwd['key_out'], 'key_out',
        types=str,
        allowed=lok,
    )

    # -----------
    # implemented ?
    # -----------

    if ctype != 'cart':
        msg = f"csys transform not implement for ctype = '{ctype}'\n"
        raise Exception(msg)

    return kwd


# #############################################
# #############################################
#       transform
# #############################################


def _get_transform(coll=None, kwd=None):

    # ------------
    # basics
    # ------------

    wcsys = coll._which_csys
    ctype = coll.dobj[wcsys][kwd['key_in']]['ctype']
    nd = coll.dobj[wcsys][kwd['key_in']]['nd']
    size = int(nd[0])

    lx = ['x0', 'x1', 'x2']

    # ------------
    # data
    # ------------

    origin_in = coll.dobj[wcsys][kwd['key_in']]['origin']
    origin_out = coll.dobj[wcsys][kwd['key_out']]['origin']
    dorigin = origin_in - origin_out

    de = {}
    for ii in range(size):
        de[f'e{ii}_in'] = coll.dobj[wcsys][kwd['key_in']][f'e{ii}']
        de[f'e{ii}_out'] = coll.dobj[wcsys][kwd['key_out']][f'e{ii}']

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
    # cartesian
    # ------------

    dout = {}
    if ctype == 'cart':
        for ii in range(size):

            # translation
            dout[f'd{lx[ii]}'] = {
                'data': np.sum(dorigin * de[f'e{ii}_out']),
                'units': units,
            }

            # rotation
            for jj in range(size):
                dout[f"cos_e{jj}_e{ii}"] = {
                    'data': np.sum(de[f'e{jj}_in'] * de[f"e{ii}_out"]),
                    'units': None,
                }

    return dout
