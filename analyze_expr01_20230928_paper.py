from myutils3_v2 import *
from expr01_defs import *

prefix = './res-20230928/'
RRR='R1_lambda_1'
totaltime='/T100000'
fNameDict = OrderedDict([
    ('LowPopArt'    , RRR+'/'+totaltime+'/LowPopArt.pkl'),
    ('LowESTR'    , RRR+'/'+totaltime+'/LowESTR.pkl'),
    ('bmoracle'                 , RRR+'/'+totaltime+'/bmoracle.pkl'),
    ('bltwostage-sp_simple2'    , RRR+totaltime+'/bltwostage-sp_simple2.pkl'),
    ('bloful'                   , RRR+totaltime+'/bloful.pkl'),
 #   ('bltwostage-bm-sp_simple2' , RRR+'/'+totaltime+'/bltwostage-bm-sp_simple2.pkl'),
])
algoNameList = list(fNameDict.keys())

argBestMeanList = []
argBestMDList = []
plotDataMean = []
plotDataMD = []
plotDataNT = []
crbestUcbList = []
for algoName in algoNameList:
    fName = fNameDict[algoName]
    print ('\n### %s' % fName)
    out = LoadPickle(prefix + fName)
    res = out.res
    opts = out.opts
    tAry = res.tAry
    params = out.paramList

    printExpr('opts')

    cr = np.array(res.cum_regrets) # (tryIdx, paramIdx, t)
    cr_end = cr[:,:,-1]    # (tryIdx, paramIdx)
    me = cr_end.mean(0)    
    dev = getDeviationMat(cr_end.T)
#    printParamList(params, [('%.3g(%.1g)' % tuple(v)) for v in zip(me,dev)])

    printExpr('params[0]._fields')
    print('mean(dev): ',end='')
    for (i,v) in enumerate(zip(me,dev)):
        ss = ''
        for k in params[i]:
            ss += '%.2g, '% k
        print('%-12s: %.3g(%.2g)' % ((ss[:-2],) + tuple(v)) )
    print('mean+dev: ' + str(me+dev))

    argBestMean = np.argmin(me)
    argBestMeanList.append( argBestMean )
    print('best mean    : idx=%d, %g(%g)' % (argBestMean, me[argBestMean], dev[argBestMean]))

    argBestMD = np.argmin(me+dev)
    argBestMDList.append( argBestMD )
    print('best mean+dev: idx=%d, %g(%g)' % (argBestMD, me[argBestMD], dev[argBestMD]) )

    tm = np.array(res.times)
    print ('time: (mean, min, max) = (%g,%g,%g)' % (tm.mean(), tm.min(), tm.max()))
    tm_best = tm[:,argBestMD]
    print ('time of argBestMD: (mean, min, max) = (%g,%g,%g)' % (tm_best.mean(), tm_best.min(), tm_best.max()))

    #-----------------------------------------------UC
    #- plot...
    title = prefix + '; Tune by mean'
    crbest = cr[:,argBestMean,:] # [tryIdx, T] 
    me,err = getErrorBarMat(crbest.T)
    plotDataMean.append( (me,err,params[argBestMean],title) )

    #- plot...
    # title = prefix + '; Tune by UCB'
    title = ''
    crbest = cr[:,argBestMD,:] # [tryIdx, T] 
    me,err = getErrorBarMat(crbest.T)
    plotDataMD.append( (me,err,params[argBestMD],title) )
    crbestUcbList.append( crbest[:,-1] )

    pass

import matplotlib
import matplotlib.pyplot as plt
plt.ion()
plt.close("all")
matplotlib.rcParams.update({'font.size': 12})

algoNameList
conversion = {
    'bloful': 'OFUL',
    'bltwostage-sp_simple2': 'ESTR',   
    'LowPopArt'    :'LPA-ESTR (ours)',
    'LowESTR'    :'LowESTR',
  #  'bltwostage-bm-sp_simple2': 'ESTR-BM',
    'bmoracle': 'rO-UCB',
}
algoNameListNew = [ conversion[name] for name in algoNameList ]

#colorList = ['red', 'green', 'blue', 'black', 'cyan', 'magenta', 'yellow']
colorList = ['blue','black', 'red', 'green', 'orange']
#
for (k, plotdata) in enumerate([plotDataMean, plotDataMD]):
    if k == 0: 
        continue

    fig = plt.figure(k)
    nameList = []
    for (i,v) in enumerate(plotdata):
        me, err, param, title = v
        color = colorList[i]
        #tAry = np.arange(1,len(me)+1)
        plt.plot(tAry, me, color=color, alpha=0.7, linewidth=2, label=algoNameListNew[i])
        plt.fill_between(tAry, me-err, me+err, color=color, alpha=0.20)
#        nameList.append( algoNameList[i] + '[%s]'%param.shortstr() )
        nameList.append( algoNameListNew[i] )
    plt.legend(loc='upper left', fontsize=15, framealpha=0.10)
    #plt.title(title)
    plt.xlabel('Time step', fontsize=15)
    plt.ylabel('Cumulative regret', fontsize=15)
    
    #-  adjust axis
    aa = list(plt.axis())
    aa[2] = 0
    plt.axis(aa)

    fig.savefig(prefix+RRR+totaltime+"/AISTATS231016.png", bbox_inches='tight')




#--- extra
print('\n##- testing significance between %s and %s'%(algoNameList[0], algoNameList[1]))
printExpr('evalTestSignificance( crbestUcbList[0], crbestUcbList[1] )')
