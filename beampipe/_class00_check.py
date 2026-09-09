import numpy as np
import astropy.units as asunits
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

_ORIGIN = np.r_[0., 0., 0.]

_DUNITS = {
    'cart': 'm',
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
    # units
    units0=None,
    units1=None,
    units2=None,
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

    dcsys = {
        kk: vv for kk, vv in kwd.items()
        if not kk.startswith('e')
        and not kk.startswith('units')
        and kk != 'key'
    }

    le = [kk for kk in ['e0', 'e1', 'e2'] if kwd.get(kk) is not None]
    for ie, ke in enumerate(le):
        dcsys[ke] = {
            'data': kwd[ke],
            'units': kwd[f'units{ie}'],
        }

    wcsys = coll._which_csys
    dobj = {wcsys: {kwd['key']: dcsys}}

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
        d0=coll.dobj.get(wcsys, {}),
        short='csys',
        key=kwdargs['key'],
        ndigits=None,
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
        kk: kwdargs[kk] for kk in ['e0', 'e1', 'e2']
        if kwdargs[kk] is not None
    }
    nd_min = len(dv)
    lok = [f"{ii}d" for ii in range(nd_min, 4)]
    lok = [kk for kk in lok if kk in nd_ok]

    nn = list(set([len(vv) for vv in dv.values()]))
    if len(nn) > 1:
        msg = "Unit vectors do not seem to have consistent size!"
        raise Exception(msg)
    elif len(nn) == 1:
        nd_def = f"{nn[0]}d"
    else:
        nd_def = lok[-1]

    kwdargs['nd'] = ds._generic_check._check_var(
        kwdargs['nd'], 'nd',
        types=str,
        allowed=lok,
        default=nd_def,
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
    # kcsys0
    # ------------

    lok = [
        kk for kk, vv in coll.dobj.get(wcsys, {}).items()
        if vv['ctype'] == kwdargs['ctype']
        and vv['nd'] == kwdargs['nd']
    ]
    lref = [kk for kk in lok if coll.dobj[wcsys][kk]['kcsys0'] == kk]
    kwdargs['kcsys0'] = ds._generic_check._check_var(
        kwdargs['kcsys0'], 'kcsys0',
        types=str,
        allowed=lok + [kwdargs['key']],
        default=(lref + [kwdargs['key']])[0],
    )

    # ------------
    # origin - provided => finite array of proper size
    # ------------

    if kwdargs['origin'] is None:
        kwdargs['origin'] = np.copy(_ORIGIN)

    oo = np.atleast_1d(kwdargs['origin']).ravel().astype(float)

    if np.any(~np.isfinite(oo)) or oo.size != size:
        msg = (
            "Arg 'origin' must be:\n"
            f"\t- a flat np.ndarray of finite values with size = {size}\n"
            f"Provided:\n\t{kwdargs['origin']}\n"
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
        'origin',
        'e0', 'e1', 'e2',
        'units0', 'units1', 'units2',
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


def _unit_vectors(kwd):

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
        elif kwd['e1'] is None:
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
    # clean extra
    # ----------

    size = int(kwd['nd'][0])
    for ii in range(size, 3):
        estr = f"e{ii}"
        if kwd[estr] is not None:
            msg = (
                f"Arg '{estr}' provided for a '{kwd['nd']}' csys!\n"
                f"Provided: {kwd[estr]}\n"
            )
            raise Exception(msg)

    # ----------
    # basis - not colinear
    # ----------

    # nd
    if kwd['nd'] != '1d':
        if kwd['nd'] == '2d':
            dcross = {'e0 x e1': np.cross(kwd['e0'], kwd['e1'])}
            emax = np.max([kwd['e0'], kwd['e1']])
        elif kwd['nd'] == '3d':
            dcross = {
                'e0 x e1': np.linalg.norm(np.cross(kwd['e0'], kwd['e1'])),
                'e1 x e2': np.linalg.norm(np.cross(kwd['e1'], kwd['e2'])),
                'e2 x e0': np.linalg.norm(np.cross(kwd['e2'], kwd['e0'])),
            }
            emax = np.max([kwd['e0'], kwd['e1'], kwd['e2']])

        # check colinearity
        dfail = {
            kk: vv for kk, vv in dcross.items() if np.abs(vv) < 1e-9 * emax
        }
        if len(dfail) > 0:
            lstr = [f"\t- {kk} = vv" for kk, vv in dfail.items()]
            msg = (
                "Unit vectors must not be co-linear!\n"
                + "\n".join(lstr)
            )
            raise Exception(msg)

    # ----------
    # norm
    # ----------

    if kwd['norm'] is True:
        for ii in range(size):
            estr = f"e{ii}"
            kwd[estr] = kwd[estr] / np.sqrt(np.sum(kwd[estr]**2))

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

    # ----------
    # units
    # ----------

    lunits = ['units0', 'units1', 'units2']
    for ii in range(size):
        kwd[lunits[ii]] = ds._generic_check._check_var(
            kwd[lunits[ii]], lunits[ii],
            types=str,
            default=_DUNITS[kwd['ctype']],
        )
        try:
            kwd[lunits[ii]] = asunits.Unit(kwd[lunits[ii]])
        except Exception:
            pass

    # clean
    for ii in range(size, 3):
        if kwd[lunits[ii]] is not None:
            msg = (
                f"Arg '{lunits[ii]}' provided for a '{kwd['nd']}' csys!\n"
                f"Provided: {kwd[lunits[ii]]}\n"
            )
            raise Exception(msg)

    # uniformity
    lunits = [kwd[f'units{ii}'] for ii in range(size)]
    if len(set(lunits)) != 1:
        msg = "Non-uniform units!"
        raise Exception(msg)

    # ---------------
    # clean and check
    # ---------------

    lNone = [kk for kk, vv in kwd.items() if vv is None]
    assert len(lNone) == (3-size)*2
    for kk in lNone:
        del kwd[kk]

    return
