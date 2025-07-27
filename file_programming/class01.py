def demo_write_mode():
    print("\n--- Mode: 'w' (Write) ---")
    try:
        with open('demo_w.txt', 'w') as f:
            f.write("This was written using 'w' mode.\n")
        print("Successfully wrote to 'demo_w.txt' using 'w' mode.")
    except Exception as e:
        print("Error with 'w' mode:", e)

def demo_append_mode():
    print("\n--- Mode: 'a' (Append) ---")
    try:
        with open('demo_a.txt', 'a') as f:
            f.write("This line was appended using 'a' mode.\n")
        print("Successfully appended to 'demo_a.txt' using 'a' mode.")
    except Exception as e:
        print("Error with 'a' mode:", e)

def demo_exclusive_mode():
    print("\n--- Mode: 'x' (Exclusive Creation) ---")
    try:
        with open('demo_x.txt', 'x') as f:
            f.write("This file was created using 'x' mode.\n")
        print("Successfully created 'demo_x.txt' using 'x' mode.")
    except FileExistsError as e:
        print("FileExistsError with 'x' mode:", e)
    except Exception as e:
        print("Other error with 'x' mode:", e)

def demo_binary_write_mode():
    print("\n--- Mode: 'wb' (Write Binary) ---")
    try:
        binary_data = bytes([72, 101, 108, 108, 111])  # "Hello"
        with open('demo_wb.bin', 'wb') as f:
            f.write(binary_data)
        print("Successfully wrote binary data to 'demo_wb.bin'.")
    except Exception as e:
        print("Error with 'wb' mode:", e)

def demo_read_plus_write_mode():
    print("\n--- Mode: 'r+' (Read and Write) ---")
    try:
        # Ensure file exists
        with open('demo_rp.txt', 'w') as f:
            f.write("Existing content.\n")

        with open('demo_rp.txt', 'r+') as f:
            original = f.read()
            f.seek(0)
            f.write("New content!\n")
            print("Original content was:", original.strip())
            print("Successfully used 'r+' to read and write.")
    except FileNotFoundError as e:
        print("FileNotFoundError with 'r+' mode:", e)
    except Exception as e:
        print("Other error with 'r+' mode:", e)

def demo_r_plus_on_nonexistent():
    print("\n--- Mode: 'r+' on Nonexistent File ---")
    try:
        with open('nonexistent_rp.txt', 'r+') as f:
            f.write("Trying 'r+' on a file that doesn't exist.\n")
    except FileNotFoundError as e:
        print("Expected error: FileNotFoundError with 'r+' on non-existent file:", e)

if __name__ == "__main__":
    demo_write_mode()
    demo_append_mode()
    demo_exclusive_mode()
    demo_binary_write_mode()
    demo_read_plus_write_mode()
    demo_r_plus_on_nonexistent()
