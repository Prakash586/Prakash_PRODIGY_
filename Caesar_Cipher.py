def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        # Check if character is an uppercase letter
        if char.isupper():
            encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
        # Check if character is a lowercase letter
        elif char.islower():
            encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
        # If it's neither, keep the character as it is (spaces, punctuation, etc.)
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        # Check if character is an uppercase letter
        if char.isupper():
            decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
        # Check if character is a lowercase letter
        elif char.islower():
            decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
        # If it's neither, keep the character as it is (spaces, punctuation, etc.)
        else:
            decrypted_text += char
    return decrypted_text

# User input
text = input("Enter the text: ")
shift = int(input("Enter the shift value: "))

# Encrypt and display the result
encrypted_text = encrypt(text, shift)
print("Encrypted text:", encrypted_text)

# Decrypt and display the result
decrypted_text = decrypt(encrypted_text, shift)
print("Decrypted text:", decrypted_text)