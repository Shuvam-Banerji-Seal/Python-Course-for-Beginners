#!/usr/bin/env python3
"""
Basic File Operations Examples
Demonstrates fundamental file operations with different modes.
Based on the original class01.py from the course.
"""

import os
import time

def demo_write_mode():
    """Demonstrate 'w' mode - Write (destructive)"""
    print("\n--- Mode: 'w' (Write) ---")
    try:
        with open('sample_files/demo_w.txt', 'w', encoding='utf-8') as f:
            f.write("This was written using 'w' mode.\n")
            f.write("This mode creates new files or overwrites existing ones.\n")
        print("✅ Successfully wrote to 'demo_w.txt' using 'w' mode.")
        
        # Show the content
        with open('sample_files/demo_w.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"📖 Content: {content.strip()}")
            
    except Exception as e:
        print(f"❌ Error with 'w' mode: {e}")

def demo_append_mode():
    """Demonstrate 'a' mode - Append (safe addition)"""
    print("\n--- Mode: 'a' (Append) ---")
    try:
        # First write
        with open('sample_files/demo_a.txt', 'a', encoding='utf-8') as f:
            f.write("First line appended using 'a' mode.\n")
        print("✅ First append successful")
        
        # Second write (adds to existing content)
        with open('sample_files/demo_a.txt', 'a', encoding='utf-8') as f:
            f.write("Second line appended using 'a' mode.\n")
        print("✅ Second append successful")
        
        # Show accumulated content
        with open('sample_files/demo_a.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"📖 Accumulated content:\n{content}")
            
    except Exception as e:
        print(f"❌ Error with 'a' mode: {e}")

def demo_exclusive_mode():
    """Demonstrate 'x' mode - Exclusive creation"""
    print("\n--- Mode: 'x' (Exclusive Creation) ---")
    
    # Clean up any existing file first
    test_file = 'sample_files/demo_x.txt'
    if os.path.exists(test_file):
        os.remove(test_file)
    
    try:
        # First attempt - should succeed
        with open(test_file, 'x', encoding='utf-8') as f:
            f.write("This file was created using 'x' mode.\n")
        print("✅ Successfully created file using 'x' mode.")
        
        # Second attempt - should fail
        with open(test_file, 'x', encoding='utf-8') as f:
            f.write("This won't work!")
            
    except FileExistsError as e:
        print(f"❌ Expected FileExistsError: {e}")
        print("💡 'x' mode prevents accidental overwrites!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def demo_binary_write_mode():
    """Demonstrate 'wb' mode - Write binary"""
    print("\n--- Mode: 'wb' (Write Binary) ---")
    try:
        # Create some binary data
        binary_data = bytes([72, 101, 108, 108, 111])  # "Hello" in ASCII
        
        with open('sample_files/demo_wb.bin', 'wb') as f:
            f.write(binary_data)
        print(f"✅ Successfully wrote binary data: {binary_data}")
        
        # Read it back in binary mode
        with open('sample_files/demo_wb.bin', 'rb') as f:
            read_data = f.read()
            print(f"📖 Read back: {read_data}")
            print(f"📝 As text: {read_data.decode('utf-8')}")
            
    except Exception as e:
        print(f"❌ Error with 'wb' mode: {e}")

def demo_read_plus_write_mode():
    """Demonstrate 'r+' mode - Read and write"""
    print("\n--- Mode: 'r+' (Read and Write) ---")
    try:
        # First, ensure file exists with some content
        with open('sample_files/demo_rp.txt', 'w', encoding='utf-8') as f:
            f.write("Original content that we'll modify.")
        
        # Now use r+ mode
        with open('sample_files/demo_rp.txt', 'r+', encoding='utf-8') as f:
            # Read the original content
            original = f.read()
            print(f"📖 Original content: '{original}'")
            
            # Move cursor back to the beginning
            f.seek(0)
            
            # Overwrite part of the content
            f.write("MODIFIED")
            print("✅ Successfully used 'r+' to read and write.")
        
        # Show the result
        with open('sample_files/demo_rp.txt', 'r', encoding='utf-8') as f:
            modified = f.read()
            print(f"📖 Modified content: '{modified}'")
            
    except FileNotFoundError as e:
        print(f"❌ FileNotFoundError with 'r+' mode: {e}")
        print("💡 'r+' mode requires the file to exist!")
    except Exception as e:
        print(f"❌ Other error with 'r+' mode: {e}")

def demo_r_plus_on_nonexistent():
    """Show what happens with 'r+' on non-existent file"""
    print("\n--- Mode: 'r+' on Nonexistent File ---")
    try:
        with open('sample_files/nonexistent_rp.txt', 'r+', encoding='utf-8') as f:
            f.write("Trying 'r+' on a file that doesn't exist.\n")
    except FileNotFoundError as e:
        print(f"❌ Expected error: {e}")
        print("💡 'r+' mode requires the file to exist first!")

def demonstrate_file_positions():
    """Show how file cursor positions work with different modes"""
    print("\n--- File Cursor Positions ---")
    
    # Create a test file
    test_content = "Line 1\nLine 2\nLine 3\n"
    with open('sample_files/position_test.txt', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # Show different starting positions
    modes_and_positions = [
        ('r', 'beginning'),
        ('a', 'end'),
        ('w', 'beginning (after truncating)'),
        ('r+', 'beginning')
    ]
    
    for mode, description in modes_and_positions:
        if mode == 'w':
            # Special case for 'w' mode since it truncates
            with open('sample_files/position_test.txt', 'w', encoding='utf-8') as f:
                f.write(test_content)  # Restore content
                position = f.tell()
            print(f"Mode '{mode}': cursor at position {position} ({description})")
        else:
            with open('sample_files/position_test.txt', mode, encoding='utf-8') as f:
                position = f.tell()
                print(f"Mode '{mode}': cursor at position {position} ({description})")

def performance_comparison():
    """Compare performance of different file operations"""
    print("\n--- Performance Comparison ---")
    
    # Create test data
    test_data = "This is a test line.\n" * 1000
    
    # Test write performance
    start_time = time.time()
    with open('sample_files/perf_test.txt', 'w', encoding='utf-8') as f:
        f.write(test_data)
    write_time = time.time() - start_time
    
    # Test read performance
    start_time = time.time()
    with open('sample_files/perf_test.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    read_time = time.time() - start_time
    
    # Test append performance
    start_time = time.time()
    with open('sample_files/perf_test.txt', 'a', encoding='utf-8') as f:
        f.write("Appended line.\n")
    append_time = time.time() - start_time
    
    print(f"📊 Performance Results:")
    print(f"   Write: {write_time:.6f} seconds")
    print(f"   Read:  {read_time:.6f} seconds")
    print(f"   Append: {append_time:.6f} seconds")
    print(f"   File size: {len(test_data)} characters")

def main():
    """Run all demonstrations"""
    print("🐍 Basic File Operations Demonstration")
    print("=" * 50)
    
    # Create sample_files directory if it doesn't exist
    os.makedirs('sample_files', exist_ok=True)
    
    # Run all demonstrations
    demo_write_mode()
    demo_append_mode()
    demo_exclusive_mode()
    demo_binary_write_mode()
    demo_read_plus_write_mode()
    demo_r_plus_on_nonexistent()
    demonstrate_file_positions()
    performance_comparison()
    
    print("\n✅ All demonstrations completed!")
    print("💡 Check the 'sample_files' directory to see the created files.")

if __name__ == "__main__":
    main()