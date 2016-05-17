from learning import Algo

a = Algo()

ret = a.permute_variables( [[0,0,0,0]], [ (1,(-.1,.1)), (2,(-2,1)) ] )

print 'test: ', str(ret)
print 'testlen: ',  str(len(ret))

ret = a.build_gradient(vars = [1,2])

print 'testlen: ',  str(len(ret))

ret = a.build_gradient(vars = [1,2], no_origin = True)

print 'test: ', str(ret)
print 'testlen: ',  str(len(ret))

ret = a.build_gradient(vars = [1,2,3,4], no_origin = True)

print 'testlen: ',  str(len(ret))

##TODO 5/17:
    #update x_gradient, y_gradient; Beta_gradient too?