#from sage.structure.sage_object import SageObject
class MessageTimingHelper():
    '''
    This is a helper class which facilitates message optimization calculations
    '''
    @staticmethod
    def MessagingRate(broadcastInterval,messageRate):
        '''

        :param broadcastInterval: the broadcasting interval for a particular message type or dataset
        :param messageRate: the time needed to broadcast one message (6 seconds for l5, 12 seconds for l2c)
        :return: broadcastInterval/messageRate
        '''
        if messageRate is not 0:
            return broadcastInterval/messageRate
        else:
            raise ZeroDivisionError()


    @staticmethod
    def L5MessagingRate():
        return 6

    @staticmethod
    def L2CMessagingRate():
        return 12

    @staticmethod
    def MinutesToSeconds(minutes):
        return minutes * 60
