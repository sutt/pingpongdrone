from learning import Algo

a = Algo()

ret = a.permute_variables( [[0,0,1,1]], [ (1,(-.1,.1)), (2,(-2,1)) ] )

print 'test: ', str(ret)