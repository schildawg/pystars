import csv, re

import re

def lexer(input_string):
    tokens = []
    index = 0
    length = len(input_string)
    
    while index < length:
        # Skip whitespace
        if input_string[index].isspace():
            index += 1
            continue
        
        # Check for numbers
        if input_string[index].isdigit():
            num = ""
            while index < length and input_string[index].isdigit():
                num += input_string[index]
                index += 1
            tokens.append(("NUMBER", int(num)))
            continue
        
        # Check for labels (alphabetic characters only)
        elif input_string[index].isalpha():
            label = ""
            while index < length and input_string[index].isalpha():
                label += input_string[index]
                index += 1
            tokens.append(("LABEL", label))
            continue
        
        # If we encounter an unknown character, raise an error
        else:
            raise ValueError(f"Unexpected character: {input_string[index]} at position {index}")
    
    return tokens

greek_letters = {
    'Alp': 'alpha', 'Bet': 'beta', 'Gam': 'gamma', 'Del': 'delta', 'Eps': 'epsilon',
    'Zet': 'zeta', 'Eta': 'eta', 'The': 'theta', 'Iot': 'iota', 'Kap': 'kappa',
    'Lam': 'lambda', 'Mu': 'mu', 'Nu': 'nu', 'Xi': 'xi', 'Omi': 'omicron',
    'Pi': 'pi', 'Rho': 'rho', 'Sig': 'sigma', 'Tau': 'tau', 'Ups': 'upsilon',
    'Phi': 'phi', 'Chi': 'chi', 'Psi': 'psi', 'Ome': 'omega'
}

stars = []
with open('yale_bright_stars.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  
    stars.append(header)  

    for row in csv_reader:
        stars.append(row)

count = 0

with open("stars2.csv", "w") as file:
    for row in stars:
        name = row[1]

        # if row[1] == "":
        #     continue

        constellation = row[1][-3:].lower()
        if not constellation.isalpha():
            continue;
    
        number = ""
        letter = ""

        tokens = lexer(row[1])
        current = 0
        if tokens[current][0] == "NUMBER":
            number = tokens[current][1]
            current = current + 1
        
        if tokens[current][0] == "LABEL":
            if tokens[current][1].lower() != constellation:
               letter = tokens[current][1]
               current = current + 1

        if letter == None or letter == "":
            letter = str(number)

        for key, full_name in greek_letters.items():
            if letter in key:
                letter = full_name
                break

        if current < len(tokens) and tokens[current][0] == "NUMBER":
            letter = letter + str(tokens[current][1])
            current = current + 1

        ra = row[19] + ":" + row[20] + ":" + row[21]
        dec = row[22] + row[23] + ":" + row[24] + ":" + row[25]
        glong = row[26]
        glat = row[27]
        glat = row[27]
        vmag = row[28]
        color = row[31]
        spectrum = row[37]
        parallex = row[42]
        
        # if parallex == "":
        #     continue

        count = count + 1

        file.write(row[0] + "," + constellation + "," + str(number) + "," + letter + "," + ra + "," + dec + "," + glong + "," + glat + "," + vmag + "," + color + "," + spectrum + "," + parallex + "\n")

print(count)
# print("Α α, Β β, Γ γ, Δ δ, Ε ε, Ζ ζ, Η η, Θ θ, Ι ι, Κ κ, Λ λ, Μ μ, Ν ν, Ξ ξ, Ο ο, Π π, Ρ ρ, Σ σ/ς, Τ τ, Υ υ, Φ φ, Χ χ, Ψ ψ, Ω ω.")