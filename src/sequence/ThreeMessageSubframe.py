from sage.structure.sage_object import SageObject

class ThreeMessageSubframe(SageObject):
    '''
    This subframe class models a subframe as three consecutive messages

    the following diagram illustrates a superframe of 5 three message subframes example:

    +--------------+
    | 5 SUPERFRAME |
    |______________|
    |10|10|10|10|10|
    |11|11|11|11|11|
    |CC|CC|CC|CC|CC|
    +--------------+
    '''
    def __init__(self, firstMessage,secondMessage,thirdMessage):
        self.FirstMessage = firstMessage
        self.SecondMessage = secondMessage
        self.ThirdMessage = thirdMessage

    def __next__(self):
        raise NotImplementedError("Next is not implemented yet")

    def __iter__(self):
        raise NotImplementedError("Iter is not implemented yet")
