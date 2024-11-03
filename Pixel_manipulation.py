from PIL import Image
import numpy as np

def encrypt_image(input_image_path, output_image_path, key):
    # Open the image and convert it to RGB mode if it's not already
    image = Image.open(input_image_path).convert("RGB")
    image_array = np.array(image)
    
    # Encrypt the image by adding the key to each RGB channel
    encrypted_array = (image_array + key) % 256
    encrypted_image = Image.fromarray(encrypted_array.astype(np.uint8))
    
    # Save the encrypted image
    encrypted_image.save(output_image_path)
    print(f"Image encrypted and saved as {output_image_path}")

def decrypt_image(encrypted_image_path, output_image_path, key):
    # Open the encrypted image and convert it to RGB mode
    image = Image.open(encrypted_image_path).convert("RGB")
    image_array = np.array(image)
    
    # Decrypt the image by subtracting the key from each RGB channel
    decrypted_array = (image_array - key) % 256
    decrypted_image = Image.fromarray(decrypted_array.astype(np.uint8))
    
    # Save the decrypted image
    decrypted_image.save(output_image_path)
    print(f"Image decrypted and saved as {output_image_path}")

# User input
input_image_path = input("Enter the path to the input image: ")
encrypted_image_path = "encrypted_image.png"
decrypted_image_path = "decrypted_image.png"
key = int(input("Enter an encryption key (integer value): "))

# Encrypt the image
encrypt_image(input_image_path, encrypted_image_path, key)

# Decrypt the image
decrypt_image(encrypted_image_path, decrypted_image_path, key)