def tokenize(s):
    r = s.replace("(", " ( ").replace(")", " ) ").split()
    return r

def atom(token):
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return Symbol(token)

def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF")
    c = tokens.pop(0)
    if c == '(':
        A = []
        while tokens[0] != ')':
            A.append(read_from_tokens(tokens))
        tokens.pop(0)
        return A
    elif c == ')':
        raise SyntaxError("Unexpected )")
    else:
        return atom(c)

def atom(token):
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return Symbol(token)

def standard_env():
    "An environment with some Scheme standard procedures."
    import math, operator as op
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.div, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

Symbol = str
List = list
Number = (int, float)
Env = dict
global_env = standard_env()

def eval(exp, env=global_env):
    if isinstance(exp, Symbol):
        return env.find(exp)[exp]
    elif not isinstance(exp, List):
        return exp
    elif exp[0] == 'quote':
        return exp[1]
    elif exp[0] == 'if':
        (_, test, conseq, alt) = exp
        if eval(test, env):
            return eval(conseq, env)
        else:
            return eval(alt, env)
    elif exp[0] == 'define':
        (_, v, e) = exp
        env[v] = eval(e, env)
    else:
        procedure = eval(exp[0], env)
        args = [eval(arg, env) for arg in exp[1:]]
        return procedure(*args)
        
def parse(p): 
    return read_from_tokens(tokenize(p))

class Procedure(object):
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    
    def __call__(self, *args):
        return eval(self.body, Env(self.params, args, self.env)

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)

if __name__ == '__main__':
    print(eval(parse("( * (- (+ 3 5) 3) 9)")))

    
