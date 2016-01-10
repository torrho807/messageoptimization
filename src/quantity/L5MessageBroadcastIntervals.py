from MessageBroadcastIntervals import MessageBroadcastIntervals
from MessageTimingHelper import MessageTimingHelper
class L5MessageBroadcastIntervals(MessageBroadcastIntervals):
    def __init__(self,SvCount):
        '''
        Creates Broadcast Intervals for L5 signal
        :param SvCount: the number of Svs in the constellation (assuming healthy and unhealthy)
        :return:Creates L5 Broadcast Intervals For Messaging
        '''
        MessageBroadcastIntervals.__init__(self,SvCount,5)

    def BuildMessagingDataRates(self):
        self.Type10Rate         = MessageTimingHelper.MessagingRate(24,self.MessageRate)                                        #First Ephemeris Messsage
        self.Type11Rate         = MessageTimingHelper.MessagingRate(24,self.MessageRate)                                        #Second Ephemeris Message
        self.TypeCcRate         = MessageTimingHelper.MessagingRate(24,self.MessageRate)                                        #Clock Correction Data
        self.TypeIonoRate       = MessageTimingHelper.MessagingRate(144,self.MessageRate)                                       #Iono Data
        self.TypeRaRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(10),self.MessageRate)  #Reduced Almanac Data
        self.TypeMaRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(60),self.MessageRate)  #Midi Almanac Data
        self.TypeEopRate        = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(15),self.MessageRate)  #Eop Data
        self.TypeUtcRate        = MessageTimingHelper.MessagingRate(144,self.MessageRate)                                       #Utc Data
        self.TypeDcRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(15),self.MessageRate)  #Dc Data
        self.TypeGgtoRate       = MessageTimingHelper.MessagingRate(144,self.MessageRate)                                       #Ggto Data
