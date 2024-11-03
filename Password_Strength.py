import re

def check_password_strength(password):
    # Initialize the score and feedback list
    score = 0
    feedback = []
    
    # Check length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")
    
    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    # Check for numbers
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one number.")

    # Check for special characters
    if re.search(r'[@$!%*?&]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one special character (e.g., @$!%*?&).")

    # Provide overall feedback
    if score == 5:
        feedback.append("Your password is strong.")
    elif 3 <= score < 5:
        feedback.append("Your password is moderate. Try adding more variety to make it stronger.")
    else:
        feedback.append("Your password is weak. Consider adding uppercase letters, numbers, and special characters.")
    
    # Display feedback
    print("\nPassword Strength Feedback:")
    for comment in feedback:
        print("-", comment)

# User input
password = input("Enter your password to assess its strength: ")
check_password_strength(password)
