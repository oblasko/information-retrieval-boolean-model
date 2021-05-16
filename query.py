from nltk.stem import *
from information_retrieval import InvertedIndex

op_precedence = {
    "NOT": 3,
    "AND": 2,
    "OR": 1,
    "(": -1,
    ")": -1
}

COLLECTION_SIZE = 18

class Evaluator:
    def __init__(self, num_of_docs):
        self.all_docs = [str(i) for i in list(range(num_of_docs))]
        self.in_index = InvertedIndex()
    
    def AND(self, left, right):
        """returning document ids that contains both left and right terms"""
        if (left and right):
            return left.intersection(right)
        return set()

    def OR(self, left, right):
        """returning document ids that contains one or two terms"""
        return left.union(right)

    def NOT(self, left):
        """returning all document ids in collection that doesn't contain given term"""
        res = set(self.all_docs).symmetric_difference(left)
        return res
    
    def parse_querry(self, user_query):
        """parses the user querry and returning the querry in the correct order of operators"""
        """Example: 1. ((A AND (NOT D))) OR NOT C -> ["A", "D", "NOT", "AND", "C", "NOT", "OR"]
                    2. A AND (D OR C) -> ["A", "D", "C", "OR", "AND"]"""
        ps = PorterStemmer()    
        parsed_q = []
        operators = []

        querry = user_query.replace("(", "( ").replace(")", " )").split(" ")

        for i in range(len(querry)):
            if querry[i].upper() in op_precedence:
                querry[i] = querry[i].upper()
            else:
                querry[i] = ps.stem(querry[i])

        for term in querry:
            #opening parenthesis
            if term == "(":
                operators.append(term)
            #closing parenthesis
            elif term == ")":
                current_operator = operators.pop()
                #we need to output all operators that were present in the parenthesis first
                while current_operator != "(":
                    parsed_q.append(current_operator)
                    current_operator = operators.pop()
            
            #some operator other than parenthesis found
            elif term in op_precedence:
                #there are still some operators left that could have higher precedence
                if operators:
                    #last pushed operator
                    current_operator = operators[-1]
                    while operators and op_precedence[current_operator] > op_precedence[term]:
                        #output operator with higher precedence first
                        parsed_q.append(operators.pop())
                        if operators:
                            current_operator = operators[-1]
                
                operators.append(term)
            #normal term
            else:
                parsed_q.append(term)
        
        #add remaining operators
        while operators:
            parsed_q.append(operators.pop())
        
        return parsed_q

    def evalute_querry(self, user_query):
        parsed_querry = self.parse_querry(user_query)
        evaluation = []

        for term in parsed_querry:
            #operator handling
            if term == "AND":
                """presence of the elements is guaranteed due to the postfix parsing"""
                left = evaluation.pop()
                right = evaluation.pop()
                evaluation.append(self.AND(left, right))
            
            elif term == "OR":
                """presence of the elements is guaranteed due to the postfix parsing"""
                left = evaluation.pop()
                right = evaluation.pop()
                evaluation.append(self.OR(left, right))

            elif term == "NOT":
                """presence of the elements is guaranteed due to the postfix parsing"""
                left = evaluation.pop()
                evaluation.append(self.NOT(left))
            #term handling
            else:
                #transforms linked list of document ids into set
                if term in self.in_index.index:
                    term_in_docs = self.in_index.index.get(term).to_set()
                #term not found in any documment
                else:
                    term_in_docs = set()
                evaluation.append(term_in_docs)
        
        #final evaluation
        return evaluation.pop()
            
    def evaluate(self, user_query):
        """returns filenames of the documents in which the given querry is satisfied"""
        res = self.evalute_querry(user_query)
        res_filenames = []
        for r in res:
            res_filenames.append(self.in_index.collection_ids[r])
        return res_filenames


def test_evaluator():
    e1 = Evaluator(COLLECTION_SIZE)
    assert(e1.parse_querry("((A AND (NOT D))) OR NOT C") == ["A", "D", "NOT", "AND", "C", "NOT", "OR"])

    assert(e1.parse_querry("A OR D OR NOT C") == ['A', 'D', 'C', 'NOT', 'OR', 'OR'])

    assert(e1.parse_querry("A AND D OR C") == ["A", "D", "AND", "C", "OR"])

    assert(e1.parse_querry("A AND (D OR C)") == ["A", "D", "C", "OR", "AND"])

    assert(e1.parse_querry("A AND NOT A") == ["A", "A", "NOT", "AND"])

    assert(len(e1.evaluate("god")) == 16)
    assert(len(e1.evaluate("NOT god")) == 2)
    assert(len(e1.evaluate("Goddard AND god")) == 1)
    assert(len(e1.evaluate("Goddard AND NOT god")) == 0)
    assert(len(e1.evaluate("Exeunt")) == 4)
    assert(len(e1.evaluate("Exeunt AND jhfsdnfkjsndf" )) == 0)
    assert(len(e1.evaluate("Exeunt OR jhfsdnfkjsndf" )) == 4)
    assert(len(e1.evaluate("Exeunt AND NOT jhfsdnfkjsndf" )) == 4)
    assert(len(e1.evaluate("NOT jhfsdnfkjsndf" )) == 18)
    assert(len(e1.evaluate("Shakespeare" )) == 9)
    assert(len(e1.evaluate("(Goddard AND god) OR Exeunt")) == 5)
    assert(len(e1.evaluate("(Goddard AND god) OR NOT Exeunt")) == 14)
    assert(len(e1.evaluate("(Goddard AND god) AND NOT Exeunt")) == 1)
    assert(len(e1.evaluate("(Goddard AND god) AND Exeunt")) == 0)
    assert(e1.evaluate("gilbishwnajifnsajinfs") == [])
    


test_evaluator()
