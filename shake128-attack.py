# Marwan Nour           marwan.nour@polytechnique.edu

import XKCP.Standalone.CompactFIPS202.Python.CompactFIPS202 as kc
import sys
import os
import time

DEBUG = True

# Helped  for byte reading from file    
def get_bytes_from_file(filename):
    if(not os.path.isfile(filename)):
        print("File not found")
        sys.exit(1)
    
    f = open(filename, "rb")
    st = f.read()
    f.close()
    return st

# Floyd
def floyd(x0, output_size):
    s = 1
    T = kc.SHAKE128(x0, output_size)
    H = kc.SHAKE128(kc.SHAKE128(x0, output_size), output_size)
    # for debugging
    i = 0
    while (H != T):
        i += 1
        if ((i % 1000) == 0):
            print("-> i = " + (str)(i))
            print(T)
            print(H)
        
        s += 1
        T = kc.SHAKE128(T, output_size)
        H = kc.SHAKE128(kc.SHAKE128(H, output_size), output_size)
    
    print("-----------------------------------------")
    print("s = " + (str)(s))
    print("-----------------------------------------")
    print(T)
    print(H)
    print("-----------------------------------------")
    
    T1 = T
    T2 = x0
    T1_p = kc.SHAKE128(T1, output_size)
    T2_p = kc.SHAKE128(T2, output_size)
    # for debugging
    j = 0
    while T1_p != T2_p:
        j += 1
        if ((j % 1000) == 0):
            print("-> j = " + (str)(j))
        
        T1 = T1_p
        T2 = T2_p
        T1_p = kc.SHAKE128(T1, output_size)
        T2_p = kc.SHAKE128(T2, output_size)

    print("Collision found")
    # if DEBUG:
    #     print(T1)
    #     print(T2)
    return (T1, T2)       


# Helper for testing the files
def test_files(file1, file2, output_size):
    res1 = kc.SHAKE128(get_bytes_from_file(file1), output_size)
    print(res1)

    res2 = kc.SHAKE128(get_bytes_from_file(file2), output_size)
    print(res2)
    return res1 == res2

# Main
def main():
    if(len(sys.argv) != 3):
        print("Invalid number of arguments")
        sys.exit(1)
    
    filename = sys.argv[1]
    output_size = (int)(sys.argv[2])
    
    # Get input file as byte array
    input_file = get_bytes_from_file(filename)
    
    start = time.time()
    # (T1, T2) = floyd(b'00', output_size)
    print("Finding collisions with: " + filename)
    (T1, T2) = floyd(input_file, output_size)
    end = time.time()
    duration = end - start

    print("T1:\t\t" + (str)(T1))
    print("T2:\t\t" + (str)(T2))
    print("Duration:\t" + (str)(duration))

    # Checking
    print()
    print("H(T1):\t\t" + (str)(kc.SHAKE128(T1, output_size)))
    print("H(T2):\t\t" + (str)(kc.SHAKE128(T2, output_size)))
    print()

    # Check output directory
    if(not os.path.isdir("collisions-" + (str)(output_size))):
        os.mkdir("collisions-" + (str)(output_size))
    
    # Change directory
    os.chdir("collisions-" + (str)(output_size))

    # # For Debugging
    # if DEBUG:
    #     print("Current directory: " + os.getcwd())

    # Check for test number, increase if file exists
    test_number = 0
    while((os.path.isfile("ex-" + (str)(test_number) + ".A")) or (os.path.isfile("ex-" + (str)(test_number) + ".B"))):
        test_number += 1

    # Write output in A
    fileA = "ex-" + (str)(test_number) + ".A"
    output_file_A = open(fileA, "wb")
    output_file_A.write(T1)
    output_file_A.close()

    # Write output in B
    fileB = "ex-" + (str)(test_number) + ".B"
    output_file_B = open(fileB, "wb")
    output_file_B.write(T2)
    output_file_B.close()

    print("DONE")

    # Debugging
    if DEBUG:
        print("T1:\t\t" + (str)(bytes(T1)))
        print("T2:\t\t" + (str)(bytes(T2)))
        
        # Checking
        print()
        print("H(T1):\t\t" + (str)(kc.SHAKE128(T1, output_size)))
        print("H(T2):\t\t" + (str)(kc.SHAKE128(T2, output_size)))
        print()

        print(fileA)
        print(fileB)
        print("File Testing:" + (str)(test_files(fileA, fileB, output_size)))
        print(open(fileA, "rb").read())
        print(open(fileB, "rb").read())
        


if __name__ == "__main__":
    main()

    # TEST 0
    # print("test")
    # print(kc.SHAKE128(bytearray("Hello", "utf-8"), 3))
    # by = get_bytes_from_file("shake128-attack.py")
    # print(kc.SHAKE128(by, 3))
    
    # TEST 1
    # (T1, T2) = floyd(b'hello', 2)
    # print(kc.SHAKE128(T1, 2))
    # print(kc.SHAKE128(T2, 2))
    # print()
    # print(test_files("shake128-attack.py", "shake128-attack.py", 2))

