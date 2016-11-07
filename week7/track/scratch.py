
#TODO 11/6

    # FIX output fn increment has a bug?
    # FIX != None is not None
    # log timing
    # error handling within object funtions?
    
 
#   Even though I realise this is an old question, I'd like to suggest using the traceback module to handle output of the exceptions.
#Use traceback.print_exc() to print the current exception to standard error, just like it would be printed if it remained uncaught, or traceback.format_exc() to get the same output as a string. You can pass various arguments to either of those functions if you want to limit the output, or redirect the printing to a file-like object.

#Got VLC 2.2.4
    
    
    
a = None
if a != None:
    print 'hey'
    
if a is None:
    print 'ay'
    
if a is not None:
    print 'not'


def increment(x):
    if x > 10:
        pass
    return 1
        
for i in range(20):

    increment(i)
    print i
    
print 'done'
    
