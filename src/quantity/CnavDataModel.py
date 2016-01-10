__author__ = 'torrho'

from sage.all import MixedIntegerLinearProgram
#from OptimizationGoal import OptimizationGoal
#from MessageTimingHelper import MessageTimingHelper
class CnavDataModel():
    '''
    This builds a list of linear constraints for CNAV messging by data subcomponent within messages:
    self.Type10Rate         = #First Ephemeris Messsage 10
    self.Type11Rate         = #Second Ephemeris Message 11
    self.TypeIonoRate       = #Iono/ISC Data on Message 30
    self.TypeRa12Rate       = #Reduced Almanac Data On Message 12
    self.TypeRa31Rate       = #Reduced Almanac Data on Message 31
    self.TypeMaRate         = #Midi Almanac Data on Message 37
    self.TypeEopRate        = #Eop Data on Message 32
    self.TypeUtcRate        = #Utc Data on Message 33
    self.TypeDc34Rate       = #Clock and Ephemeral Differential Correction Data on Message 34
    self.TypeDc13Rate       = #Clock Differential Correction Data on Message 13
    self.TypeDc14Rate       = #Ephemeral Differential Correction Data on Message 14
    self.TypeGgtoRate       = #GGTO Data on Message 35
    '''

    def __init__(self,broadcastInterval, milp, Type10Rate, Type11Rate, TypeCcRate, TypeIonoRate, TypeRa12Rate, TypeRa31Rate, TypeMaRate, TypeEopRate, TypeUtcRate, TypeDc34Rate, TypeDc13Rate, TypeDc14Rate,TypeGgtoRate, Type15, Type36, IsBitOptimization):
        '''
        :param broadcastInterval: Provide Modelling constraints w.r.t. timing
        :param milp: Mixed Integer Linear Programming object
        :param Type10Rate: The rate at which we broadcast message type 10
        :param Type11Rate: The rate at which we broadcast message type 11
        :param TypeCcRate: The rate at which we broadcast clock corrections on message type thirties
        :param TypeIonoRate: The rate at which we broadcast message type 30
        :param TypeRa12Rate: The rate at which we broadcast message type 12
        :param TypeRa31Rate: The rate at which we broadcast message type 31
        :param TypeMaRate: The rate at which we broadcast message type 37
        :param TypeEopRate: The rate at which we broadcast message type 32
        :param TypeUtcRate: The rate at which we broadcast message type 33
        :param TypeDc34Rate: The rate at which we broadcast message type 34
        :param TypeDc13Rate: The rate at which we broadcast message type 13
        :param TypeDc14Rate: The rate at which we broadcast message type 14
        :param TypeGgtoRate: The rate at which we broadcast message type 35
        :param Type15      : Do you want to maximize objective with type 15
        :param Type36      : Do you want to maximize objective with type 36
        :param IsBitOptimization: Do you want to maximize by bit optimization?  if not then maximize by message count
        :remark:  If the rates are 0, we assume that we do not broadcast that message.
        '''
        self.broadcastInterval = broadcastInterval
        #check if MixedIntegerLinearProgram
        # if type(milp) is type(MixedIntegerLinearProgram):
        #     self.milp = milp
        # else:
        self.milp = MixedIntegerLinearProgram()
        #create messaging variable
        self.msg = self.milp.new_variable(integer=True, nonnegative=True)
        #determine worst broadcasting interval requirement
        self.totalBroadcastInterval = self.DetermineTotalBroadcastIntervalTime(broadcastInterval, Type10Rate,
                                                                               Type11Rate, TypeCcRate, TypeIonoRate, TypeRa12Rate,
                                                                               TypeRa31Rate, TypeMaRate, TypeEopRate,
                                                                               TypeUtcRate, TypeDc34Rate, TypeDc13Rate,
                                                                               TypeDc14Rate, TypeGgtoRate)
        #check if OptimizationGoal
        self.IsBitOptimization = IsBitOptimization
        #set types
        self.type10Rate = Type10Rate
        self.type11Rate = Type11Rate
        self.typeCcRate = TypeCcRate
        self.typeIonoRate = TypeIonoRate
        self.typeRa12Rate = TypeRa12Rate
        self.typeRa31Rate = TypeRa31Rate
        self.typeMaRate = TypeMaRate
        self.typeEopRate = TypeEopRate
        self.typeUtcRate = TypeUtcRate
        self.typeDc34Rate = TypeDc34Rate
        self.typeDc13Rate = TypeDc13Rate
        self.typeDc14Rate = TypeDc14Rate
        self.typeGgtoRate = TypeGgtoRate
        self.type15 = Type15
        self.type36 = Type36
        #build linear constraints if called for it.
        if self.type10Rate:
            self.BuildType10()
        if self.type11Rate:
            self.BuildType11()
        if self.typeCcRate:
            self.BuildTypeCc()
        if self.typeIonoRate:
            self.BuildTypeIono()
        if self.typeRa12Rate or self.typeRa31Rate:
            self.BuildRaType()
        if self.typeMaRate:
            self.BuildMaType()
        if self.typeEopRate:
            self.BuildEopRate()
        if self.typeUtcRate:
            self.BuildUtcRate()
        if self.typeDc34Rate or self.typeDc13Rate or self.typeDc14Rate:
            self.BuildDcRate()
        if self.typeGgtoRate:
            self.BuildGgtoRate()
        self.BuildTotalMessagesConstraint()
        self.BuildOptimizationGoal()

    def BuildTotalMessagesConstraint(self):
        self.milp.add_constraint(self.msg[10]+self.msg[11]+self.msg[12]+self.msg[13]+self.msg[14]+self.msg[15]+self.msg[30]+self.msg[31]+self.msg[32]+self.msg[33]+self.msg[34]+self.msg[35]+self.msg[36]+self.msg[37]==self.totalBroadcastInterval)

    def DetermineTotalBroadcastIntervalTime(self,broadcastInterval, Type10Rate, Type11Rate, TypeCcRate, TypeIonoRate, TypeRa12Rate, TypeRa31Rate, TypeMaRate, TypeEopRate, TypeUtcRate, TypeDc34Rate, TypeDc13Rate, TypeDc14Rate, TypeGgtoRate):
        '''
        :param broadcastInterval: An object that inherits MessageBroadcastIntervals
        :param Type10Rate: The rate at which we broadcast message type 10
        :param Type11Rate: The rate at which we broadcast message type 11
        :param TypeIonoRate: The rate at which we broadcast message type 30
        :param TypeRa12Rate: The rate at which we broadcast message type 12
        :param TypeRa31Rate: The rate at which we broadcast message type 31
        :param TypeMaRate: The rate at which we broadcast message type 37
        :param TypeEopRate: The rate at which we broadcast message type 32
        :param TypeUtcRate: The rate at which we broadcast message type 33
        :param TypeDc34Rate: The rate at which we broadcast message type 34
        :param TypeDc13Rate: The rate at which we broadcast message type 13
        :param TypeDc14Rate: The rate at which we broadcast message type 14
        :param TypeGgtoRate: The rate at which we broadcast message type 35
        :return: The number of messages needed within a super frame
        '''
        interval = 0
        if Type10Rate > 0 or Type11Rate > 0 or TypeCcRate > 0:
            interval = 4
        if TypeIonoRate > 0 or TypeGgtoRate > 0 or TypeUtcRate > 0:
            interval = 24
        if TypeRa31Rate > 0 or TypeRa12Rate > 0:
            interval = 100
        if TypeEopRate > 0 or TypeDc34Rate > 0 or TypeDc13Rate > 0 or TypeDc14Rate > 0:
            interval = 150
        if TypeMaRate:
            interval = 600
        return interval
    
    def BuildType10(self):
        '''
        Builds the linear constraints for message type 10
        :return:
        '''
        self.milp.add_constraint(self.msg[10] >= self.totalBroadcastInterval/4)

    def BuildType11(self):
        '''
        
        :return:
        '''
        self.milp.add_constraint(self.msg[11] >= self.totalBroadcastInterval/4)
    def BuildTypeCc(self):
        '''
        
        :return:
        '''
        self.milp.add_constraint(self.msg[30]+self.msg[31]+self.msg[32]+self.msg[33]+self.msg[34]+self.msg[35]+self.msg[36]+self.msg[37] >= self.totalBroadcastInterval/4)
    def BuildTypeIono(self):
        '''
        
        :return:
        '''
        self.milp.add_constraint(self.msg[30] >= self.totalBroadcastInterval/25)
    def BuildRaType(self):
        '''
        type 12 has 7
        type 31 has 4
        Reduced Almanac


        The almanac parameters are provided in any one of message types 31, 37, and 12. Message type 37 provides Midi almanac parameters and the reduced almanac parameters are provided in either message type 31 or type 12. The SV shall broadcast both message types 31 (and/or 12) and 37. However, the reduced almanac parameters (i.e. message types 31 and/or 12) for the complete set of SVs in the constellation will be broadcast by a SV using shorter duration of time compared to the broadcast of the complete set of Midi almanac parameters (i.e. message type 37). The parameters are defined below, followed by material pertinent to the use of the data.

        :return:
        '''
        if self.typeRa12Rate and self.typeRa31Rate:
            self.milp.add_constraint(7*self.msg[12]+4*self.msg[31]>=self.broadcastInterval.SvCount*6)
        if self.typeRa12Rate and not self.typeRa31Rate:
            self.milp.add_constraint(7*self.msg[12]>=self.broadcastInterval.SvCount*6)
        if self.typeRa31Rate and not self.typeRa12Rate:
            self.milp.add_constraint(4*self.msg[31]>=self.broadcastInterval.SvCount*6)
    def BuildMaType(self):
        '''
        Midi Almanac

        The almanac parameters are provided in any one of message types 31, 37, and 12. Message type 37 provides Midi almanac parameters and the reduced almanac parameters are provided in either message type 31 or type 12. The SV shall broadcast both message types 31 (and/or 12) and 37. However, the reduced almanac parameters (i.e. message types 31 and/or 12) for the complete set of SVs in the constellation will be broadcast by a SV using shorter duration of time compared to the broadcast of the complete set of Midi almanac parameters (i.e. message type 37). The parameters are defined below, followed by material pertinent to the use of the data.

        :return:
        '''
        self.milp.add_constraint(self.msg[37]>=self.broadcastInterval.SvCount)
    def BuildEopRate(self):
        '''
        
        :return:
        '''
        self.milp.add_constraint(self.msg[32] >= 4)
    def BuildUtcRate(self):
        '''
        
        :return:
        '''
        self.milp.add_constraint(self.msg[33] >= self.totalBroadcastInterval/25)
    def BuildDcRate(self):
        '''
        Message type 34 provides SV clock correction parameters (ref. Section 30.3.3.2) and also, shall contain DC parameters that apply to the clock and ephemeris data transmitted by another SV. One message type 34, Figure 30-7, shall contain 34 bits of clock differential correction (CDC) parameters and 92 bits of ephemeris differential correction (EDC) parameters for one SV other than the transmitting SV. Bit 150 of message type 34 shall be a DC Data Type indicator that indicates the data type for which the DC parameters apply. Zero (0) signifies that the corrections apply to CNAV data, Dc(t), and one (1) signifies that the corrections apply to NAV data, D(t).
Message types 13 and 14 together also provide DC parameters. Message type 13, Figure 30-12, shall contain CDC parameters applicable to 6 SVs and message type 14, Figure 30-13, shall contain EDC parameters applicable to 2 SVs. There shall be a DC Data Type indicator preceding each CDC or EDC packet. The content of an individual data packet is depicted in Figure 30-16. The number of bits, scale factors (LSB), the range, and the units of all fields in the DC packet are given in Table 30-X.
        :return:
        '''
        if self.typeDc14Rate and self.typeDc13Rate and self.typeDc34Rate:
            self.milp.add_constraint(2*self.msg[14]+self.msg[34]>=(self.broadcastInterval.SvCount - 1)*4)
            self.milp.add_constraint(6*self.msg[13]+self.msg[34]>=(self.broadcastInterval.SvCount - 1)*4)
        if self.typeDc14Rate and self.typeDc13Rate and not self.typeDc34Rate:
            self.milp.add_constraint(2*self.msg[14]>=(self.broadcastInterval.SvCount - 1)*4)
            self.milp.add_constraint(6*self.msg[13]>=(self.broadcastInterval.SvCount - 1)*4)
        if self.typeDc14Rate and not self.typeDc13Rate and self.typeDc34Rate:
            self.milp.add_constraint(2*self.msg[14]+self.msg[34]>=(self.broadcastInterval.SvCount - 1)*4)
        if self.typeDc14Rate and not self.typeDc13Rate and not self.typeDc34Rate:
            self.milp.add_constraint(2*self.msg[14]>=(self.broadcastInterval.SvCount - 1)*4)
        if not self.typeDc14Rate and self.typeDc13Rate and self.typeDc34Rate:
            self.milp.add_constraint(6*self.msg[13]+self.msg[34]>=(self.broadcastInterval.SvCount - 1)*4)
        if not self.typeDc14Rate and self.typeDc13Rate and not self.typeDc34Rate:
            self.milp.add_constraint(6*self.msg[13]>=(self.broadcastInterval.SvCount - 1)*4)
        if not self.typeDc14Rate and not self.typeDc13Rate and self.typeDc34Rate:
            self.milp.add_constraint(self.msg[34]>=(self.broadcastInterval.SvCount - 1)*4)
        if not self.typeDc14Rate and not self.typeDc13Rate and not self.typeDc34Rate:
            return
    def BuildGgtoRate(self):
        '''
        
        :return:
        '''
        self.milp.add_constraint(self.msg[35] >= self.totalBroadcastInterval/25)
    def BuildOptimizationGoal(self):
        '''

        :return:
        '''
        if self.type15 and self.type36 and self.IsBitOptimization:
            self.milp.set_objective(149*self.msg[36] + 238*self.msg[15])
        if self.type15 and self.type36 and not self.IsBitOptimization:
            self.milp.set_objective(self.msg[36] + self.msg[15])
        if self.type15 and not self.type36 and self.IsBitOptimization:
            self.milp.set_objective(238*self.msg[15])
        if self.type15 and not self.type36 and not self.IsBitOptimization:
            self.milp.set_objective(self.msg[15])
        if not self.type15 and self.type36 and self.IsBitOptimization:
            self.milp.set_objective(149*self.msg[36])
        if not self.type15 and self.type36 and not self.IsBitOptimization:
            self.milp.set_objective(self.msg[36])
        if not self.type15 and not self.type36 and self.IsBitOptimization:
            raise Exception('Optimization Execption: need to specify an optimization goal')
        if not self.type15 and not self.type36 and not self.IsBitOptimization:
            raise Exception('Optimization Execption: need to specify an optimization goal')

    def Solve(self):
        print "solving..."
        self.milp.show()
        self.milp.solve()
        print "solved!"

    def GetResults(self):
        for msg in sorted(self.milp.get_values(self.msg)):
            print 'Message %s = %s' % (msg,int(round(self.milp.get_values(self.msg)[msg])))
