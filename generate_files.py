import pandas as pd

def generate_txt_from_csv(csv_file_path):
    # Llegeix el fitxer CSV
    data = pd.read_csv(csv_file_path)
    
    # Obtenir el títol del fitxer, que es podrà modificar segons la teva preferència
    file_title = csv_file_path.split('/')[-1].replace('.csv', '')
    
    # Dades del dataframe
    columns = len(data.columns)  # Quantitat de columnes
    rows = len(data)
    min_value = data.min().min()  # El valor mínim de totes les columnes
    max_value = data.max().max()  # El valor màxim de totes les columnes
    
    # Crear contingut del fitxer de text
    content = f"""
file title  : {file_title}
data type  : string
file type  : ascii
columns     : {columns}
rows        : {rows}
ref.system  : plane
ref.units   : m
unit dist.  : 15
min. X      : 0
max. X      : 2
min. Y      : 0
max. Y      : 2
pos 'n error: unknown
resolution  : 30
min. value  : {min_value}
max. value  : {max_value}
Value units : unspecified
Value Error : unknown
flag Value  : none
flag def 'n : none
legend cats : 0
"""  
    # Escriure el contingut en un fitxer de text
    output_file_path = csv_file_path.replace('.csv', '_info.txt')
    with open(output_file_path, 'w') as file:
        file.write(content)
    
    print(f"Generated file: {output_file_path}")

# Exemple d'ús
for file in ['humidity.csv', 'vegetation.csv', 'terrain.csv', 'rivers.csv']:
    generate_txt_from_csv(file)
