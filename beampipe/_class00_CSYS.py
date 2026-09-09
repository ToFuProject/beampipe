import copy
from typing import Annotated


import numpy as np
from datastock import DataStock as Previous


# from . import _class00_check as _check
from . import _class00_check as _check
from . import _class00_show as _show
from . import _class00_transform as _transform
from . import _class00_transform_coords as _transform_coords


__all__ = ['CSYS']


#############################################
#############################################
#       DEFAULT VALUES
#############################################


_WHICH_CSYS = 'csys'


#############################################
#############################################
#       Spectral Lines
#############################################


class CSYS(Previous):

    _ddef = copy.deepcopy(Previous._ddef)
    _which_csys = _WHICH_CSYS

    # -------------------
    # add csys
    # -------------------

    def add_csys(
        self,
        key: Annotated[str | None, 'key of the csys to be added'] = None,
        # cent
        origin: Annotated[np.ndarray | None, "coords of the csys origin"] = None,
        # ctype
        ctype: Annotated[str | None, "type of csys (cart, ...)"] = None,
        # vect
        e0: Annotated[np.ndarray | None, "coords of unit vector e0"] = None,
        e1: Annotated[np.ndarray | None, "coords of unit vector e1"] = None,
        e2: Annotated[np.ndarray | None, "coords of unit vector e2"] = None,
        # units
        units0: Annotated[str | None, "units of coords along e0"] = None,
        units1: Annotated[str | None, "units of coords along e1"] = None,
        units2: Annotated[str | None, "units of coords along e2"] = None,
        # vector options
        ortho: Annotated[bool | None, "Are vectors orthogonal"] = None,
        norm: Annotated[bool | None, "Are vectors normalized"] = None,
        direct: Annotated[bool | None, "Is the vectors basis direct"] = None,
        # ref csys
        kcsys0: Annotated[str | None, "csys in which coords are expressed"] = None,
    ) -> None:
        """ Add a csys

        Can be 1d, 2d or 3d
        origin must be an iterable with accordingly 1, 2 or 3 coordinates
        ctype is the
        1 2 or 3 base vectors must be provided accordingly
        if norm = True => they will be normalized
        if direct = True, they should form a direct base (for 2d and 3d only)

        Coordinates are given with respect to a ref csys kcsys0

        """

        # ------------
        # check inputs
        # ------------

        dref, ddata, dobj = _check.main(coll=self, **locals())

        # ------------
        # Populate
        # ------------

        self.update(dref=dref, ddata=ddata, dobj=dobj)

        return

    # -------------------
    # show
    # -------------------

    def _get_show_obj(self, which=None):
        if which == self._which_csys:
            return _show._show
        else:
            return super()._get_show_obj(which)

    def _get_show_details(self, which=None):
        if which == self._which_csys:
            return _show._show_details
        else:
            return super()._get_show_details(which)

    # -------------------
    # remove csys
    # -------------------

    # -------------------
    # transform
    # -------------------

    def get_csys_transform(
        self,
        key_in: Annotated[str | None, 'key to csys'] = None,
        key_out: Annotated[str | None, 'key to csys'] = None,
    ) -> dict:
        """ Get the transform needed to get from one to another csys

        Returns a dict
        """
        return _transform.main(coll=self, key_in=key_in, key_out=key_out)

    def transform_csys_coords(
        self,
        key_in=None,
        key_out=None,
        # coordinates
        x0=None,
        x1=None,
        x2=None,
    ):
        """ Transform coordinates from a given csys into another

        coordinates have to be broadcastable arrays
        can be provided as key to broadcastable ddata
        """

        return _transform_coords.main(coll=self, **locals())

    # -------------------
    # move within csys
    # -------------------

    def move_translate_by():
        return

    def move_rotate_by():
        return

    # -------------------
    # move to align with something
    # -------------------

    def move_align_to():
        return
