import random
import time
import smtplib
from email.mime.text import MIMEText

# Simulating the "database" with a dictionary
temp_data = {}  # To store temporary guest data
users_db = {}  # To store permanent user data

# A helper function to simulate sending email (for the example, we'll just print it)
def send_verification_email(email, code):
    # Normally, you would send an email here via SMTP
    print(f"Sending verification code {code} to {email}...")

# Function to generate and send a verification code
def generate_verification_code():
    return str(random.randint(100000, 999999))

# Function to simulate QR code scan and email verification
def handle_qr_scan(bin_id):
    # Guest enters their email
    email = input("Enter your email to leave a message: ")

    # Generate and send a verification code
    verification_code = generate_verification_code()
    send_verification_email(email, verification_code)

    # Store the data temporarily
    temp_data[email] = {
        'bin_id': bin_id,
        'message': input("Enter your message: "),
        'media': input("Enter media (URL of image or video, or leave blank): "),
        'verified': False,
        'verification_code': verification_code,
        'timestamp': time.time()
    }

    # Ask user to verify email
    entered_code = input(f"Enter the verification code sent to {email}: ")

    if entered_code == verification_code:
        # Mark as verified
        temp_data[email]['verified'] = True
        print("Email verified successfully!")

        # Ask the user to confirm if they want to link their account later
        link_account = input("Do you want to create an account to save your data for future use? (yes/no): ").lower()

        if link_account == "yes":
            create_account(email)
    else:
        print("Invalid verification code. Please try again.")

# Function to create an account and link data
def create_account(email):
    if email in temp_data and temp_data[email]['verified']:
        username = input("Create a username for your account: ")
        password = input("Create a password: ")

        # Store user data permanently
        users_db[email] = {
            'username': username,
            'password': password,
            'messages': [temp_data[email]['message']],
            'media': [temp_data[email]['media']],
            'timestamp': time.time()
        }

        print(f"Account created successfully! Welcome, {username}!")

        # Transfer temporary data to the permanent account
        del temp_data[email]
    else:
        print("Invalid or unverified email. Please try again.")

# Main function to simulate the flow
def main():
    print("Welcome to SeeIT!")
    bin_id = input("Scan the QR Code (enter the bin ID): ")

    # Handle QR scan and email verification
    handle_qr_scan(bin_id)

    # Display permanent user data (if any)
    print("Permanent Users Database:")
    for email, data in users_db.items():
        print(f"Email: {email} - Username: {data['username']}")

# Run the simulation
if __name__ == "__main__":
    main()
