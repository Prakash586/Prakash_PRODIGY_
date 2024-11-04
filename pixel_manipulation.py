from PIL import Image
import numpy as np
# Function to encrypt/decrypt the image
def image_encrypt_decrypt(image_path, key, output_path):
    # Open image
    img = Image.open(image_path)
    img_array = np.array(img)
    # Flatten the 3D image array into 1D for pixel-wise manipulation
    flat_img_array = img_array.flatten()
    # Perform XOR operation with the key
    encrypted_flat_img = np.bitwise_xor(flat_img_array, key)
    # Reshape back to the original image shape
    encrypted_img_array = encrypted_flat_img.reshape(img_array.shape)
    # Convert numpy array back to an image
    encrypted_img = Image.fromarray(encrypted_img_array.astype('uint8'))
    # Save the output image
    encrypted_img.save(output_path)
    print(f"Image saved at: {output_path}")
# Main function to encrypt/decrypt based on user choice
def main():
    # Ask user for the input image path, key, and operation
    image_path = input("Enter the path of the image: ")
    output_path = input("Enter the output path for the encrypted/decrypted image: ")
    key = int(input("Enter a numeric key (0-255): "))
    
    # Check if the key is in the valid range
    if not (0 <= key <= 255):
        print("Invalid key! Please enter a value between 0 and 255.")
        return
    # Ask the user if they want to encrypt or decrypt
    choice = input("Do you want to encrypt or decrypt the image? (e/d): ").lower()
    if choice == 'e':
        print("Encrypting the image...")
    elif choice == 'd':
        print("Decrypting the image...")
    else:
        print("Invalid choice. Exiting.")
        return
    # Perform the encryption or decryption
    image_encrypt_decrypt(image_path, key, output_path)
if __name__ == "__main__":
    main()