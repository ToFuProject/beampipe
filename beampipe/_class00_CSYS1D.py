import copy


import numpy as np
import datastock as ds
import ds.Collection as Previous



# from . import _class00_check as _check
from . import _class00_check as _check


__all__ = ['SYS1D']


#############################################
#############################################
#       DEFAULT VALUES
#############################################


_QUANT_NE = 'ne'
_QUANT_TE = 'Te'
_UNITS_LAMBDA0 = 'm'


#############################################
#############################################
#       Spectral Lines
#############################################


class CSYS1D(Previous):

    _ddef = copy.deepcopy(Previous._ddef)
    _which_csys1d = 'csys1d'

    # -------------------
    # add csys1d
    # -------------------

    def add_csys1d(self, key=None, csys_cent=None, csys_vect=None):
        """ Add a csys1d
        """
        _check.add_csys1d(
            coll=self,
            key=key,
        )














