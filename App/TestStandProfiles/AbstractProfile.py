from abc import ABC, abstractmethod, abstractproperty

class AbstractProfile(ABC):

    test_stand = None

    @abstractproperty
    def name(self):
        raise NotImplementedError


    @abstractproperty
    def test_property(self):
        raise NotImplementedError

    @abstractmethod
    def my_method(self):
        raise NotImplementedError
