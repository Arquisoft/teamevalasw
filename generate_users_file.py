import pandas as pd
import secrets
import string

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_user_pass(input_xlsx, output_txt):
    # Read the Excel file
    df = pd.read_excel(input_xlsx, engine='openpyxl')

    # Check if 'user' column exists
    if 'user' not in df.columns:
        raise ValueError("The Excel file must contain a 'user' column.")

    # Generate passwords
    with open(output_txt, 'w') as f:
        for user in df['user'].dropna():
            password = generate_password()
            f.write(f"{user}:{password}\n")

    print(f"User:Password pairs written to {output_txt}")

# Example usage
generate_user_pass("data.xlsx", "users.txt")
