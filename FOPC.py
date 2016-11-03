
# A statement is simply a list with the predicate at that head and tail consists of the 
# arguments that the predicate is applied to.
#
# e.g. ('clean', 'Cell 11')
#
# A pattern is the same thing, except in that a pattern might include variables 
# 
# In this instance, variables are just strings with a "?" as the first character.
#
# When a statement matches a pattern, it is within the context of a set of bindings.
#
#  e.g. when ('clean', 'Cell 11') matches ('clean', '?x") the result is 
#            ('?x': 'Cell 11')
#
#        when they don't match, the result is just False
#  
#  The bindings list can then be used to set the context of later matches

# Just test to see if something is a variable

def is_variable(x):
    return x[0] == "?"


# Match a statement by matching its elements where each match produces a potentially increasing
# set of bindings that are passed down to constrain the rest of the matches in the statement

def match(statement, pattern, bindings):
    for e,p in zip(statement,pattern):
        bindings = element_match(e, p, bindings)
        if bindings is False:
            return False
    return bindings
    
 
# Elements are matched in the contest of a set of existing bindings.  
# if the two elements match, then just return the current bindings
# if the pattern element is a variable, test to see if it is bound.
#       if it is bound, use the binding to see if there is a match
#       if it is not bound, bind it to the current statement element, add the binding to bindings list and return the 
#           expanded bindings list
    
def element_match(e, p, bindings):
    if e == p:
        return bindings
    elif is_variable(p):
        if bindings.get(p):
            p = bindings.get(p)
            return element_match(e,p,bindings)
        else:
            bindings[p] = e
            return bindings
    else:
        return False


# bind takes an element and binding list.  If the element is a variable that is bound, 
# it returns the element it is bound to.  Otherwise, it just hands back the element 
 
def bind(x, bindings):
    return bindings.get(x,x)


# instantiate takes a full statement and a bindings list.  it binds all variables in the 
# statement and returns it.   
    
def instantiate(statement, bindings):
    return map(lambda(x): bind(x, bindings), statement)      
    
    

    
        

            

