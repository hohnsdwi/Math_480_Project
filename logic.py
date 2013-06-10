r"""
Logic

Manipulation of symbolic logic expressions.

An expression is created from a string that consists of the
operators ``!``, ``&``, ``|``, ``->``, ``<->``, which
correspond to the logical functions ``not``, ``and``, ``or``,
``if then``, ``if and only if``, respectively. Variable names
must start with a letter and contain only alpha-numerics and
the underscore character.

AUTHORS:

- Chris Gorecki (2007): initial version
- William Stein (2007-08-31): integration into SAGE-2.8.4
"""

#*****************************************************************************
# Copyright (C) 2006 William Stein <wstein@gmail.com>
# Copyright (C) 2007 Chris Gorecki <chris.k.gorecki@gmail.com>
#
# Distributed under the terms of the GNU General Public License (GPL)
# http://www.gnu.org/licenses/
#*****************************************************************************

import string

#constants
tok_list = ['OPAREN', 'CPAREN', 'AND', 'OR', 'NOT', 'IFTHEN', 'IFF']
bin_list = ['AND', 'OR', 'IFTHEN', 'IFF']
operators = '()&|!<->'
#variables
vars = {}
vars_order = []

class SymbolicLogic:
        """
        EXAMPLES::
        
            sage: log = SymbolicLogic()
            sage: s = log.statement("a&b|!(c|a)")
            sage: t = log.truthtable(s)
            sage: log.print_table(t)
            a     | b     | c     | value |
            --------------------------------
            False | False | False | True  |
            False | False | True  | False |
            False | True  | False | True  |
            False | True  | True  | False |
            True  | False | False | False |
            True  | False | True  | False |
            True  | True  | False | True  |
            True  | True  | True  | True  |
        """
    def statement(self, s):
        r"""
        This function returns a token list to be further manipulated
        by other functions in the class.
        
        INPUT:
        
        - ``self`` -- the calling object.
        - ``s`` -- a string containing the logic expression to be manipulated.
        - ``global vars`` -- a dictionary with the variable names and their current boolean value.
        - ``global vars_order`` -- a list of the variable names in the order they were found.
        
        OUTPUT:
        
        Returns a list containing the following:
        
        1. A list of tokens
        2. A dictionary of varaiable/value pairs (where the value is 'True' or 'False')
        3. List of the variable names in the order they were found
        
        EXAMPLES:
        
        This example illustrates the creation of a statement.
        
        ::
        
            sage: log = SymbolicLogic()
            sage: s = log.statement("a&b|!(c|a)")
        
        We can now create another statement.
        
        ::
        
            sage: s2 = log.statement("!((!(a&b)))")
        
        It is an error to use invalid variable names.
		
		::
        
            sage: s = log.statement("3fe & @q")
            Invalid variable name:  3fe
            Invalid variable name:  @q
        
        It is an error to use invalid syntax.
		
		::
        
            sage: s = log.statement("a&&b")
            Malformed Statement
            sage: s = log.statement("a&((b)")
            Malformed Statement
        """
        global vars, vars_order
        toks, vars, vars_order = ['OPAREN'], {}, []
        tokenize(s, toks)
        statement = [toks, vars, vars_order]
        try:                           #verify the syntax
            eval(toks)
        except(KeyError, RuntimeError):
            print 'Malformed Statement'
            return []
        return statement
    
    def truthtable(self, statement, start=0, end=-1):
        r"""
        This function returns a truthtable corresponding to
        the given statement.
        
        INPUT:
        
        - ``self`` -- the calling object: not used.
        - ``statement`` -- a list of 3 items, the tokens and two global
          variables vars and vars_order.
        - ``start`` -- an integer representing the row of the truth
          table from which to start initialized to 0 which
          is the first row when all the variables are
          false.
        - ``end`` -- an integer representing the last row of the
          truthtable to be created initialized to -1 which
          if left is converted to the last row of the
          full table.
        - ``global vars`` -- a dictionary with the variable names and
          their current boolean value.
        - ``global vars_order`` -- a list of the variable names in
          the order they were found.
        
        OUTPUT:
        
        - Returns the truthtable (a 2-d array with the creating statement
          tacked on the front) corresponding to the statement.
        
        EXAMPLES:
        
        This example illustrates the creation of a statement.
        
        ::
        
            sage: log = SymbolicLogic()
            sage: s = log.statement("a&b|!(c|a)")
            sage: t = log.truthtable(s) #creates the whole truth table
        
        We can now create truthtable of rows 1 to 5.
        
        ::
        
            sage: s2 = log.truthtable(s, 1, 5); s2
            [[['OPAREN', 'a', 'AND', 'b', 'OR', 'NOT', 'OPAREN', 'c', 'OR', 'a', 'CPAREN', 'CPAREN'], {'a': 'False', 'c': 'True', 'b': 'False'}, ['a', 'b', 'c']], ['False', 'False', 'True', 'False'], ['False', 'True', 'False', 'True'], ['False', 'True', 'True', 'True'], ['True', 'False', 'False', 'False']]
        
        
        There should be no errors if the statement did not return
        any errors.
        
        .. NOTE::
        
    	When sent with no start or end parameters this is an
	    exponential time function requiring `O(2^n)` time, where
	    `n` is the number of variables in the logic expression.
        """
        global vars, vars_order
        toks, vars, vars_order = statement
        if(end == -1):
            end = 2 ** len(vars)
        table = [statement]
        keys = vars_order
        keys.reverse()
        for i in range(start,end):
            j = 0
            row = []
            for key in keys:
                bit = get_bit(i, j)
                vars[key] = bit
                j += 1
                row.insert(0, bit)
            row.append(eval(toks))
            table.append(row)
        return table

    def print_table(self, table):
        r"""
        This function returns a truthtable corresponding to
        the given statement.
        
        INPUT:
        
        - ``self`` -- the calling object: not used.
        - ``table`` -- an object created by :meth:`truthtable`
          that contains variable values and the
          corresponding evaluation of the statement.
        - ``global vars_order`` -- a list of the variable names in
          the order they were found.
        
        OUTPUT:
        
        - Prints to the terminal window a formatted version of
          the truthtable (which is basically a 2-d array).
        
        EXAMPLES:
        
        This example illustrates the creation of a statement.
        
        ::
        
            sage: log = SymbolicLogic()
            sage: s = log.statement("a&b|!(c|a)")
            sage: t = log.truthtable(s) #creates the whole truth table
            sage: log.print_table(t)
            a     | b     | c     | value |
            --------------------------------
            False | False | False | True  |
            False | False | True  | False |
            False | True  | False | True  |
            False | True  | True  | False |
            True  | False | False | False |
            True  | False | True  | False |
            True  | True  | False | True  |
            True  | True  | True  | True  |
        
        We can also print a shortened table.
        
        ::
        
            sage: t = log.truthtable(s, 1, 5)
            sage: log.print_table(t)
            a     | b     | c     | value | value |
            ----------------------------------------
            False | False | False | True  | True  |
            False | False | True  | False | False |
            False | False | True  | True  | False |
            False | True  | False | False | True  |
        
        There should be no errors if the statement did not return
        any errors.
        """
        statement = table[0]
        del table[0]
        vars_order = statement[2]
        vars_len = []
        line = s = ""
        vars_order.reverse()
        vars_order.append('value')
        for var in vars_order:
            vars_len.append(len(var))
            s = var + ' '
            while(len(s) < len('False ')):
                s += ' '
            s += '| '
            line += s
        print line
        print len(line) * '-'
        for row in table:
            line = s = ""
            i = 0
            for e in row:
                if e == 'True':
                    j = 2
                else:
                    j = 1
                s = e + ' ' * j
                if(i < len(vars_len)):
                    while(len(s) <= vars_len[i]):
                        s += ' '
                s += '| '
                line += s
                i += 1
            print line
        print
    
    def combine(self, statement1, statement2):
        r"""
        This function takes ``statement1`` and ``statement2`` and returns
        a new statement that combines each input seperated by the operator
        'OR'
        
        INPUT:
        
        - ``self`` -- The calling object
        - ``statement1`` -- A logical expression, either a string or a 
          statement object from calling SymbolicLogic().statement("")
        - ``statement2`` -- A logical expression, either a string or a
          statement object from calling SymbolicLogic().statement("")
        
        OUTPUT: 
        
        - Returns a new ``statement`` object whose expression is
          ``statement1`` and ``statement2`` combined using the operator 'OR'
        
        EXAMPLES:
        
        This example illustrates the combination of two statement objects.
        
        ::
        
            sage: log=SymbolicLogic()
            sage: s=log.statement("a&b")
            sage: d=log.statement("c&d")
            sage: f=log.combine(s,d)
            sage: f
            [['OPAREN',
              'OPAREN',
              'a',
              'AND',
              'b',
              'CPAREN',
              'OR',
              'OPAREN',
              'c',
              'AND',
              'd',
              'CPAREN',
              'CPAREN'],
            {'a': 'False', 'b': 'False', 'c': 'False', 'd': 'False'},
            ['a', 'b', 'c', 'd']]
        
        We can also use a mix of strings and statement objects.
        
        ::
        
            sage: log=SymbolicLogic()
            sage: s=log.statement("a&b")
            sage: f=log.combine(s,"c&d")
            sage: f
            [['OPAREN',
            'OPAREN',
            'a',
            'AND',
            'b',
            'CPAREN',
            'OR',
            'OPAREN',
            'c',
            'AND',
            'd',
            'CPAREN',
            'CPAREN'],
            {'a': 'False', 'b': 'False', 'c': 'False', 'd': 'False'},
            ['a', 'b', 'c', 'd']]
        """
        x = statement1
        y = statement2
        if(type(x) == list and type(y) == list and len(x) == 3 and len(y) == 3):
            statement3=[['OPAREN'],x[1],x[2]]
            for i in range(len(x[0])):
                statement3[0].append(x[0][i])
            #statement3[0].append('CPAREN')
            statement3[0].append('OR')
            #statement3[0].append('OPAREN')
            for i in range(len(y[0])):
                statement3[0].append(y[0][i])
            #statement3[0].append('CPAREN')
            statement3[0].append('CPAREN')
            for key in y[1]:
                statement3[1][key]=y[1][key]
            for i in range(len(y[2])):
                statement3[2].append(y[2][i])
            statement3[2]=sorted(list(set(statement3[2])))
            return statement3
        elif(type(x) == str and type(y) == str):
            z="("+ x + ")|(" + y + ")"
            return self.statement(z)
        elif(type(x) == list and type(y) == str and len(x) == 3):
            y=self.statement(y)
            return self.combine(x,y)
        elif(type(y) == list and type(x) == str and len(y) == 3):
            x=self.statement(x)
            return self.combine(x,y)
        else:
            raise TypeError('Malformed Inputs, combine accepts only strings and statement objects')
    def simplify(self, table):
		r"""
        .. TODO::
		
			implement the simplify function which calls
			a c++ implementation of the ESPRESSO algorithm
			to simplify the truthtable: probably Minilog
        """
    
    def prove(self, statement):
		r"""
        .. TODO::
        
			implement a prove function which test to
    		see if the statement is a tautology or contradiction
    		by calling a c++ library TBD
        """

def get_bit(x, c):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns bit ``c`` of the number ``x``.
    
    INPUT:
    
    - ``x`` -- An integer, the number from which to take the bit.
    - ``c`` -- An integer, the bit number to be taken, where 0 is
      the low order bit.
    
    OUTPUT:
    
	- Returns ``True`` if bit ``c`` of number ``x`` is ``1``, ``False``
      otherwise.
    
    EXAMPLES::
    
    sage: sage.logic.logic.get_bit(0,0)
    False
    """
    bits = []
    while(x > 0):
        if(x % 2 == 0):
            b = 'False'
        else:
            b = 'True'
        x /= 2
        bits.append(b)
    if(c > len(bits) - 1):
        return 'False'
    else:
        return bits[c]

def eval(toks):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns ``True`` if the expression contained in toks would
    evaluate to ``True`` and ``False`` otherwise.  It relies on
	setting the values of the variables in the global dictionary vars.
    
    INPUT:
    
    - ``toks`` -- a token list representing a logic expression.
    
    OUTPUT:
	
	- Returns ``True`` if evaluates to ``True`` with variables
      in vars and ``False`` otherwise.
    
    EXAMPLES::
    
        sage: a=true
        sage: b=false
        sage: c=true
        sage: d=true
        sage: eval("(a&b)|(c&d)")
        True
    """
    stack = []
    for tok in toks:
        stack.append(tok)
        if(tok == 'CPAREN'):
            lrtoks = []
            while(tok != 'OPAREN'):
                tok = stack.pop()
                lrtoks.insert(0, tok)
            stack.append(eval_ltor_toks(lrtoks[1:-1]))
    if(len(stack) > 1):
        raise RuntimeError
    return stack[0]

def eval_ltor_toks(lrtoks):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns ``True`` if the expression contained in lrtoks would
    evaluate to ``True`` and ``False`` otherwise.  It relies on setting
    the values of the variables in the global dictionary vars.
    
    INPUT:
    
    - ``lrtoks`` -- a token list representing part of a logical
      expression that contains no inner parentheses.
    
    OUTPUT:
    
	- Returns ``True`` if evaluates to ``True`` with variables
      in vars and ``False`` otherwise.
    
    EXAMPLES::
    
        sage: a=true
        sage: b=false
        sage: c=true
        sage: d=true
        sage: log=SymbolicLogic()
        sage: s=log.statement("a&b&c&d")
        sage: eval("(a&b)|(c&d)")
        sage: g=[]
        sage: for i in range (len(s[0])-1):
        sage: 	if i != 0:
        sage: 		g.append(s[0][i])
        sage: sage.logic.logic.eval_ltor_toks(g)
        'False'
    """
    reduce_monos(lrtoks)        #monotonic ``!`` operators go first
    reduce_bins(lrtoks)         #then the binary operators
    if(len(lrtoks) > 1):
        raise RuntimeError
    return lrtoks[0]

def reduce_bins(lrtoks):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It takes a series of tokens with no parentheses or monotonic
    operators and evaluates it to a single boolean value.
    
    INPUT:
    
    - ``lrtoks`` -- a token list representing part of a logical
      expression that contains no inner parentheses or
      monotonic operators.
    
    OUTPUT:
    
	- The pointer to lrtoks is now a list containing ``True`` or
      ``False``.
	
    EXAMPLES::
    
        sage: g=['True','AND','False']
        sage: sage.logic.logic.reduce_bins(g)
        sage: g
        ['False']
    """
    i = 0
    while(i < len(lrtoks)):
        if(lrtoks[i] in bin_list):
            args = [lrtoks[i - 1], lrtoks[i], lrtoks[i + 1]]
            lrtoks[i - 1] = eval_bin_op(args)
            del lrtoks[i]
            del lrtoks[i]
            reduce_bins(lrtoks)
        i += 1

def reduce_monos(lrtoks):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It takes a series of tokens with no parentheses and replaces
    the monotonic operator/variable pairs with a boolean value.
    
    INPUT:
    
    - ``lrtoks`` -- a token list representing part of a logical
      expression that contains no inner parentheses.
    
    OUTPUT:
    
	- The pointer to ``lrtoks`` is now a list containing no monotonic
      operators.
	
    EXAMPLES::
    
        sage: b='True'
        sage: g=['NOT',b]
        sage: sage.logic.logic.reduce_monos(g)
        sage: g
        ['False']
    """
    i = 0
    while(i < len(lrtoks)):
        if(lrtoks[i] == 'NOT'):
            args = [lrtoks[i], lrtoks[i + 1]]
            lrtoks[i] = eval_mon_op(args)
            del lrtoks[i + 1]
        i += 1

def eval_mon_op(args):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns a boolean value based on the truthtable of
    the operator sent to it.
    
    INPUT:
    
    - ``args`` -- a list of length 2 containing the token 'NOT' and
      then a variable name.
    - ``global vars`` -- a dictionary with the variable names and
      their current boolean value.
    
    OUTPUT:
    
	- Returns the inverse of the boolean value represented by the
	  variable.
	
    EXAMPLES::
    
        sage: a=false
        sage: sage.logic.logic.eval_mon_op(['NOT','a'])
        'True'
    """
    if(args[1] != 'True' and args[1] != 'False'):
        val = vars[args[1]]
    else:
        val = args[1]

    if(val == 'True'):
        return 'False'
    else:
        return 'True'

def eval_bin_op(args):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns a boolean value based on the truthtable of
    the operator sent to it.
    
    INPUT:
    
    - ``args`` -- a list of length 3 to containing a variable name
      then a token representing a binary logical operator
      then another variable name.
    - ``global vars`` -- a dictionary with the variable names and
      their current boolean value.
    
    OUTPUT:
    
	- Returns the boolean evaluation of the operator based on
      the values of the variables.
    
    EXAMPLES::
    
        sage: a=false
        sage: b=true
        sage: sage.logic.logic.eval_bin_op(['a','AND','b'])
        'False'
    """
    if(args[0] == 'False'):
        lval = 'False'
    elif(args[0] == 'True'):
        lval = 'True'
    else:
        lval = vars[args[0]]

    if(args[2] == 'False'):
        rval = 'False'
    elif(args[2] == 'True'):
        rval = 'True'
    else:
        rval = vars[args[2]]

    if(args[1] == 'AND'):
        return eval_and_op(lval, rval)
    elif(args[1] == 'OR'):
        return eval_or_op(lval, rval)
    elif(args[1] == 'IFTHEN'):
        return eval_ifthen_op(lval, rval)
    elif(args[1] == 'IFF'):
        return eval_iff_op(lval, rval)

def eval_and_op(lval, rval):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns the logical ``and`` operator applied to lval and rval.
    
    INPUT:
    
    - ``lval`` -- the variable name appearing to the left of the
      ``and`` operator.
    - ``rval`` -- the variable name appearing to the right of the
      ``and`` operator.
    
    OUTPUT:
    
	- Returns the logical ``and`` operator applied to ``lval`` and ``rval``.
    
    EXAMPLES::
    
        sage: sage.logic.logic.eval_and_op('True', 'True')
        'True'
    """
    if(lval == 'False' and rval == 'False'):
        return 'False'
    elif(lval == 'False' and rval == 'True'):
        return 'False'
    elif(lval == 'True' and rval == 'False'):
        return 'False'
    elif(lval == 'True' and rval == 'True'):
        return 'True'

def eval_or_op(lval, rval):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns the logical ``or`` operator applied to lval and rval.
    
    INPUT:
    
    - ``lval`` -- the variable name appearing to the left of the
      ``or`` operator.
    - ``rval`` -- the variable name appearing to the right of the
      ``or`` operator.
    
    OUTPUT:
    
	- Returns the logical ``or`` operator applied to ``lval`` and ``rval``.
	
    EXAMPLES::
    
        sage: sage.logic.logic.eval_or_op('False', 'True')
        'True'
    """
    if(lval == 'False' and rval == 'False'):
        return 'False'
    elif(lval == 'False' and rval == 'True'):
        return 'True'
    elif(lval == 'True' and rval == 'False'):
        return 'True'
    elif(lval == 'True' and rval == 'True'):
        return 'True'

def eval_ifthen_op(lval, rval):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns the logical ``if then`` operator applied to lval and rval.
    
    INPUT:
    
    - ``lval`` -- the variable name appearing to the left of the
      ``if then`` operator.
    - ``rval`` -- the variable name appearing to the right of the
      ``if then`` operator.
    
    OUTPUT:
    
	- Returns the logical ``if then`` operator applied to ``lval`` and ``rval``.
	
    EXAMPLES::
    
        sage: sage.logic.logic.eval_ifthen_op('True', 'False')
        'False'
    """
    if(lval == 'False' and rval == 'False'):
        return 'True'
    elif(lval == 'False' and rval == 'True'):
        return 'True'
    elif(lval == 'True' and rval == 'False'):
        return 'False'
    elif(lval == 'True' and rval == 'True'):
        return 'True'

def eval_iff_op(lval, rval):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It returns the logical ``if and only if`` operator applied to
	lval and rval.
    
    INPUT:
    
    - ``lval`` -- the variable name appearing to the left of the
      ``if and only if`` operator.
    - ``rval`` -- the variable name appearing to the right of the
      ``if and only if`` operator.
    
    OUTPUT:
    
	- Returns the logical ``if and only if`` operator applied to
      ``lval`` and ``rval``.
    
    EXAMPLES::
    
        sage: sage.logic.logic.eval_iff_op('False', 'False')
        'True'
    """
    if(lval == 'False' and rval == 'False'):
        return 'True'
    elif(lval == 'False' and rval == 'True'):
        return 'False'
    elif(lval == 'True' and rval == 'False'):
        return 'False'
    elif(lval == 'True' and rval == 'True'):
        return 'True'

def tokenize(s, toks):
    r"""
    This function is for internal use by :class:`SymbolicLogic`.
    It tokenizes the string s and places the tokens in toks.
    
    INPUT:
    
    - ``s`` -- a string that contains a logical expression.
    - ``toks`` -- a list to contain the tokens of s.
    - ``global vars`` -- a dictionary with the variable names and
      their current boolean value.
    - ``global vars_order`` -- a list of the variable names in
      the order they were found.
    
    OUTPUT:
    
	- The tokens are placed in ``toks``.
	
    EXAMPLES::
    
        sage: g="(a&b)|(!c)"
        sage: toks=['OPAREN']
        sage: sage.logic.logic.tokenize(g, toks)
        sage: toks
        ['OPAREN', 'OPAREN', 'a', 'AND', 'b', 'CPAREN', 'OR', 'OPAREN', 'NOT', 'c', 'CPAREN', 'CPAREN']
    """
    i = 0
    while(i < len(s)):
        tok = ""
        skip = valid = 1
        if(s[i] == '('):
            tok = tok_list[0]
        elif(s[i] == ')'):
            tok = tok_list[1]
        elif(s[i] == '&'):
            tok = tok_list[2]
        elif(s[i] == '|'):
            tok = tok_list[3]
        elif(s[i] == '!'):
            tok = tok_list[4]
        elif(s[i:i + 2] == '->'):
            tok = tok_list[5]
            skip = 2
        elif(s[i:i + 3] == '<->'):
            tok = tok_list[6]
            skip = 3
        
        if(len(tok) > 0):
            toks.append(tok)
            i += skip
            continue
        else:
            #token is a variable name
            if(s[i] == ' '):
                i += 1
                continue
            
            while(i < len(s) and s[i] not in operators and s[i] != ' '):
                tok += s[i]
                i += 1
            
            if(len(tok) > 0):
                if(tok[0] not in string.letters):
                    valid = 0
                for c in tok:
                    if(c not in string.letters and c not in string.digits 
                       and c != '_'):
                        valid = 0
            
            if(valid == 1):
                toks.append(tok)
                vars[tok] = 'False'
                if(tok not in vars_order):
                    vars_order.append(tok)
            else:
                print 'Invalid variable name: ', tok
                toks = []
    
    toks.append('CPAREN')
