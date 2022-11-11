from utils.tree import Node
from collections import deque

def is_in_facts(var:str, facts:dict) -> bool:
    return var in list(facts.keys())


def add_in_facts(facts:dict, var:str) -> None:
    facts[var] = True


def get_new_facts(root:Node, facts:dict) -> None:
    for child in root.children:
        if child.value:
            add_in_facts(facts, child.name)


def modus_ponens_facts(root:Node, facts) -> bool:
    if root.name in list(facts.keys()):
        if facts[root.name]:
            root.value = True
            return True
    return False



def forward_chaining(root:Node, rules:list, facts:dict):
    
    def modus_ponens_forward(rule:dict, facts):
        antecedente_set = set(rule['antecedente'])
        facts_set = set(facts)

        #se todas as variáveis dos antecedentes estão nos fatos
        if len(antecedente_set.difference(facts_set)) == 0:
            return True
        return False


    def encadeamento_para_frente(root:Node, rules:list, facts:dict):
        i = len(facts)
        rules_copy = rules
        used_keys = list(facts.keys())
        
        while not i > len(facts):
            for rule in rules_copy:
                if modus_ponens_forward(rule, used_keys):
                    facts[list(rule['consequente'].keys())[0]] = True
                    rules_copy.remove(rule)
            if not i >= len(facts):
                used_keys.append(list(facts.keys())[i])
            if modus_ponens_facts(root, facts):
                return True
            i += 1
        return False

    return encadeamento_para_frente(root, rules, facts)


def backward_chaining(root:Node, intermediate_rules:list, goal_rules:list, facts:dict):
    
    def build_tree(root:Node, rules:list):
        for rule in rules:
            consequente = rule.get('consequente')
            if root.name in list(consequente.keys()):
                for antecedente in rule.get('antecedente'):
                    if not root.is_parent(antecedente):
                        root.add_child(Node(antecedente, False))
    

    def modus_ponens_backward(root:Node, facts) -> bool:
        if root.value:
            if not is_in_facts(root.name, facts):
                add_in_facts(facts, root.name)
            return True

        if root.has_children():
            flag = True
            for child in root.children:        
                if not child.value:
                    flag = False
                    break

            if flag and not is_in_facts(root.name, facts):
                add_in_facts(facts, root.name)
            root.value = flag
            return flag
        else:
            return False


    def verification(root:Node, rules:list, facts:dict):
        root.value = modus_ponens_facts(root, facts)
        
        if root.value:
            return True
        
        if modus_ponens_backward(root, facts):
            return True

        build_tree(root, rules)


    def print_tree(root:Node):
        print("\n---------New tree")
        Stack = deque([root])
        preorder_visited = []
        
        while Stack:
            top = Stack.pop()
            preorder_visited.append(top)
            print(f'Top: {top.name}')
            print('Children: ')

            top.print_children()
            for child in top.children:
                Stack.append(child)


    def build_encadeamento_para_tras() -> Node:
        Stack = deque([root])
        preorder_visited = []
        
        while Stack:
            top = Stack.pop()
            preorder_visited.append(top)

            build_tree(root, goal_rules)

            for child in top.children:
                build_tree(root, intermediate_rules)
                Stack.append(child)
        
        print_tree(root)
        return root

    return build_encadeamento_para_tras()
