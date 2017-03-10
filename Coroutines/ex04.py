import math
import operator

# Subgenerator for unary operators.
def parse_unary_operator(op):
    return op((yield from parse_argument((yield))))

# Subgenerator for binary operators.
def parse_binary_operator(op):
    values = []
    for i in (1, 2):
        values.append((yield from parse_argument((yield))))
    print(op(*values))
    return op(*values)

OPERATORS = {
    'sqrt': (parse_unary_operator, math.sqrt),
    '~': (parse_unary_operator, operator.invert),
    '+': (parse_binary_operator, operator.add),
    '-': (parse_binary_operator, operator.sub),
    '*': (parse_binary_operator, operator.mul),
    '/': (parse_binary_operator, operator.truediv)
}

# Detect whether argument is an operator or number - for
# operators we delegate to the appropriate subgenerator.
def parse_argument(token):
    subgen, op = OPERATORS.get(token, (None, None))
    if subgen is None:
        #return float(token)
        return int(token)
    else:
        return (yield from subgen(op))

# Parent generator - send() tokens into this.    
def parse_expression():
    result = None
    while True:
        token = (yield result)
        print(token, result)
        result = yield from parse_argument(token)


pe = parse_expression()
print(pe.send(None))
#print(pe.send('+'))
#print(pe.send(4))
#print(pe.send(3))
print(pe.send('~'))
print(pe.send('+'))
print(pe.send(4))
print(pe.send(3))
