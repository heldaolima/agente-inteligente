import csv
from utils.incerteza import varFC

def get_rules(rules:list, variables:list, file_name:str): 
    try:
        with open(f'./data/{file_name}.csv') as rules_file:
            rules_dict = csv.DictReader(rules_file)
            i = 0

            for regra in rules_dict:
                rules.append({})
                rules[i]['antecedente'] = {}
                rules[i]['consequente'] = {}
                for var in regra['antecedente'].split(' and '):
                    rules[i]['antecedente'][var] = True
                    if not var in variables: 
                        variables.append(var)
                rules[i]['consequente'][regra['consequente']] = True
                if regra['consequente'] not in variables: 
                        variables.append(regra['consequente'])
                i += 1
    except IOError as error:
        raise FileNotFoundError("Pasta não econtrada")


def print_rules(rules:list, prefixo:str):
    for rule in rules:
        vars_ant = list(rule['antecedente'].keys())
        num_vars = len(vars_ant)
        var_cons = rule['consequente']
        print(prefixo, end=' ')
        for i in range(0, num_vars):
            if i == num_vars-1:
                print(f'{" ".join(vars_ant[i].split("_"))}, então ', end='')
            else:
                print(f'{" ".join(vars_ant[i].split("_"))} ^', end='')
            print(' ', end='')
        print(f'{var_cons.to_string()}')


def print_facts(facts:dict):
    for key in list(facts.keys()):
        print(f'{key}: {facts[key]}')