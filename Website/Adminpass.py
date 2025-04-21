from werkzeug.security import generate_password_hash

# Create a hashed password for the admin user
hashed_password = generate_password_hash('123')  # Replace 'admin_password' with the desired password
print(hashed_password)  # This will print the hashed password
