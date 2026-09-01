# -*- coding: utf-8 -*-


#############################################
#############################################
#       DEFAULTS
#############################################


_LORDER = [
    'nd', 'ctype',
    'ortho', 'norm', 'direct',
    'kcsys0',
]


#############################################
#############################################
#       Show
#############################################


def _show(coll=None, which=None, lcol=None, lar=None, show=None):

    # ---------------------------
    # column names
    # ---------------------------

    lcol.append([which] + _LORDER)

    # ---------------------------
    # data
    # ---------------------------

    lkey = [
        k1 for k1 in coll._dobj.get(which, {}).keys()
        if show is None or k1 in show
    ]

    lar0 = []
    for k0 in lkey:

        # initialize with key
        arr = [k0]

        # loop
        for k1 in _LORDER:

            # parameters
            nn = str(coll.dobj[which][k0].get(k1))
            arr.append(nn)

        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar


#############################################
#############################################
#       Show single diag
#############################################


def _show_details(coll=None, key=None, lcol=None, lar=None, show=None):

    wcsys = coll._which_csys
    size = int(coll.dobj[wcsys][key]['nd'][0])

    # ---------------------------
    # column names
    # ---------------------------

    lcol.append([
        'attr', 'x0', 'x1', 'x2',
    ])

    # ---------------------------
    # data
    # ---------------------------

    lar0 = []
    lk = ['origin', 'e0', 'e1', 'e2']
    for kk in lk:

        # initialize with key, type
        arr = [kk]

        # is2d
        for ii in range(3):
            if ii < size:
                nn = coll.dobj[wcsys][key][kk][ii]
            else:
                nn = ''
            arr.append(nn)

        # aggregate
        lar0.append(arr)

    lar.append(lar0)

    return lcol, lar
