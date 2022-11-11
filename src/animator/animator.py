from collections import deque
import sys
import os

# use 'utils' package
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# END use 'utils' package

import utils.read_inputs as read_inputs
from utils.tree import Node
import utils.chainings as chainings

def encadear(rules:list, facts:dict):
    pass

def playable(rule:dict, facts:dict) -> bool:
    antecedente_set = set(rule['antecedente'])
    facts_set = set(facts)

    return len(antecedente_set.difference(facts_set)) == 0


def modus_ponens_forward(rule:dict, facts:dict) -> bool:
    consequente = list(rule['consequente'].keys())[0]
    if consequente in facts.keys():
        return facts[consequente]

    for var in list(rule['antecedente'].keys()):
        if not var in facts.keys():
            return False
        
        if facts[var] != rule['antecedente'][var]:
            rule['consequente'][consequente] = False
            return False
    return True


def proved_true(rule:dict, var:str, facts:dict):
    return var in facts.keys() and rule[var] == facts[var]


def proved_false(rule:dict, var:str, facts:dict) -> bool:
    return var in facts.keys() and rule[var] != facts[var]


def adivinhar(intermediate_rules:list, goal_rules:list, facts:dict, variables:list):    
    # trees = []

    # for rule in goal_rules:
    #     trees.append(backward_chaining(Node(list(rule['consequente'].keys())[0], False), intermediate_rules, goal_rules, facts))

    #fase 1: descobrir os primeiros dados sobre o animal
    for rule in list(intermediate_rules):
        consequente = list(rule['consequente'].keys())[0]
        
        if proved_false(rule['consequente'], consequente, facts):
            intermediate_rules.remove(rule)
            continue
        
        for ant in list(rule['antecedente'].keys()):

            if proved_false(rule['antecedente'], ant, facts):
                print(f'\n I have already prooved {ant} false')
                break
            
            if proved_true(rule['antecedente'], ant, facts):
                print(f'\n I have already prooved {ant} true')
                continue 

            ans = input(f"O animal {' '.join(ant.split('_'))}? [s/n] ").lower().strip()
            if ans[0] == 's':
                facts[ant] = True
            elif ans[0] == 'n':
                facts[ant] = False
                facts['nao_'+ant] = True
        
        if modus_ponens_forward(rule, facts):
            facts[consequente] = True
        else:
            facts[consequente] = False
            facts['nao_'+consequente] = True
            # intermediate_rules.remove(rule)
            # break
        
        print(f'fatos agora: {facts}')        
        
    print("acabei de passar pelas regras intermediárias. Resultado: ")
    for rule in intermediate_rules:
        print(rule)

    #fase 2: preprocessar as regras objetivo, para remover os animais que não se encaixam com as respostas até aqui

    #fase 3: descobrir qual é o animal pela repetição do processo
    


def main(modo):
    intermediate_rules = []
    goal_rules = []
    facts = {}
    variables = []

    try:
        read_inputs.get_rules(intermediate_rules, variables, "intermediate_rules")
        read_inputs.get_rules(goal_rules, variables, "goal_rules")
        read_inputs.get_facts(facts, variables, "data")
    except Exception as e:
        print(f'ERRO: {e.args[0]}')
        return 


    print('Eu conheço os seguintes animais: ')
    for goal in goal_rules:
        print(f"> {list(goal['consequente'].keys())[0]}")

    print('Pense em um deles...\nVariáveis:')
    # read_inputs.print_variables(variables)
    
    adivinhar(intermediate_rules, goal_rules, facts, variables)

    

# if len(sys.argv) <= 1: 
#     print("Usage: python3 animator.py <modo>.\nModos: 'adivinhar' | 'diagnosticar'")

# sys.argv[1] = sys.argv[1].lower().strip()
# if not sys.argv[1] in ['adivinhar', 'diagnosticar']:
#     print("ERRO: modo inválido.\nModos: 'adivinhar' | 'diagnosticar'")


main(sys.argv)
