from sage.structure.sage_object import SageObject
from sage.numerical.mip import MixedIntegerLinearProgram
from OptimizationGoal import OptimizationGoal
from MessageTimingHelper import MessageTimingHelper
class CnavMessageModel(SageObject):
    '''
    This builds a list of linear constraints for CNAV messaging
    self.Type10Rate         = MessageTimingHelper.MessagingRate(48,self.MessageRate)                                        #First Ephemeris Messsage
    self.Type11Rate         = MessageTimingHelper.MessagingRate(48,self.MessageRate)                                        #Second Ephemeris Message
    self.TypeCcRate         = MessageTimingHelper.MessagingRate(48,self.MessageRate)                                        #Clock Correction Data
    self.TypeIonoRate       = MessageTimingHelper.MessagingRate(288,self.MessageRate)                                       #Iono Data
    self.TypeRaRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(20),self.MessageRate)  #Reduced Almanac Data
    self.TypeMaRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(120),self.MessageRate)  #Midi Almanac Data
    self.TypeEopRate        = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(20),self.MessageRate)  #Eop Data
    self.TypeUtcRate        = MessageTimingHelper.MessagingRate(288,self.MessageRate)                                       #Utc Data
    self.TypeDcRate         = MessageTimingHelper.MessagingRate(MessageTimingHelper.MinutesToSeconds(30),self.MessageRate)  #Dc Data
    self.TypeGgtoRate       = MessageTimingHelper.MessagingRate(288,self.MessageRate)
    '''
    def __init__(self, broadcastInterval, milp, optimizationGoal, type10,type11,typeCc,typeIono,typeRa,typeMa,typeEop,typeUtc,typeDc,typeGgto):
        '''

        :param broadcastInterval: Provide the modelling constraints
        :param milp: MixedIntegerLinearProgram object
        :param optimizationGoal: specifies the optimization goal we wish to consider for Cnav
        :param type10:      true/false: Do we want to model message type 10?
        :param type11:      true/false: Do we want to model message type 11?
        :param typeCc:      true/false: Do we want to model clock correction data?
        :param typeIono:    true/false: Do we want to model Iono data?
        :param typeRa:      true/false: Do we want to model Reduced Almanac?
        :param typeMa:      true/false: Do we want to model Midi Almanac?
        :param typeEop:     true/false: Do we want to model EOP data?
        :param typeUtc:     true/false: Do we want to model UTC data?
        :param typeDc:      true/false: Do we want to model Dc data?
        :param typeGgto:    true/false: Do we want to model Ggto data?
        :return: a list of linear constraints corresponding to the desired CnavModel
        '''
        self.broadcastInterval = broadcastInterval
        #check if MixedIntegerLinearProgram
        if type(milp) is type(MixedIntegerLinearProgram):
            self.milp = milp
        else:
            self.milp = MixedIntegerLinearProgram()
        #create messaging variable
        self.msg = self.milp.new_variable(integer=True, nonnegative=True)
        #determine worst broadcasting interval requirement
        self.totalBroadcastInterval = self.DetermineTotalBroadcastInterval(type10,type11,typeCc,typeIono,typeRa,typeMa,typeEop,typeUtc,typeDc,typeGgto)
        #check if OptimizationGoal
        if type(optimizationGoal) is not type(OptimizationGoal):
            self.optimizationGoal = OptimizationGoal()
        elif:
            self.optimizationGoal = optimizationGoal
        #set types
        self.type10 = type10
        self.type11 = type11
        self.typeCc = typeCc
        self.typeIono = typeIono
        self.typeRa = typeRa
        self.typeMa = typeMa
        self.typeEop = typeEop
        self.typeUtc = typeUtc
        self.typeDc = typeDc
        self.typeGgto = typeGgto
        if type10:
            BuildType10()
        if type11:
            BuildType11()
        if typeCc:
            BuildTypeCc()
        if typeIono:
            BuildTypeIono()
        if typeRa:
            BuildTypeRa()
        if typeMa:
            BuildTypeMa()
        if typeEop:
            BuildTypeEop()
        if typeUtc:
            BuildTypeUtc()
        if typeDc:
            BuildTypeDc()
        if typeGgto:
            BuildTypeGgto()
    def BuildType10(self):
        '''
        Builds type 10 constraints
        :return:
        '''
        messageQuantity = int(self.totalBroadcastInterval / 4)
        self.milp.add_constraint(self.msg[10] >= messageQuantity)
    def BuildType11(self):
        '''

        :return:
        '''
        messageQuantity = int(self.totalBroadcastInterval / 4)
        self.milp.add_constraint(self.msg[11] >= messageQuantity)
    def BuildTypeCc(self):
        '''

        :return:
        '''
        messageQuantity = int(self.totalBroadcastInterval / 4)
        self.milp.add_constraint(self.msg[30] + self.msg[31] + self.msg[32] + self.msg[33] + self.msg[34] + self.msg[35] + self.msg[36] + self.msg[37] >= messageQuantity)

    def BuildTypeIono(self):
        '''

        :return:
        '''
        raise NotImplementedException()
    def BuildTypeRa(self):
        '''

        :return:
        '''
        raise NotImplementedException()
    def BuildTypeMa(self):
        '''

        :return:
        '''
        raise NotImplementedException()
    def BuildTypeEop(self):
        '''

        :return:
        '''
    def BuildTypeUtc(self):
        '''

        :return:
        '''
        raise NotImplementedException()
    def BuildTypeDc(self):
        '''

        :return:
        '''
        raise NotImplementedException()
    def BuildTypeGgto(self):
        '''

        :return:
        '''
        raise NotImplementedException()
    def DetermineTotalBroadcastInterval(self,type10,type11,typeCc,typeIono,typeRa,typeMa,typeEop,typeUtc,typeDc,typeGgto):
        '''

        :param type10:      true/false: Do we want to model message type 10?
        :param type11:      true/false: Do we want to model message type 11?
        :param typeCc:      true/false: Do we want to model clock correction data?
        :param typeIono:    true/false: Do we want to model Iono data?
        :param typeRa:      true/false: Do we want to model Reduced Almanac?
        :param typeMa:      true/false: Do we want to model Midi Almanac?
        :param typeEop:     true/false: Do we want to model EOP data?
        :param typeUtc:     true/false: Do we want to model UTC data?
        :param typeDc:      true/false: Do we want to model Dc data?
        :param typeGgto:    true/false: Do we want to model Ggto data?
        :return: depending on the model we want to construct, evaluate the total amount of time necessary to
        '''
        interval = 0
        if type10 or type11 or typeCc:
            interval = 4
        if typeIono or typeGgto or typeUtc:
            interval = 24
        if typeRa:
            interval = 100
        if typeEop or typeDc:
            interval = 150
        if typeMa:
            interval = 600
        return interval