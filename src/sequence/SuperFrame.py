from sage.structure.sage_object import SageObject

class Superframe(SageObject):
    '''
    This class implements a superframe of size N

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
    def __init__(self, subframeCount):
        '''
        :param subframeCount: an integer that specifices how many subframes are contained in the subframe
        :return:
        '''
        self.SubframeCount = 0
        if subframeCount > -1:
            self.SubframeCount = subframeCount

    def __next__(self):
        raise NotImplementedError("Next is not implemented yet")

    def __iter__(self):
        raise NotImplementedError("Iter is not implemented yet")
    def __add__(self, other):
        tempSubframeCount = self.SubframeCount + other.SubframeCount
        tempSuperFrame = Superframe(tempSubframeCount)
        for subframe in self:
            for message in subframe:
                raise NotImplementedError("Not Implemented Yet")