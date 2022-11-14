import csv
from utils.incerteza import varFC


def get_rules_fc(rules:list, variables:list, file_name:str):
    try:
        with open(f'./data/{file_name}.csv') as rules_file:
            rules_dict = csv.DictReader(rules_file)
            i = 0

            for regra in rules_dict:
                rules.append({})
                rules[i]['antecedente'] = []
                for var in regra['antecedente'].split(' and '):
                    rules[i]['antecedente'].append(varFC(var, True, 100.0))
                    if var not in variables: 
                        variables.append(var)
                consequente = regra['consequente'].split('=')
                try:
                    consequente[1] = float(consequente[1])
                except ValueError:
                    print("ERRO: O consequente deve ter um fator de certeza")
                    exit(1)
                rules[i]['consequente'] = varFC(consequente[0], True, consequente[1])
                if consequente[0] not in variables: 
                        variables.append(regra['consequente'])
                i += 1
    except IOError as error:
        raise FileNotFoundError("Pasta não econtrada")


def print_rules_fc(rules:list):
    for rule in rules:
        print("Se o sintoma é", end=' ')
        for ant in rule['antecedente']:
            print(ant.to_string(), end=' ')
        print(f" -> {rule['consequente'].to_string()}")
        
            # len_ant = len(rule['antecedente'])
            # print('Se o sintoma é', end=' ')
            # for i in range(0, len_ant):
            #     print(' '.join(rule[i].get_name().split('_')), end='')
            #     if i == len_ant - 1:
            #         print(" , então ", end='')
            #     else:
            #         print(" E ", end='')
            # print(rule['consequente'].to_string())