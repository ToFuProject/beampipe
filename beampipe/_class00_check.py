import copy


import numpy as np
import datastock as ds


#############################################
#############################################
#       DEFAULT VALUES
#############################################

_LOK_ND = {
    'cart': ['1d', '2d', '3d'],
    'cyl': ['2d', '3d'],
    'sph': ['2d', '3d'],
}


#############################################
#############################################
#       main
#############################################


def main(
    coll=None,
    key=None,
    # cent
    origin=None,
    # ctype
    ctype=None,
    # nd
    nd=None,
    # vect
    e0=None,
    e1=None,
    e2=None,
    # vecto options
    ortho=None,
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
    # 1d vs 2d vs 3d
    # ---------------

    _unit_vectors(kwd)

    # ---------------
    # dobj
    # ---------------

    wcsys = coll._which_csys
    dobj = {
        wcsys: {
            key: copy.deepcopy(kwd),
        }
    }

    return None, None, dobj


#############################################
#############################################
#       check
#############################################


def _check(
    **kwdargs,
):
    """ check inputs for main()
    """

    # ------------
    # key
    # ------------

    coll = kwdargs['coll']
    wcsys = coll._which_csys
    kwdargs['key'] = ds._generic_check._obj_key(
        d0=coll.get(wcsys, {}),
        short='csys',
        key=kwdargs['key'],
        ndigits=None,
    )

    # ------------
    # kcsys0
    # ------------

    lref = [kk for kk in lok if coll.dobj[wcsys][kk][''] == kk]
    lok = list(coll.get(wcsys, {}).keys()) + [key]
    kwdargs['kcsys0'] = ds._generic_check._check_var(
        kwdargs['kcsys0'], 'kcsys0',
        types=str,
        allowed=lok,
        default=lref[0],
    )

    # ------------
    # ctype
    # ------------

    lok = sorted(_LOK_ND.keys())
    kwdargs['ctype'] = ds._generic_check._check_var(
        kwdargs['ctype'], 'ctype',
        types=str,
        allowed=lok,
        default=lok[0],
    )
    nd_ok = _LOK_ND[kwdargs['ctype']]

    # ------------
    # nd
    # ------------

    dv = {
        kk: kwdargs[kk] for k in ['e0', 'e1', 'e2']
        if kwdargs[kk] is not None
    }
    nd_min = len(dv)
    lok = [f"{ii}d" for ii in range(nd_min, 4)]
    lok = [kk for kk in lok if kk in nd_ok]
    kwdargs['nd'] = ds._generic_check._check_var(
        kwdargs['nd'], 'nd',
        types=str,
        allowed=lok,
    )
    size = int(kwdargs['nd'][0])

    # vs vectors
    if len(dv) > 0:
        if size - len(dv) > 1:
            msg = (
                f"For a csys of nd = '{kwdargs['nd']}' provide either:\n"
                "\t- No unit vectors (all default)\n"
                "\t- All or all but one (derived) unit vectors\n"
            )
            raise Exception(msg)

    # ------------
    # origin - provided => finite array of proper size
    # ------------

    oo = np.atleast_1d(kwdargs['origin']).ravel().astype(float)

    if np.any(~np.isfinite(oo)) or oo.size != size:
        msg = (
            f"Arg 'origin' must be:\n"
            "\t- a flat np.ndarray of finite values with size = {size}\n"
            "Provided:\n\t{kwdargs['origin']}\n"
        )
        raise Exception(msg)
    kwdargs['origin'] = oo

    # ------------
    # unit vectors - provided => finite array of proper size
    # ------------

    for kk, vv in dv.items():
        vv = np.atleast_1d(vv).ravel().astype(float)

        if np.any(~np.isfinite(vv)) or vv.size != size:
            msg = (
                f"Arg '{kk}' must be:\n"
                "\t- a flat np.ndarray of finite values with size = {size}\n"
                "Provided:\n\t{kwdargs[kk]}\n"
            )
            raise Exception(msg)
        kwdargs[kk] = vv

    # ------------
    # bool
    # ------------

    for kk in ['ortho', 'norm', 'direct']:
        kwdargs[kk] = ds._generic_check._check_var(
            kwdargs[kk], kk,
            types=bool,
            default=True,
        )

    # ------------
    # clean
    # ------------

    lok = [
        'key', 'nd', 'ctype',
        'origin,''e0', 'e1', 'e2',
        'ortho', 'norm', 'direct', 'kcsys0',
    ]
    lout = [kk for kk in kwdargs.keys() if kk not in lok]
    for kk in lout:
        del kwdargs[kk]

    return kwdargs


#############################################
#############################################
#       Unit vectors
#############################################


def _unit_vectors(
    **kwd,
):

    # ----------
    # all default
    # ----------

    lv = ['e0', 'e1', 'e2']
    if all([kwd[kk] is None for kk in lv]):
        if kwd['nd'] == '1d':
            kwd['e0'] = np.r_[0.]
        elif kwd['nd'] == '2d':
            kwd['e0'] = np.r_[1, 0.]
            kwd['e1'] = np.r_[0, 1.]
        else:
            kwd['e0'] = np.r_[1, 0., 0]
            kwd['e1'] = np.r_[0, 1., 0]
            kwd['e2'] = np.r_[0, 0., 1]

    # ----------
    # Not all default
    # ----------

    # 2d
    if kwd['nd'] == '2d':
        if kwd['e0'] is None:
            kwd['e0'] = np.r_[kwd['e1'][1], -kwd['e1'][0]]
        elif kwd['e1']:
            kwd['e1'] = np.r_[-kwd['e0'][1], kwd['e0'][0]]

    # 3d
    elif kwd['nd'] == '3d':
        if kwd['e0'] is None:
            kwd['e0'] = np.cross(kwd['e1'], kwd['e2'])
        elif kwd['e1'] is None:
            kwd['e1'] = np.cross(kwd['e2'], kwd['e0'])
        elif kwd['e2'] is None:
            kwd['e2'] = np.cross(kwd['e0'], kwd['e1'])

    # ----------
    # basis - not colinear
    # ----------

    # nd
    if kwd['nd'] != '1d':
        if kwd['nd'] == '2d':
            lcross = [np.cross(kwd['e0'], kwd['e1'])]
            emax = np.max([kwd['e0'], kwd['e1']])
        elif kwd['nd'] == '3d':
            lcross = [
                np.cross(kwd['e0'], kwd['e1']),
                np.cross(kwd['e1'], kwd['e2']),
                np.cross(kwd['e2'], kwd['e0']),
            ]
            emax = np.max([kwd['e0'], kwd['e1'], kwd['e2']])

        # check colinearity
        if np.any(np.abs(lcross) < 1e-9 * emax):
            msg = (
                "Unit vectors must not be co-linear!"
            )
            raise Exception(msg)

    # ----------
    # norm
    # ----------

    if kwd['norm'] is True:
        for kk in lv:
            kwd[kk] = kwd[kk] / np.sqrt(np.sum(kwd[kk]**2))

    # -----------
    # ortho
    # -----------

    if kwd['ortho'] is True and kwd['nd'] != '1d':
        if kwd['nd'] == '2d':
            lsca = [np.sum(kwd['e0'] * kwd['e1'])]
        elif kwd['nd'] == '3d':
            lsca = [
                np.sum(kwd['e0'] * kwd['e1']),
                np.sum(kwd['e1'] * kwd['e2']),
                np.sum(kwd['e2'] * kwd['e0']),
            ]

        # check perpendicularity
        if np.any(np.abs(lsca) > 1e-9 * emax):
            msg = (
                "Unit vectors must be perpendicular!"
            )
            raise Exception(msg)

    # ----------
    # direct
    # ----------

    if kwd['direct'] is True and kwd['nd'] != '1d':
        if kwd['nd'] == '2d':
            vect = np.r_[-kwd['e0'][1], kwd['e0'][0]]
            sca = np.sum(vect * kwd['e1'])
            if sca < 0.:
                msg = (
                    "The vector basis must be direct!"
                )
                raise Exception(msg)
        elif kwd['nd'] == '3d':
            vect = np.cross(kwd['e0'], kwd['e1'])
            sca = np.sum(vect * kwd['e2'])
            if sca < 0.:
                msg = (
                    "The vector basis must be direct!"
                )
                raise Exception(msg)

    return
