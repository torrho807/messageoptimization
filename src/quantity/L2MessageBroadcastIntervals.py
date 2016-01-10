from MessageBroadcastIntervals import MessageBroadcastIntervals
from MessageTimingHelper import MessageTimingHelper
class L2MessageBroadcastIntervals(MessageBroadcastIntervals):
    def __init__(self,SvCount):
        '''
        Creates Broadcast Intervals for L2 signal
        :param SvCount: the number of Svs in the constellation (assuming healthy and unhealthy)
        :return:Creates L2 Broadcast Intervals For Messaging
        '''
        MessageBroadcastIntervals.__init__(self,SvCount,2)

    def BuildMessagingDataRates(self):
        self.Type10Rate         = MessageTimingHelper.MessagingRate(48,self.MessageRate)                                        #First Ephemeris Messsage
        self.Type11Rate         = MessageTimingHelper.MessagingRate(48,self.MessageRate)                                        #Second Ephemeris Message
        self.TypeCcRate         = MessageTimingHelper.MessagingRate(48,self.MessageRate)                                        #Clock Correction Data
        self.TypeIonoRate       = MessageTimingHelper.MessagingRate(288,self.MessageRate)                                       #Iono Data
        self.TypeRaRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(20),self.MessageRate)  #Reduced Almanac Data
        self.TypeMaRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(120),self.MessageRate) #Midi Almanac Data
        self.TypeEopRate        = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(20),self.MessageRate)  #Eop Data
        self.TypeUtcRate        = MessageTimingHelper.MessagingRate(288,self.MessageRate)                                       #Utc Data
        self.TypeDcRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(30),self.MessageRate)  #Dc Data
        self.TypeGgtoRate       = MessageTimingHelper.MessagingRate(288,self.MessageRate)                                       #Ggto Data