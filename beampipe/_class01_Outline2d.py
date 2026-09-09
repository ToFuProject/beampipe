import copy
from typing import Annotated


from ._class00_CSYS import CSYS as Previous
from . import _class01_check as _check
# from . import _class01_show as _show


__all__ = ['Outline2d']


#############################################
#############################################
#       DEFAULT VALUES
#############################################


_WHICH_OUTLINE2D = 'outline2d'


#############################################
#############################################
#       Spectral Lines
#############################################


class Outline2d(Previous):

    _ddef = copy.deepcopy(Previous._ddef)
    _which_outline2d = _WHICH_OUTLINE2D

    # -------------------
    # add csys
    # -------------------

    def add_outline2d(
        self,
        key: Annotated[str | None, 'key of the outline2d to be added'] = None,
        key_csys: Annotated[str | None, 'key of the csys'] = None,
        # circle
        center=None,
        radius=None,
        # polygon
        outline_x0=None,
        outline_x1=None,
        # from svg
    ) -> None:
        """ Add a outline2d

        Coordinates are given with respect to key_csys

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

