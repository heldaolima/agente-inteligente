import sys
import os

# use 'utils' package
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# END use 'utils' package

import utils.read_inputs_fc as read_inputs
from utils.incerteza import varFC

def proved_false(var:varFC, facts:dict) -> bool:
    return var.get_name() in facts.keys() and facts[var.get_name()] != var.value


def diagnostico(rules:list, facts:dict) -> bool:
    for rule in list(rules):
        consequente = rule['consequente']
        
        if proved_false(rule['consequente'], consequente, facts):
            rules.remove(rule)
            continue
        
        for ant in list(rule['antecedente'].keys()):
            if proved_false(rule['antecedente'], facts):
                break
            
            if proved_true(rule['antecedente'], ant, facts):
                continue 

            while True:
                ans = input(f"Você sente {' '.join(ant.split('_'))}? [s/n] ").strip().lower()
                if ans[0] not in ['s', 'n']:
                    print('Resposta inválida.')
                else:
                    break
                
            if ans[0] == 's':
                facts[ant] = True
                facts['nao_'+ant] = False
            elif ans[0] == 'n':
                facts[ant] = False
                facts['nao_'+ant] = True
                break

        if modus_ponens_forward_single_rule(rule, facts):
            print("can do modus ponens")
            pass
    
    return False


def main():
    rules = []
    facts = {}
    variables = []

    try:
        read_inputs.get_rules_fc(rules, variables, "rules")
    except Exception as e:
        print(f'ERRO: {e.args[0]}')
        return 

    print("Regras: ")
    read_inputs.print_rules_fc(rules)

    
    diagnostico(rules, facts)


main()
