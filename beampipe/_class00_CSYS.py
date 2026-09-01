import copy


from datastock import DataStock as Previous


# from . import _class00_check as _check
from . import _class00_check as _check
from . import _class00_show as _show


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
        key=None,
        # cent
        origin=None,
        # ctype
        ctype=None,
        # vect
        e0=None,
        e1=None,
        e2=None,
        # vecto options
        norm=None,
        direct=None,
        # ref csys
        kcsys0=None,
    ):
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
    # convert csys
    # -------------------
