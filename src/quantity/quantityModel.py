__author__ = 'torrho'
from CnavDataModel import CnavDataModel
from L2MessageBroadcastIntervals import L2MessageBroadcastIntervals


if __name__ == '__main__':
    l2cInterval = L2MessageBroadcastIntervals(31)
    print '15,36 message optimized'
    cnav = CnavDataModel(l2cInterval,None,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False)
    cnav.Solve()
    cnav.GetResults()
    print '15,36 bit optimized'
    cnav = CnavDataModel(l2cInterval,None,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)
    cnav.Solve()
    cnav.GetResults()
    print '15 optimized'
    cnav = CnavDataModel(l2cInterval,None,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False)
    cnav.Solve()
    cnav.GetResults()
    print '36 optimized'
    cnav = CnavDataModel(l2cInterval,None,True,True,True,True,True,True,True,True,True,True,True,True,True,False,True,False)
    cnav.Solve()
    cnav.GetResults()