import sys
import os

# use 'utils' package
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# END use 'utils' package

import utils.read_inputs_fc as read_inputs
from utils.incerteza import varFC

def string_diagnostico(cons:varFC) -> str:
    return f"{' '.join(cons.name.split('_')).capitalize()}: (FC: {cons.fc:.2f})"


def print_facts(facts:list):
    for fact in facts:
        print(fact.to_string())
    print()


def print_rule(rule:dict):
    print("Se os sintomas são ", end='')
    for i in range(0, len(rule['antecedente'])):
        print(string_diagnostico(rule['antecedente'][i]), end='')
        if i == len(rule['antecedente']) - 1:
            print(' -> ', end='')
        else:
            print(' E ', end='')
    print(string_diagnostico(rule['consequente']))
    

def atualizar_fc(var:varFC, facts:list):
    for fact in facts:
        if fact.name == var.name:
            var.set_fc(fact.fc)
            return


def proved_true(var:varFC, facts:dict) -> bool:
    return var.name in facts.keys() and facts[var.name] == var.value


def proved_false(var:varFC, facts:dict) -> bool:
    return var.name in facts.keys() and facts[var.name] != var.value


def modus_ponens_FC(rule:dict, facts:list, facts_answered):
    minimo = rule['antecedente'][0].fc
    for i in range(0, len(rule['antecedente'])):
        if proved_false(rule['antecedente'][i], facts_answered):
            return False
        
        if rule['antecedente'][i].fc < minimo:
            minimo = rule['antecedente'][i].fc
    
    print(f"mínimo: {minimo}")
    rule['consequente'].set_fc(minimo * rule['consequente'].fc)
    return True


def diagnostico(rules:list, facts:list) -> bool:
    facts_answered = {}
    for rule in list(rules):
        if proved_false(rule['consequente'], facts_answered):
            rules.remove(rule)
            continue
        
        for ant in list(rule['antecedente']):
            if proved_false(ant, facts_answered):
                break
            
            if proved_true(ant, facts_answered):
                atualizar_fc(ant, facts)
                continue 

            while True:
                ans = input(f"Você sente {' '.join(ant.name.split('_'))}? [s/n] ").strip().lower()
                if ans[0] not in ['s', 'n']:
                    print('Resposta inválida.')
                else:
                    break
                
            if ans[0] == 's':
                while True:
                    try:
                        certeza = float(input('Defina o grau de certeza [0, 1]: '))
                        if certeza < 0 or certeza > 1:
                            print('O valor deve estar entre 0 e 1.')
                        else: 
                            break
                    except ValueError:
                        print('Erro: Insira um valor válido.')
                
                ant.set_fc(certeza)

                facts.append(ant)
                facts_answered[ant.name] = True
            
            elif ans[0] == 'n':
                facts_answered[ant.name] = False
                break


        if modus_ponens_FC(rule, facts, facts_answered):
            print(f"\nDiagnóstico: {string_diagnostico(rule['consequente'])}")
            print('\nExplicação: ')
            print_rule(rule)
            print('\nMemória de trabalho: ')
            print_facts(facts)

            facts.append(rule['consequente'])
            facts_answered[rule['consequente'].name] = True
            return True
        else:
            facts_answered[rule['consequente'].name] = False
            
    return False


def main():
    rules = []
    facts = []
    variables = []

    try:
        read_inputs.get_rules_fc(rules, variables, "rules")
    except Exception as e:
        print(f'ERRO: {e.args[0]}')
        return 
    
    if not diagnostico(rules, facts):
        print("Não consegui identificar a doença.")

main()
