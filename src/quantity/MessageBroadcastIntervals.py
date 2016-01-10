#from sage.structure.sage_object import SageObject
from MessageTimingHelper import MessageTimingHelper
class MessageBroadcastIntervals():
    '''
    This depicts a message broadcast interval for either L25 or L5

    This class models L5 however the L2C and L5 requirements are equivalent.

    Please see ICD 705
    '''

    def __init__(self, SvCount,SignalType):
        '''

        :param SvCount: the number of Svs in the constellation (assuming healthy and unhealthy)
        :param SignalType: 2 -> L2C 5 -> L5
        :return: creates an object that contains the constraints that are needed to model the problem
        '''

        self.SignalType = SignalType
        #Initialized to zero for now,  Can be used for customizing model later on
        self.Type10Rate         = 0                                        #First Ephemeris Messsage
        self.Type11Rate         = 0                                        #Second Ephemeris Message
        self.TypeCcRate         = 0                                        #Clock Correction Data
        self.TypeIonoRate       = 0                                        #Iono Data
        self.TypeRaRate         = 0                                        #Reduced Almanac Data
        self.TypeMaRate         = 0                                        #Midi Almanac Data
        self.TypeEopRate        = 0                                        #Eop Data
        self.TypeUtcRate        = 0                                        #Utc Data
        self.TypeDcRate         = 0                                        #Dc Data
        self.TypeGgtoRate       = 0                                        #Ggto Data
        if self.SignalType == 2:
            self.MessageRate = MessageTimingHelper.L2CMessagingRate()
            self.BuildMessagingDataRates()
        elif self.SignalType == 5:
            self.MessageRate = MessageTimingHelper.L5MessagingRate()
            self.BuildMessagingDataRates()
        else:
            raise Exception(':param SignalType: 2 -> L2C 5 -> L5')
        self.SvCount = SvCount

    def BuildMessagingDataRates(self):
        raise NotImplementedException()