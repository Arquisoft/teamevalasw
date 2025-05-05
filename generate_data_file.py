import pandas as pd

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

# Select and reorder the desired columns
result = df[['user', 'name', 'surname', 'group','language']]

#remove registers with empty group
result = result[result['group'].notna()]

# Save to a new Excel file
result.to_excel('data.xlsx', index=False)
