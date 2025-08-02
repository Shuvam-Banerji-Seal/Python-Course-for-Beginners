#!/usr/bin/env python3
"""
Advanced File Techniques
Based on the original class_03.py and advanced concepts from the course.
Demonstrates file seeking, binary operations, and performance considerations.
"""

import os
import time
import pickle
import struct
from pathlib import Path

def demonstrate_file_seeking():
    """Demonstrate file seeking operations"""
    print("--- File Seeking Demonstration ---")
    
    # Create a sample file with numbered lines
    sample_content = ""
    for i in range(10):
        sample_content += f"This is line {i+1:2d} with some content.\n"
    
    filepath = 'sample_files/seek_demo.txt'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"✅ Created file with {len(sample_content)} characters")
    
    # Demonstrate different seek operations
    with open(filepath, 'r', encoding='utf-8') as f:
        print(f"📍 Initial position: {f.tell()}")
        
        # Read first line
        first_line = f.readline()
        print(f"📖 First line: {first_line.strip()}")
        print(f"📍 Position after reading first line: {f.tell()}")
        
        # Seek to beginning
        f.seek(0)
        print(f"📍 Position after seek(0): {f.tell()}")
        
        # Seek to middle of file
        middle_pos = len(sample_content) // 2
        f.seek(middle_pos)
        print(f"📍 Position after seek({middle_pos}): {f.tell()}")
        
        # Read from middle
        middle_content = f.read(50)
        print(f"📖 Content from middle: {repr(middle_content)}")
        
        # Seek to end
        f.seek(0, 2)  # 2 means from end
        print(f"📍 Position at end: {f.tell()}")
        
        # Seek backwards from end
        f.seek(-50, 2)  # 50 characters from end
        print(f"📍 Position 50 chars from end: {f.tell()}")
        end_content = f.read()
        print(f"📖 Last 50 characters: {repr(end_content)}")

def performance_comparison_with_seeking():
    """Compare performance with and without seeking"""
    print("\n--- Performance Comparison: With vs Without Seeking ---")
    
    # Create a large file for testing
    large_content = "This is a test line with some content.\n" * 10000
    filepath = 'sample_files/large_file.txt'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(large_content)
    
    print(f"📄 Created large file with {len(large_content):,} characters")
    
    # Method 1: Read entire file (without seeking)
    start_time = time.time()
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    read_all_time = time.time() - start_time
    
    # Method 2: Use seeking to read specific parts
    start_time = time.time()
    with open(filepath, 'r', encoding='utf-8') as f:
        # Read first 1000 characters
        f.seek(0)
        first_part = f.read(1000)
        
        # Read middle 1000 characters
        middle_pos = len(large_content) // 2
        f.seek(middle_pos)
        middle_part = f.read(1000)
        
        # Read last 1000 characters
        f.seek(-1000, 2)
        last_part = f.read(1000)
    
    seek_time = time.time() - start_time
    
    print(f"⏱️ Read entire file: {read_all_time:.6f} seconds")
    print(f"⏱️ Read with seeking: {seek_time:.6f} seconds")
    print(f"🚀 Seeking is {read_all_time/seek_time:.2f}x faster for partial reads")

def demonstrate_binary_operations():
    """Demonstrate binary file operations"""
    print("\n--- Binary File Operations ---")
    
    # Create binary data
    binary_data = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])  # PNG header
    binary_data += b"This is fake PNG data" + bytes(range(256))
    
    filepath = 'sample_files/binary_demo.bin'
    
    # Write binary data
    with open(filepath, 'wb') as f:
        f.write(binary_data)
    
    print(f"✅ Wrote {len(binary_data)} bytes of binary data")
    
    # Read and analyze binary data
    with open(filepath, 'rb') as f:
        # Read header
        header = f.read(8)
        print(f"📄 File header: {header.hex()}")
        
        # Check if it's a PNG file
        if header == b'\x89PNG\r\n\x1a\n':
            print("🖼️ This appears to be a PNG file!")
        
        # Read next 20 bytes
        next_data = f.read(20)
        print(f"📖 Next 20 bytes: {next_data}")
        
        # Show current position
        print(f"📍 Current position: {f.tell()}")
        
        # Read remaining data
        remaining = f.read()
        print(f"📊 Remaining bytes: {len(remaining)}")

def demonstrate_pickle_operations():
    """Demonstrate pickle serialization (from class02.py)"""
    print("\n--- Pickle Operations ---")
    
    # Create complex data structure
    data_to_pickle = {
        'name': 'Advanced File Course',
        'version': 2.0,
        'topics': ['encoding', 'modes', 'binary', 'performance'],
        'metadata': {
            'created': time.time(),
            'author': 'Python Course',
            'students': 150
        },
        'numbers': list(range(100))
    }
    
    filepath = 'sample_files/data.pkl'
    
    # Pickle the data
    start_time = time.time()
    with open(filepath, 'wb') as f:
        pickle.dump(data_to_pickle, f)
    pickle_time = time.time() - start_time
    
    print(f"✅ Pickled data in {pickle_time:.6f} seconds")
    
    # Unpickle the data
    start_time = time.time()
    with open(filepath, 'rb') as f:
        loaded_data = pickle.load(f)
    unpickle_time = time.time() - start_time
    
    print(f"✅ Unpickled data in {unpickle_time:.6f} seconds")
    print(f"📊 Data integrity check: {loaded_data == data_to_pickle}")
    print(f"📄 Loaded data keys: {list(loaded_data.keys())}")
    
    # Compare with text file approach
    import json
    text_filepath = 'sample_files/data.json'
    
    start_time = time.time()
    with open(text_filepath, 'w', encoding='utf-8') as f:
        json.dump(data_to_pickle, f)
    json_write_time = time.time() - start_time
    
    start_time = time.time()
    with open(text_filepath, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    json_read_time = time.time() - start_time
    
    print(f"\n📊 Performance Comparison:")
    print(f"   Pickle write: {pickle_time:.6f}s")
    print(f"   JSON write:   {json_write_time:.6f}s")
    print(f"   Pickle read:  {unpickle_time:.6f}s")
    print(f"   JSON read:    {json_read_time:.6f}s")
    
    # File size comparison
    pickle_size = os.path.getsize(filepath)
    json_size = os.path.getsize(text_filepath)
    print(f"   Pickle size:  {pickle_size} bytes")
    print(f"   JSON size:    {json_size} bytes")

def demonstrate_struct_operations():
    """Demonstrate struct module for binary data"""
    print("\n--- Struct Operations for Binary Data ---")
    
    # Pack different data types
    import struct
    
    # Define data
    record_id = 12345
    temperature = 23.5
    humidity = 65.2
    timestamp = int(time.time())
    sensor_name = b'TEMP_01'  # 8 bytes max
    
    # Pack data using struct
    # Format: > (big-endian), I (unsigned int), f (float), f (float), I (unsigned int), 8s (8 bytes string)
    format_string = '>IfII8s'
    packed_data = struct.pack(format_string, record_id, temperature, humidity, timestamp, sensor_name)
    
    print(f"📦 Packed data: {packed_data}")
    print(f"📏 Packed size: {len(packed_data)} bytes")
    
    # Write to binary file
    filepath = 'sample_files/sensor_data.bin'
    with open(filepath, 'wb') as f:
        f.write(packed_data)
    
    # Read and unpack
    with open(filepath, 'rb') as f:
        read_data = f.read()
        unpacked = struct.unpack(format_string, read_data)
    
    print(f"📖 Unpacked data: {unpacked}")
    print(f"   Record ID: {unpacked[0]}")
    print(f"   Temperature: {unpacked[1]:.1f}°C")
    print(f"   Humidity: {unpacked[2]:.1f}%")
    print(f"   Timestamp: {unpacked[3]}")
    print(f"   Sensor: {unpacked[4].decode('utf-8').rstrip('\\x00')}")

def demonstrate_memory_efficient_reading():
    """Show memory-efficient ways to read large files"""
    print("\n--- Memory-Efficient File Reading ---")
    
    # Create a large file
    large_filepath = 'sample_files/very_large_file.txt'
    print("📝 Creating large file...")
    
    with open(large_filepath, 'w', encoding='utf-8') as f:
        for i in range(50000):
            f.write(f"Line {i+1:05d}: This is a sample line with some content to make it longer.\n")
    
    file_size = os.path.getsize(large_filepath)
    print(f"✅ Created file of {file_size:,} bytes")
    
    # Method 1: Read line by line (memory efficient)
    print("\n🔄 Method 1: Line-by-line reading")
    start_time = time.time()
    line_count = 0
    with open(large_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line_count += 1
            if line_count % 10000 == 0:
                print(f"   Processed {line_count:,} lines...")
    
    line_time = time.time() - start_time
    print(f"✅ Processed {line_count:,} lines in {line_time:.3f} seconds")
    
    # Method 2: Read in chunks (for binary or when you need more control)
    print("\n🔄 Method 2: Chunk-based reading")
    start_time = time.time()
    chunk_size = 8192  # 8KB chunks
    total_bytes = 0
    
    with open(large_filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
    
    chunk_time = time.time() - start_time
    print(f"✅ Processed {total_bytes:,} bytes in {chunk_time:.3f} seconds")
    
    # Method 3: Read entire file (memory intensive - for comparison)
    print("\n🔄 Method 3: Read entire file (not recommended for large files)")
    start_time = time.time()
    try:
        with open(large_filepath, 'r', encoding='utf-8') as f:
            entire_content = f.read()
        entire_time = time.time() - start_time
        print(f"✅ Read {len(entire_content):,} characters in {entire_time:.3f} seconds")
        
        print(f"\n📊 Performance Summary:")
        print(f"   Line-by-line: {line_time:.3f}s (most memory efficient)")
        print(f"   Chunk-based:  {chunk_time:.3f}s (good for binary)")
        print(f"   Entire file:  {entire_time:.3f}s (memory intensive)")
        
    except MemoryError:
        print("❌ Not enough memory to read entire file!")

def demonstrate_file_context_managers():
    """Show proper file handling with context managers"""
    print("\n--- Context Managers and Resource Management ---")
    
    # Bad example (without context manager)
    print("❌ Bad example (manual file handling):")
    try:
        f = open('sample_files/manual_handle.txt', 'w', encoding='utf-8')
        f.write("This is risky!")
        # If an error occurs here, the file won't be closed!
        # raise Exception("Simulated error")
        f.close()
        print("   File handled manually (risky)")
    except Exception as e:
        print(f"   Error occurred: {e}")
        if 'f' in locals() and not f.closed:
            f.close()
            print("   Had to manually close file in exception handler")
    
    # Good example (with context manager)
    print("\n✅ Good example (context manager):")
    try:
        with open('sample_files/context_managed.txt', 'w', encoding='utf-8') as f:
            f.write("This is safe!")
            # Even if an error occurs here, the file will be closed automatically
            # raise Exception("Simulated error")
        print("   File handled with context manager (safe)")
    except Exception as e:
        print(f"   Error occurred: {e}")
        print("   File was automatically closed by context manager")
    
    # Multiple files with context manager
    print("\n✅ Multiple files with context manager:")
    with open('sample_files/source.txt', 'w', encoding='utf-8') as src, \
         open('sample_files/destination.txt', 'w', encoding='utf-8') as dst:
        src.write("Source content")
        dst.write("Destination content")
        print("   Both files handled safely")

def main():
    """Run all advanced file technique demonstrations"""
    print("🚀 Advanced File Techniques Demonstration")
    print("=" * 60)
    
    # Create sample_files directory
    Path('sample_files').mkdir(exist_ok=True)
    
    # Run all demonstrations
    demonstrate_file_seeking()
    performance_comparison_with_seeking()
    demonstrate_binary_operations()
    demonstrate_pickle_operations()
    demonstrate_struct_operations()
    demonstrate_memory_efficient_reading()
    demonstrate_file_context_managers()
    
    print("\n✅ All advanced demonstrations completed!")
    print("💡 Check the 'sample_files' directory for generated files.")
    
    # Cleanup large files to save space
    large_files = ['sample_files/large_file.txt', 'sample_files/very_large_file.txt']
    for filepath in large_files:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🧹 Cleaned up {filepath}")

if __name__ == "__main__":
    main()