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
    # print(f"Was it proved false? {var}")
    return var in facts.keys() and rule[var] != facts[var]


def perguntar(rules:list, facts:dict, goal:bool):
    # print(rules)
    for rule in list(rules):
        # print(f"Curr rule: {rule}")
        consequente = list(rule['consequente'].keys())[0]
        
        if proved_false(rule['consequente'], consequente, facts):
            rules.remove(rule)
            continue
        
        for ant in list(rule['antecedente'].keys()):
            if proved_false(rule['antecedente'], ant, facts):
                break
            
            if proved_true(rule['antecedente'], ant, facts):
                continue 

            while True:
                ans = input(f"O animal {' '.join(ant.split('_'))}? [s/n] ").strip().lower()
                if ans[0] not in ['s', 'n']:
                    print('Resposta inválida.')
                else:
                    break
                
            if ans[0] == 's':
                facts[ant] = True
            elif ans[0] == 'n':
                facts[ant] = False
                facts['nao_'+ant] = True
                break

        if modus_ponens_forward(rule, facts):
            if goal:
                while True:
                    decid = input(f"O animal é um {consequente}? [s/n] ").strip().lower()
                    if decid[0] not in ['s', 'n']:
                        print("Resposta inválida.")
                    else:
                        break
                if decid[0] == 's':
                    facts[consequente] = True
                    return True
                elif decid[0] == 'n':
                    break
            else: 
                facts[consequente] = True
        else:
            facts[consequente] = False
            facts['nao_'+consequente] = True
    
    return False


def adivinhar(intermediate_rules:list, goal_rules:list, facts:dict) -> bool:
    perguntar(intermediate_rules, facts, False)
    
    goal_cp = []
    for rule in goal_rules:
        flag = True
        for ant in list(rule['antecedente'].keys()):
            if proved_false(rule['antecedente'], ant, facts):
                flag = False
                break
        if flag:   
            goal_cp.append(rule)

    for rule in goal_cp:
        pass
    
    return perguntar(goal_cp, facts, True)


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

    print('Pense em um deles...\n')
    
    print("Adivinhei") if adivinhar(intermediate_rules, goal_rules, facts) else print("Tem certeza que pensou em um dos animais que eu conheço?")


main(sys.argv)
