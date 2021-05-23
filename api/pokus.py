q = "shakespear or"
import pyeda.boolalg.expr
import re

def val(querry):
    querry = re.sub(r"\bnot([( ])", r"~\1", querry.lower().strip())
    querry = re.sub(r" and ", r" & ", querry)
    querry = re.sub(r" or ", r" | ", querry)
    querry = re.sub(r"and ", r" & ", querry)
    querry = re.sub(r"or ", r" | ", querry)
    querry = re.sub(r" and", r" & ", querry)
    querry = re.sub(r" or", r" | ", querry)
    
    print(querry)
    querry.split()

    try:
        expr = pyeda.boolalg.expr.expr(querry)
        return True
    except pyeda.parsing.boolexpr.Error as error:
        return False

print(val(q))