from __future__ import annotations
from inspect import signature
from abc import ABC
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from StateMachine.TestStand import TestStand

class AbstractProfile(ABC):
    test_stand: TestStand = None
    current_step = 0
    trial_time = 0

    def is_valid(self):
        _is_valid = True
        try:
            getattr(self, "sidebar_values")
            getattr(self, "sequence_columns")
            getattr(self, "dataframe_columns")
            getattr(self, "start")
            getattr(self, "tick")
            getattr(self, "end")
            getattr(self, "get_sidebar_values")
            getattr(self, "set_sequence_values")
            getattr(self, "get_dataframe_values")

        except Exception as e:
            print("TestStandBehaviour Not Valid: " + str(e))
            _is_valid = False

        if(_is_valid):    
            _is_valid = callable(getattr(self, "start"))
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: start attribute is not callable.")

        if(_is_valid):
            _is_valid = callable(getattr(self, "tick"))
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: tick attribute is not callable.")
        
        if(_is_valid):
            _is_valid = callable(getattr(self, "end"))
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: end attribute is not callable.")

        if(_is_valid):
            _is_valid = callable(getattr(self, "get_sidebar_values"))
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: get_sidebar_values attribute is not callable.")

        if(_is_valid):
            _is_valid = callable(getattr(self, "set_sequence_values"))
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: set_sequence_values attribute is not callable.")

        if(_is_valid):
            _is_valid = callable(getattr(self, "get_dataframe_values"))
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: get_dataframe_values attribute is not callable.")
            
        if(_is_valid):
            _is_valid = isinstance(getattr(self, "sidebar_values"), List)
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: sidebar_values should be of type List.")

        if(_is_valid):
            _is_valid = isinstance(getattr(self, "sequence_columns"), List)
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: sequence_columns should be of type List.")

        if(_is_valid):
            _is_valid = isinstance(getattr(self, "dataframe_columns"), List)
            if(not _is_valid):
                print("TestStandBehaviour Not Valid: dataframe_columns should be of type List.")
            
        if(_is_valid):
            print("TestStandBehaviour is Valid.")
        return _is_valid

