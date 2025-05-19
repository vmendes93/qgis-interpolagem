import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from interpoladores.base import InterpoladorBase

def test_base_interpolador_erro():
    base = InterpoladorBase()
    with pytest.raises(NotImplementedError):
        base.interpolar()
