from typing import Optional


class ProtocolCollator:
    '''
    Class that is able to report about which protocols it implements.

    Use ``declare_protocol`` in a subclass' init method to indicate that the 
    object implements a given protocol. If a subclass was previously marked 
    as implementing a protocol, and you now want it to behave as if it 
    doesn't implement that protocol, you can also ``deny_protocol``.

    Then, before attempting to call a method belonging to a protocol that a
    given object may or may not implement, use the ``implements(object, 
    protocol)`` function to check whether the object has declared that it 
    implements the protocol. 
    '''
    def __init__(self):
        self.__protocols: list[type] = []

    def declare_protocol(self, protocol: type) -> None:
        if not protocol in self.__protocols:
            self.__protocols.append(protocol)

    def deny_protocol(self, protocol: type) -> None:
        if protocol in self.__protocols:
            self.__protocols.remove(protocol)

    def implements(self, protocol: type) -> bool:
        return protocol in self.__protocols
    
    @property
    def protocols(self) -> list[type]:
        return self.__protocols.copy()