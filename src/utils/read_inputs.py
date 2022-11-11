import csv


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
                    if var not in variables: 
                        variables.append(var)
                rules[i]['consequente'][regra['consequente']] = True
                if regra['consequente'] not in variables: 
                        variables.append(regra['consequente'])
                i += 1
    except IOError as error:
        raise FileNotFoundError("Pasta não econtrada")


def get_facts(facts:dict, variables:list, folder):
    try:
        with open(f'./{folder}/facts.csv') as facts_file:
            facts_dict = csv.DictReader(facts_file)
            
            for fact in facts_dict:
                facts[fact['variavel']] = True
                if fact['variavel'] not in variables: 
                        variables.append(fact['variavel'])
    except IOError as error:
        raise FileNotFoundError("Pasta não encontrada")



def print_variables(variables:list):
    for var in variables:
        print(f'{var}')
    print()


def print_rules(rules:list):
    for rule in rules:
        vars_ant = list(rule['antecedente'].keys())
        num_vars = len(vars_ant)
        var_cons = list(rule['consequente'].keys())
        print("Se o animal é ", end='')
        for i in range(0, num_vars):
            if i == num_vars-1:
                print(f'{" ".join(vars_ant[i].split("_"))}, então ele é', end='')
            else:
                print(f'{" ".join(vars_ant[i].split("_"))} ^', end='')
            print(' ', end='')
        print(f'{var_cons[0]}')


def print_facts(facts):
    for key in list(facts.keys()):
        print(f'{key}: {True}')


def read_facts_from_user(facts:dict, variables):
    print("A base de conhecimento foi deixada vazia. Insira alguns fatos baseado nas variáveis até o momento:")
    print_variables(variables)
    
    n_facts = int(input('Insira o número de fatos: '))
    for i in range(0, n_facts):
        fact = str(input('Fato: '))
        if fact not in variables:
            variables.append(fact)
        facts[fact] = True
