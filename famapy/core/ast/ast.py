import math
from termcolor import colored

'''
This algorithm obtains an abstract syntax tree from a text string.
Support for parentheses is included
'''

def main():

    try:

        ast1 = AST("(A implies (B requires C))")
        print(ast1)

        ast2 = AST(" (A and not B)")
        print(ast2)

        ast3 = AST("A and B or C")
        print(ast3)

        ast4 = AST("(A and B) or C")
        print(ast4)

        ast5 = AST("A")
        print(ast5)

        ast6 = AST("A implies B and C requires D")
        print(ast6)

        ast7 = AST("not A and B")
        print(ast7)

        ast8 = AST("not (A and B)")
        print(ast8)

        ast9 = AST("not (A and not B)")
        print(ast9)
        
        ast10 = AST("A implies (  B requires (  C excludes ( D ) ) )")
        print(ast10)

        ast11 = AST("(A implies B) and (C requires D)")
        print(ast11)

        ast12 = AST("A implies (B requires (C and D))")
        print(ast12)

        ast13 = AST("A implies (B requires (not not C and D))")
        print(ast13)

        ast14 = AST("(A and not B)")
        print(ast14)

        ast15 = AST("A or B and C")
        print(ast15)

    except Exception as e:
        print(type(e).__name__+"\n"+str(e))
    

    try:

        pass

    except Exception as e:
        print(str(e))
    

class ASTINFO():

    unary_operators = ["not"]
    binary_operators = ["or","and","implies","excludes","requires"]

    @staticmethod
    def get_unary_operators():
        return ASTINFO.unary_operators
    
    @staticmethod
    def set_unary_operators(list):
        ASTINFO.unary_operators = list

    @staticmethod
    def get_binary_operators():
        return ASTINFO.binary_operators
    
    @staticmethod
    def set_binary_operators(list):
       ASTINFO.binary_operators = list

    

class ASTCHECK():

    @staticmethod
    def check_all(string):

        ASTCHECK.check_is_empty(string)
        ASTCHECK.check_parentheses(string)
        ASTCHECK.check_empty_parentheses(string)
        ASTCHECK.check_binary_operator_at_start_or_end(string)
        ASTCHECK.check_unary_operator_at_end(string)
        ASTCHECK.check_adjacent_binary_operators(string)
        ASTCHECK.check_adjacent_unary_plus_binary_operators(string)
        ASTCHECK.check_adjacent_features(string)
        ASTCHECK.check_binary_operator_preceded_or_succeeded_by_parentheses(string)
        ASTCHECK.check_unary_operator_succeeded_by_parentheses(string)
        

    @staticmethod
    def check_is_empty(string):

        if not bool(string.strip()):
            raise ValueError(colored("ValueError: Empty string","red"))

    @staticmethod
    def check_parentheses(string):

        count_open_parentheses = ASTUtilities.count_characters(string,"(")
        count_close_parentheses = ASTUtilities.count_characters(string,")")

        if(count_open_parentheses != count_close_parentheses):
            raise SyntaxError(colored("SyntaxError: There is not the same number of open parentheses as closed ones","red"))

    @staticmethod
    def check_adjacent_binary_operators(string):

        string_list = ASTUtilities.string2list(string)

        for i in range(0,len(string_list)-1):

            fist_item = ASTUtilities.clean_parentheses(string_list[i])
            second_item = ASTUtilities.clean_parentheses(string_list[i+1])

            if(ASTUtilities.is_binary_operator(fist_item) and ASTUtilities.is_binary_operator(second_item)):
                raise SyntaxError(colored("There cannot be two adjacent binary operators:","red")+" "+colored(string_list[i],"yellow")+" "+colored(string_list[i+1],"yellow"))

    @staticmethod
    def check_adjacent_unary_plus_binary_operators(string):

        string_list = ASTUtilities.string2list(string)

        for i in range(0,len(string_list)-1):

            fist_item = ASTUtilities.clean_parentheses(string_list[i])
            second_item = ASTUtilities.clean_parentheses(string_list[i+1])

            if(ASTUtilities.is_unary_operator(fist_item) and ASTUtilities.is_binary_operator(second_item)):
                raise SyntaxError(colored("SyntaxError: There cannot be a unary operator followed by a binary operator:","red")+" "+colored(string_list[i],"yellow")+" "+colored(string_list[i+1],"yellow"))

    @staticmethod
    def check_adjacent_features(string):

        string_list = ASTUtilities.string2list(string)

        for i in range(0,len(string_list)-1):

            fist_item = ASTUtilities.clean_parentheses(string_list[i])
            second_item = ASTUtilities.clean_parentheses(string_list[i+1])

            if(ASTUtilities.is_feature(fist_item) and ASTUtilities.is_feature(second_item)):
                raise SyntaxError(colored("SyntaxError: There cannot be two adjacent features: ","red")+" "+colored(string_list[i],"yellow")+" "+colored(string_list[i+1],"yellow"))

    @staticmethod
    def check_binary_operator_preceded_or_succeeded_by_parentheses(string):

        string_list = ASTUtilities.string2list(string)

        for i in range(0,len(string_list)):

            item_with_parentheses = string_list[i]
            item_without_parentheses = ASTUtilities.clean_parentheses(string_list[i])

            if(ASTUtilities.is_binary_operator(item_without_parentheses)):
                if(item_with_parentheses != item_without_parentheses):
                    raise SyntaxError(colored("SyntaxError: A binary operator cannot be preceded or succeeded by parentheses: ","red")+" "+colored(string_list[i],"yellow")+" "+colored(string_list[i+1],"yellow"))

    @staticmethod
    def check_unary_operator_succeeded_by_parentheses(string):

        string_list = ASTUtilities.string2list(string)

        for i in range(0,len(string_list)):

            item = ASTUtilities.clean_parentheses(string_list[i])

            if(ASTUtilities.is_unary_operator(item) and ")" in string_list[i]):
                raise SyntaxError(colored("SyntaxError: An unary operator cannot succeeded by parentheses: ","red")+""+colored(string_list[i],"yellow"))

    @staticmethod
    def check_binary_operator_at_start_or_end(string):

        string_list = ASTUtilities.string2list(string)

        fist_item = ASTUtilities.clean_parentheses(string_list[0])
        second_item = ASTUtilities.clean_parentheses(string_list[-1])

        if(ASTUtilities.is_binary_operator(fist_item)):
            raise SyntaxError(colored("There cannot be binary operator at start:","red")+" "+colored(string_list[0],"yellow"))

        if(ASTUtilities.is_binary_operator(second_item)):
            raise SyntaxError(colored("There cannot be binary operators at end:","red")+" "+colored(string_list[-1],"yellow"))

    @staticmethod
    def check_unary_operator_at_end(string):

        string_list = ASTUtilities.string2list(string)

        item = ASTUtilities.clean_parentheses(string_list[-1])

        if(ASTUtilities.is_unary_operator(item)):
            raise SyntaxError(colored("There cannot be unary operators at end:","red")+" "+colored(string_list[-1],"yellow"))

    # TODO: Detectar paréntesis vacíos "()"
    @staticmethod
    def check_empty_parentheses(string):

        for i in range(0,len(string)-1):

            first_item = string[i]
            second_item = string[i+1]

            if(first_item == "(" and second_item == ")"):
                raise SyntaxError(colored("SyntaxError: There cannot be empty parentheses: ","red")+" "+colored(string[i],"yellow")+""+colored(string[i+1],"yellow"))


class ASTUtilities():

    @staticmethod
    def string2list(string):

        string = " ".join(string.split())
        return list(string.split(" "))

    #preprocesamiento de la cadena de entrada 
    @staticmethod
    def preprocessing(string):

        preprocessed_string = string

        preprocessed_string = ASTUtilities.computing_blank_spaces(preprocessed_string)

        #preprocessed_string = ASTUtilities.preprocessing_remove_outer_parentheses(string)

        return preprocessed_string

    @staticmethod
    def computing_blank_spaces(string):

        preprocessed_string = string

        if("(" in preprocessed_string or ")" in preprocessed_string):
            # elimina espacios a la derecha de "("
            while("( " in preprocessed_string):
                for i in range(len(preprocessed_string)-1):
                    if(preprocessed_string[i] == "(" and preprocessed_string[i+1] == " "):
                        preprocessed_string = ASTUtilities.replacer(preprocessed_string,"",i+1)
                        break

            # elimina espacios a la izquierda de ")"
            while(" )" in preprocessed_string):
                for i in range(len(preprocessed_string)-1):
                    if(preprocessed_string[i] == " " and preprocessed_string[i+1] == ")"):
                        preprocessed_string = ASTUtilities.replacer(preprocessed_string,"",i)
                        break

            # añade un espacio en blanco a la izquierda de "(" si lo que hay a la izquierda no es otro "("
            end = False 
            while(not end):
                for i in range(1,len(preprocessed_string)-1):
                        if(preprocessed_string[i] == "(" and preprocessed_string[i-1] != "("):
                            preprocessed_string = ASTUtilities.replacer(preprocessed_string," (",i)
                            break
                        end = True

            # añade un espacio en blanco a la derecha de ")" si lo que hay a la derecha no es otro ")"
            end = False 
            while(not end):
                for i in range(1,len(preprocessed_string)-1):
                        if(preprocessed_string[i] == ")" and preprocessed_string[i+1] != ")"):
                            preprocessed_string = ASTUtilities.replacer(preprocessed_string,") ",i)
                            break
                        end = True

        # elimina dobles espacios
        while("  " in preprocessed_string):
            for i in range(len(preprocessed_string)-1):
                if(preprocessed_string[i] == " " and preprocessed_string[i+1] == " "):
                    preprocessed_string = ASTUtilities.replacer(preprocessed_string,"",i)
                    break

        # elimina espacios en blanco al principio y final
        preprocessed_string = preprocessed_string.strip()

        return preprocessed_string

    #cuenta caracteres repetidos
    @staticmethod
    def count_characters(string,character):
        count = 0
        for c in string:
            if(c == character):
                count = count+1
        return count
        
    #elimina paréntesis exteriores
    @staticmethod
    def preprocessing_remove_outer_parentheses(string):

        string_without_outer_parentheses = string

        while(string_without_outer_parentheses[0] == "(" and string_without_outer_parentheses[len(string_without_outer_parentheses)-1] == ")"):
            string_without_outer_parentheses = ASTUtilities.replacer(string_without_outer_parentheses, "", 0)
            string_without_outer_parentheses = ASTUtilities.replacer(string_without_outer_parentheses, "", len(string_without_outer_parentheses)-1)

        return string_without_outer_parentheses

    @staticmethod
    def clean_parentheses(string):
    
        cleaned_string = string

        cleaned_string = cleaned_string.replace("(","")
        cleaned_string = cleaned_string.replace(")","")

        return cleaned_string

    @staticmethod
    def is_unary_operator(element):
        return element in ASTINFO.get_unary_operators()

    @staticmethod
    def is_binary_operator(element):
        return element in ASTINFO.get_binary_operators()

    @staticmethod
    def is_feature(element):
        return not ASTUtilities.is_binary_operator(element) and not ASTUtilities.is_unary_operator(element) and not element == ")" and not element == "("

    @staticmethod
    # Extraído de https://stackoverflow.com/questions/41752946/replacing-a-character-from-a-certain-index/41753038#:~:text=5%20Answers&text=As%20strings%20are%20immutable%20in,value%20at%20the%20desired%20index.&text=You%20can%20quickly%20(and%20obviously,%22slices%22%20of%20the%20original.&text=Strings%20in%20Python%20are%20immutable%20meaning%20you%20cannot%20replace%20parts%20of%20them.
    def replacer(s, newstring, index, nofail=False):
        # raise an error if index is outside of the string
        if not nofail and index not in range(len(s)):
            raise ValueError("index outside given string")

        # if not erroring, but the index is still not in the correct range..
        if index < 0:  # add it to the beginning
            return newstring + s
        if index > len(s):  # add it to the end
            return s + newstring

        # insert the new string between "slices" of the original
        return s[:index] + newstring + s[index + 1:]

class AST():

    #variables  
    string = ""
    nodes = []
    list = []

    def __init__(self,string=""):

        # Preprocesamiento
        preprocessed_string = ASTUtilities.preprocessing(string)

        # Comprobaciones de sintaxis básicas
        ASTCHECK.check_all(preprocessed_string)

        self.string = preprocessed_string
        self.nodes = []
        self.list = ASTUtilities.string2list(preprocessed_string)

        print("\n-------------------------------------------\n")

        #print("\n")
        #print(self.string)
        #print(self.list)
        
        self.explore(i=0,j=len(self.list),points_to=None,level=0)
        
        # testing

        for n in self.nodes:
            #print(n)
            pass

    def __str__(self):
        return "\n\"" + self.string + "\"" + self.print_tree(self.get_root(),"\n\n" + self.get_root().get_name())

    def print_tree(self,node,string):
        childs_nodes = self.get_childs(node)
        for n in childs_nodes:
            string = string + self.print_tree(n,"\n"  + self.print_tabs(n) + n.get_name())

        return string

    def print_tabs(self,node):
        level = node.get_level()
        tabs = ""
        for i in range(level-1):
            tabs = tabs + "\t"
        return tabs

    # extrae las posiciones de los operadores binarios en el rango (i,j]
    def extract_binary_operators(self,i,j):

        list_binary_operators = []

        for i in range(i,j):
            if self.list[i] in ASTINFO.get_binary_operators():
                list_binary_operators.append(i)

        return list_binary_operators

    # extrae las posiciones de los operadores unarios en el rango (i,j]
    def extract_unary_operators(self,i,j):

        list_unary_operators = []

        for i in range(i,j):
            if self.list[i] in ASTINFO.get_unary_operators():
                list_unary_operators.append(i)

        return list_unary_operators

    # descarta los operadores binarios encerrados entre paréntesis
    def discard_nodes_in_parentheses(self,i,j,list):
        
        candidate_root_nodes_without_parentheses = []

        for e in list:

            # flag
            without_parentheses = True

            # un elemento "e" estará libre si NI a su izquierda NI a su derecha no tiene ningún elemento con apertura o cierre de paréntesis
            
            # ¿hay algún paréntesis "(" a la izquierda?
            # nota: el primer elemento no se cuenta por considerarse paréntesis exterior, de ahí lo de k != i
            for k in range(i,e):
                if("(" in self.list[k] and k != i):
                    without_parentheses = False
                    break

            # ¿hay algún paréntesis ")" a la derecha?
             # nota: el último elemento no se cuenta por considerarse paréntesis exterior, de ahí lo de k != j-1
            if(without_parentheses):
                for k in range(e+1,j):
                    if(")" in self.list[k]  and k != j-1):
                        without_parentheses = False
                        break

            if(without_parentheses): # si no tiene, en este caso, paréntesis a la derecha, también es un candidato
                candidate_root_nodes_without_parentheses.append(e)   

        return candidate_root_nodes_without_parentheses

    def explore(self,i,j,points_to,level):

        # existe el caso particular de hacer Divide y Vencerás a partir de un operador unario
        # esto provoca que sea una sublista SIN elementos, puesto que el operador unario 
        # no opera con elementos a la izquierda
        if(j-i == 0):
            return

        # lista con un solo elemento (es una feature tipo "A")
        if(j-i == 1):

            node = Node(is_leaf=True, is_feature=True, points_to=points_to, feature=ASTUtilities.clean_parentheses(self.list[i]),level=level+1, token=i)
            self.nodes.append(node)

            return 

        # lista con dos elementos (es de tipo "not A")
        if(j-i == 2):

            # el primer nodo es el unario
            node_1 = Node(points_to=points_to, operator=self.list[i],level=level+1, token=i)
            self.nodes.append(node_1)

            # el segundo nodo es la feature
            node_2 = Node(is_leaf=True, is_feature=True, points_to=i, feature=ASTUtilities.clean_parentheses(self.list[i+1]),level=level+2,token=i+1)
            self.nodes.append(node_2)

            return

        # lista con tres elementos (es de tipo "A implies B")
        if(j-i == 3):

            # el nodo padre (operator) es el central (i+1)
            node = Node(operator=self.list[i+1], points_to=points_to,  level=level+1  , token=i+1)
            self.nodes.append(node)

            # el primer hijo (feature) es el nodo de la izquierda
            node_1 = Node( is_leaf=True , is_feature=True, points_to=i+1,feature=ASTUtilities.clean_parentheses(self.list[i]),level=level+2  , token=i)
            self.nodes.append(node_1)

            # el segundo hijo (feature) es el nodo de la derecha
            node_2 = Node( is_leaf=True , is_feature=True, points_to=i+1,feature=ASTUtilities.clean_parentheses(self.list[i+2]),level=level+2  , token=i+2)
            self.nodes.append(node_2)

            return

        parent = self.find_out_parent_node(i,j)
        node = Node(points_to=points_to, operator=self.list[parent],level=level+1  , token=parent)
        self.nodes.append(node)

        # divide and conquer
        self.explore(i,parent,points_to=parent,level=level+1)
        self.explore(parent+1,j,points_to=parent,level=level+1)

    # encuentra el nodo padre más idóneo en el subconjunto [i,j)
    def find_out_parent_node(self,i,j):

        # "+str(i)+", j: "+str(j))

        parent = None

        # Obtenemos los posibles nodos candidatos a ser el padre
        candidate_binary_parent_nodes = self.extract_binary_operators(i,j)
        #print("candidate_binary_parent_nodes: ")
        #print(candidate_binary_parent_nodes)

        candidate_unary_parent_nodes = self.extract_unary_operators(i,j)
        #print("candidate_unary_parent_nodes: ")
        #print(candidate_unary_parent_nodes)

        # Descartamos aquellos que están encerrados entre paréntesis
        candidate_binary_parent_nodes_without_parentheses = self.discard_nodes_in_parentheses(i=i,j=j,list=candidate_binary_parent_nodes)
        candidate_unary_parent_nodes_without_parentheses = self.discard_nodes_in_parentheses(i=i,j=j,list=candidate_unary_parent_nodes)

        #print("\ncandidate_binary_parent_nodes_without_parentheses: ")
        #print(candidate_binary_parent_nodes_without_parentheses)

        '''
            En el mismo nivel (entiéndase por "mismo nivel" los nodos que están libres de paréntesis)
            los operadores unario tienen prioridad si previamente no hay operadores binarios
        '''

        # si la lista de operadores binarios NO está vacía
        if(candidate_binary_parent_nodes_without_parentheses):

            # de todos los operadores binarios, se obtiene el que más prioridad tenga
            parent = self.priority_binary_operator_according_to_hierarchy(candidate_binary_parent_nodes_without_parentheses) #TODO

        else: # si la lista de operadores binarios está vacía
            
            # de todos los operadores unarios, se obtiene el que más prioridad tenga
            #print("candidate_unary_parent_nodes_without_parentheses: ")
            #print(candidate_unary_parent_nodes_without_parentheses)
            parent = self.priority_unary_operator_according_to_hierarchy(candidate_unary_parent_nodes_without_parentheses) #TODO

        return parent

    # dada una lista de operadores unarios, encuentra el más prioritario
    def priority_unary_operator_according_to_hierarchy(self,list):
        
        unary_operators = ASTINFO.get_unary_operators()
        position = len(unary_operators)-1
        priority = list[0]

        for e in list:
            new_position = unary_operators.index(self.list[e])

            if(new_position < position):
                position = new_position
                priority = e

        return priority

    # dada una lista de operadores biarios, encuentra el más prioritario
    def priority_binary_operator_according_to_hierarchy(self,list):

        binary_operators = ASTINFO.get_binary_operators()
        position = len(binary_operators)-1
        priority = list[0]

        for e in list:
            new_position = binary_operators.index(self.list[e])

            if(new_position < position):
                position = new_position
                priority = e

        return priority

    # common methods
    def get_nodes_by_feature(self,feature):
        res_node = []
        for node in self.nodes:
            if node.get_name() == feature:
                res_node.append(node)
        return res_node

    def get_root(self):
        res_node = None
        for node in self.nodes:

            #print("for")

            if(node.points_to == None):
                res_node = node

                #print("ee")

                break
        return res_node

    def get_childs(self,parent_node):
        childs = []
        points_to = parent_node.get_token()
        for node in self.nodes:
            if node.get_points_to() == str(points_to):
                childs.append(node)
        return childs

    def get_nodes(self):

        return self.nodes
        
    
class Node():

    token = None

    is_leaf = False
    feature = ""
    is_feature = False
    unary_operator = False
    binary_operator = False
    points_to = None
    operator = ""

    level = None

    def __init__(self,token=None,is_leaf=False,feature="",is_feature=False,unary_operator=False,binary_operator=False,points_to=None,operator="",level=0):
        self.token = token
        self.is_leaf = is_leaf
        self.feature = feature
        self.is_feature = is_feature
        self.unary_operator = unary_operator
        self.binary_operator = binary_operator
        self.points_to = points_to
        self.operator = operator
        self.level = level

    def is_leaf(self):
        return self.is_leaf

    def is_root(self):
        return self.points_to == None

    def get_token(self):
        return self.token

    def get_points_to(self):
        if(self.points_to == None):
            return "None"
        return str(self.points_to)

    def get_name(self):
        name = ""
        if self.is_feature:
            name = self.feature
        else:
            name = self.operator

        return name

    def get_level(self):
        return self.level

    def __str__(self):
        string = "Node: "+self.get_name()+", points to: "+str(self.get_points_to())+", token: "+str(self.get_token())+", level: "+str(self.get_level())

        return string


main()