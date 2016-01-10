from ThreeMessageSubframe import ThreeMessageSubframe

class FourMessageSubframe(ThreeMessageSubframe):
    '''
    This subframe class models a subframe as three consecutive messages

    the following diagram illustrates a superframe of 5 four message subframes example:

    +--------------+
    | 5 SUPERFRAME |
    |______________|
    |10|10|10|10|10|
    |11|11|11|11|11|
    |CC|CC|CC|CC|CC|
    |XX|XX|XX|XX|XX|
    +--------------+
    '''
    def __init__(self, firstMessage,secondMessage,thirdMessage,fourthMessage):
        ThreeMessageSubframe.__init__(self,firstMessage,secondMessage,thirdMessage)
        self.FourthMessage = fourthMessage
    def __next__(self):
        raise NotImplementedError("Next is not implemented yet")

    def __iter__(self):
        raise NotImplementedError("Iter is not implemented yet")