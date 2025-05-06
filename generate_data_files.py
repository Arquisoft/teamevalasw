import pandas as pd
import secrets
import string

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Load the Excel file
df = pd.read_excel('alumnos2425.xlsx')

# Extract the user ID from Email
df['user'] = df['Email'].str.extract(r'(UO\d+)')

# Split 'Alumno' into 'surname' and 'name'
df[['surname', 'name']] = df['Alumno'].str.split(', ', expand=True)

# Rename 'EquipoLab' to 'group'
df['group'] = df['EquipoLab']

# if group contains EN, language is English
# if group contains ES, language is Spanish
df['language'] = df['group'].apply(
    lambda g: 'en' if isinstance(g, str) and 'EN' in g else
              ('es' if isinstance(g, str) and 'ES' in g else '')
)

df['password'] = df['user'].apply(lambda x: generate_password())

df = df[df['group'].notna()]

# Select and reorder the desired columns
data = df[['user', 'name', 'surname', 'group','language']]
# Save to a new Excel file
data.to_excel('data.xlsx', index=False)

# Save user:password pairs to a text file
with open('users.txt', 'w') as f:
    for _, row in df.iterrows():
        f.write(f"{row['user']}:{row['password']}\n")

#Create csvs for sending emails
#Spanish students
df_es = df[df['language'] == 'es']
df_es = df_es[['user', 'name', 'surname', 'password']]
df_es.to_csv('es.csv', index=False)
#English students
df_en = df[df['language'] == 'en']
df_en = df_en[['user', 'name', 'surname', 'password']]
df_en.to_csv('en.csv', index=False)