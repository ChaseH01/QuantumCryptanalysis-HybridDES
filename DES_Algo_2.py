'''
    -DES Encryption/Decryption
    -Author: Chase hurwitz
    -This code accepts an email, uses it to generate a random key, and then checks if that email already has existing IP, IP inverse table by lookup in a simple
    JSON file. If not, the program generates a random IP, IP inverse table and stores that user and their tables as a dictionary in the JSON file. Next, we run
    DES Encryption on their provided plaintext (must be 32 bytes/characters) and then decrypt the CT to demonstrate successful decryption as well.
'''

import hashlib
import random
import time
import json
import os

# =================
# Global variables
# =================
PERM_DB_FILE = "perm_tables.json" #for data persistence

DES_EXPANSION_TABLE = [
    31, 0, 1, 2, 3, 4,
    3, 4, 5, 6, 7, 8,
    7, 8, 9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0]

# S boxes
S = [
        #S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],

        #S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],

        #S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],

        #S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],

        #S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],

        #S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],

        #S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],

        #S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

# =========================
# 1) KEY GENERATION
# =========================

def key_generation(email, perm_table):
    # 1 hash the email to get 256 bits (32 bytes)
    hash_bytes = hashlib.sha256(email.encode('utf-8')).digest()  # 32 bytes
    
    # 2 convert the 32 bytes into a flat list of 256 bits
    key_bits = bytes_to_bits(hash_bytes)
    
    # 3 split the 256 bits into 8 segments (each 32 bits)
    segments = []
    for i in range(8):
        segments.append(key_bits[i*32:(i+1)*32])
    
    # 4 concatenate the segments into 4 blocks of 64 bits using the specified indices:
    block1 = segments[0] + segments[2]
    block2 = segments[1] + segments[3]
    block3 = segments[4] + segments[6]
    block4 = segments[5] + segments[7]

    #5 apply the permutation function here on each of these blocks:
    permuted_block1 = apply_permutation(block1, perm_table)
    permuted_block2 = apply_permutation(block2, perm_table)
    permuted_block3 = apply_permutation(block3, perm_table)
    permuted_block4 = apply_permutation(block4, perm_table)

    #6 combine into 8 segment blocks
    key_blocks = []
    for block in [permuted_block1, permuted_block2, permuted_block3, permuted_block4]:
        # Each block is 64 bits long, so we spplit each in half
        first_half = block[:32]
        second_half = block[32:]
        key_blocks.append(first_half)
        key_blocks.append(second_half)

    return key_blocks

# =========================
# 2) MESSAGE PROCESSING: 
#  - PERMUTATION TABLES
# =========================
def generate_perm_unperm_tables():
    indices = list (range(64))
    random.shuffle(indices)
    IP = indices[:] #take a slice

    # calculate the inverse
    IP_inv = [0]*64 #empty list of 64 zeros
    for i, val in enumerate(IP): 
        IP_inv[val] = i #swap index and value back to original
    
    return IP, IP_inv


def apply_permutation(bit_list, perm_table):
    """
    perm_table must be the same length as bit_list (64 bits)
    """
    result = []
    for i in range(len(perm_table)):
        result.append(bit_list[perm_table[i]])
    return result

def process_message(message, perm_table):
        # 1. Convert the message (assumed 32 characters = 256 bits) to bytes and then to a flat list of bits.
    message_bytes = message.encode("utf-8")
    message_bits = bytes_to_bits(message_bytes)
    
    # 2. Split the 256 bits into 8 segments (each 32 bits)
    segments = []
    for i in range(8):
        segment = message_bits[i*32:(i+1)*32]
        segments.append(segment)

    block1 = segments[0] + segments[2] #make 4 blocks according to diagram
    block2 = segments[1] + segments[3]
    block3 = segments[4] + segments[6]
    block4 = segments[5] + segments[7]
    
    # 4. apply the initial permutation on each 64-bit block using the provided perm_table.
    permuted_block1 = apply_permutation(block1, perm_table)
    permuted_block2 = apply_permutation(block2, perm_table)
    permuted_block3 = apply_permutation(block3, perm_table)
    permuted_block4 = apply_permutation(block4, perm_table)
    
    # 5. breaak each permuted 64-bit block into two 32-bit blocks, creating a total of 8 segments.
    message_segments = []
    for block in [permuted_block1, permuted_block2, permuted_block3, permuted_block4]:
        first_half = block[:32]
        second_half = block[32:]
        message_segments.append(first_half)
        message_segments.append(second_half)
    
    
    # 7. Return the list of 8 segments.
    return message_segments

# =========================
# 3) ENCRYPTION PROCESS: 
#  - bits to bytes and vice versa
#  - XOR function
#  - Expansion Function
#  - S-boxes
#  - encyrption
# =========================
def bytes_to_bits(byte_data):
    bit_list = []
    for byte in byte_data:
        bits = bin(byte)[2:].zfill(8)  # Convert to binary, remove "0b", pad with zeros
        for bit in bits:
            currBit = int(bit)
            bit_list.append(currBit)
    return bit_list

def bits_to_bytes(bit_data):
    """
    Assumes len(bit_list) is a multiple of 8.
    """
    byte_list = bytearray()
    for i in range(0, len(bit_data), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bit_data[i + j]
        byte_list.append(byte)
    return byte_list

def xor_bits(a, b):
    result = []
    for i in range(len(a)):
        if a[i] == b[i]:
            result.append(0)  # If bits are the same, XOR is 0
        else:
            result.append(1)  # If bits are different, XOR is 1
    return result

def expansion_32_to_48(bits):
    ''' assumes that bits is 32 bits long (indeces 0,31 inclusive)'''

    expanded_bits = []
    for i in DES_EXPANSION_TABLE:
        expanded_bits.append(bits[i])  # Append the bit at the specified index
    print("Expanded_Bits now at length 48: ", expanded_bits)
    return expanded_bits

def sbox_application(bits):
    ''' assumes that bits is 48 bits long (indeces 0,47 inclusive)'''

    output_32_bits = []
    for i in range(8):
        input_6_bits = bits[i*6:(i+1)*6]
        
        row = (input_6_bits[0] << 1) | input_6_bits[5]
        col = (input_6_bits[1] << 3) | (input_6_bits[2] << 2) | (input_6_bits[3] << 1) | input_6_bits[4]

        sbox_val = S[i][row][col]

        # Convert sbox_val into 4 bits
        val_bits = [
            (sbox_val >> 3) & 1,
            (sbox_val >> 2) & 1,
            (sbox_val >> 1) & 1,
            sbox_val & 1,
        ]
        output_32_bits.extend(val_bits)
    print("After going through sbox (now 32 bits): ", output_32_bits)
    return output_32_bits

def encryption_feistel(message_segments, key_blocks):
    """
    Given message_segments and key_blocks, each a list of 8 segments (32 bits each), encrypt in the order of
    1. Expansion
    2. XOR
    3. sbox
    4. concatentate
    """
    ciphertext = []
    
    # There are 4 pairs: indices: [0,1], [2,3], [4,5], [6,7]
    for i in range(4):
        left  = message_segments[2 * i]
        right = message_segments[2 * i + 1]
        
        # Expand the right half from 32 to 48 bits
        expanded_right = expansion_32_to_48(right)
        
        # use the key block corresponding to the right halvr's index
        key_block = key_blocks[2 * i + 1]   
        
        # Expand the key  from 32 to 48 bits
        expanded_key = expansion_32_to_48(key_block)
        
        # XOR the expanded right with the expanded key.
        xor_result = xor_bits(expanded_right, expanded_key)
        
        # Pass the result through the S-box transformation (48 bits -> 32 bits
        sbox_out = sbox_application(xor_result) 
        
        # XOR the S-box output with the saved left half
        new_left = xor_bits(left, sbox_out)
        
        # Form the ciphertext pair by concatenating new_left and the original right
        pair_ciphertext = right + new_left #we swap at the end to make it easier to pass through for decryption tho

        ciphertext.extend(pair_ciphertext)
    
    return ciphertext

# =========================
#
# 4) DECRYPTION PROCESS: 
#
# =========================

def decryption_feistel(ciphertext_bits, key_blocks, perm_inv):
    """
    Decrypt a ciphertext bascically the same we encrypt PT
    """
    recovered_plaintext = []
    
    for i in range(4):
        # Extract the 64-bit ciphertext pair.
        pair = ciphertext_bits[i * 64 : (i + 1) * 64]
        R = pair[:32]
        Lprime = pair[32:]
        
        # Expand R to 48 bits.
        expanded_R = expansion_32_to_48(R) #we use R instaed of L here because to form our CT, we swapped the pair at the veyr end
        
        # Use the key block corresponding to the right half of the pair
        key_block = key_blocks[2 * i + 1] 
        expanded_key = expansion_32_to_48(key_block)
        
        # XOR the expanded R with the expanded key
        xor_result = xor_bits(expanded_R, expanded_key)
        
        # Pass the result through the S-box transformation
        sbox_out = sbox_application(xor_result)
        
        # Recover the original left half: L = Lprime XOR sbox_out
        recovered_L = xor_bits(Lprime, sbox_out)
        
        # Reassemble the plaintext pair in the original order: (L, R)
        recovered_L_and_R = recovered_L + R
        permuted_concatenation_PT = apply_permutation(recovered_L_and_R, perm_inv)
        recovered_plaintext.extend(permuted_concatenation_PT)
    
        # Split into 8 segments of 32 bits
    segments = [recovered_plaintext[i*32:(i+1)*32] for i in range(8)]
    
    # Define the desired new order:
    order = [0, 2, 1, 3, 4, 6, 5, 7]
    
    # Reassemble the segments in the new order that matches how we originally paired the segments
    reorganized = []
    for index in order:
        reorganized.extend(segments[index])

    return reorganized


# =========================
#
# 5) GET USER INPUT: 
#
# =========================

def get_user_input():
    print("\n Welcome to DES Encryption/Decryption. Created by Chase Hurwitz") 
    
    # Prompt for user email.
    email = input("Enter your email: ").strip()
    if not email:
        print("default email used because there was an error with yours: john.doe@IES.org")
        email = "john.doe@IES.org"
    
    # Prompt for a 32-character plaintext message.
    plaintext_str = input("Enter a 32-character plaintext message: ").strip()
    if len(plaintext_str) != 32:
        default_text = "0123456789ABCDEF0123456789ABCDEF"
        print("Message must be exactly 32 characters. Using default:")
        print(default_text)
        plaintext_str = default_text

    return email, plaintext_str


# ====================================================
#
# 6) IMPLEMENT DATA PERSISTENCY WITH A SIMPLE JSON FILE: 
#
# ====================================================
def load_perm_tables():
    #Load the dictionary {email: {"IP": [...], "IP_inv": [...]}} from a JSON file
    if os.path.exists(PERM_DB_FILE):
        with open(PERM_DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {} #make it

def save_perm_tables(data):
    #Save the permutation tables dictionary to a JSON file
    with open(PERM_DB_FILE, "w") as f:
        json.dump(data, f)
        print(f"Saved permutation tables to {PERM_DB_FILE}.") #debuger

def get_or_create_perm_tables_for_user(email):
    data = load_perm_tables()

    if email in data:  # Reuse existing IP and IP_inv
        IP_table = data[email]["IP"]
        IP_inv = data[email]["IP_inv"]

    else:  # Generate new IP_table, IP_inv for this user
        IP_table, IP_inv = generate_perm_unperm_tables()
        data[email] = {
            "IP": IP_table,
            "IP_inv": IP_inv
        }

        save_perm_tables(data)# Save to JSON file
    return IP_table, IP_inv


# ====================================================
#
# 7) MAIN FUNCTION RUNS OUR CODE
#
# ====================================================

def main():

    #1 get user input
    email, message = get_user_input()

    print('\n Message:  ', message )

    #2 Generate a permutation table for 64-bit blocks
    perm_table, perm_inv = get_or_create_perm_tables_for_user(email)

    #3 Process the plaintext message into 8 segments (32 bits each)
    message_segments = process_message(message, perm_table)
    print("\nProcessed Message Segments:")
    for i, seg in enumerate(message_segments):
        print(f"Segment {i}: {seg}")
    
    #4 Generate key blocks from the email using the same permutation table
    key_blocks = key_generation(email, perm_table)
    print("\nKey Blocks:")
    for i, block in enumerate(key_blocks):
        print(f"Key Block {i}: {block}")
    
    #5 encrypt the message using our Feistel-style encryption function
    ciphertext_bits = encryption_feistel(message_segments, key_blocks)

    ciphertext_bytes = bits_to_bytes(ciphertext_bits)


    print("\n ============ ENCRYPTING ============")
    time.sleep(1.5)

    print("\nCiphertext (hex):")
    print(ciphertext_bytes.hex())
        
    print("\n ============ DECRYPTING =============")
    time.sleep(1.5)

    # 6 Decrypt the ciphertext
    recovered_bits = decryption_feistel(ciphertext_bits, key_blocks, perm_inv)

    
    recovered_bytes = bits_to_bytes(recovered_bits)

    try:
        recovered_text = recovered_bytes.decode("utf-8")
    except UnicodeDecodeError:
        recovered_text = repr(recovered_bytes)

    print("\nRecovered Plaintext:")
    print(recovered_text)
    
    if recovered_text.strip() == message:
        print("\nSUCCESS: Decrypted text matches the original!")
    else:
        print("\nERROR: Decrypted text does not match the original!")


if __name__ == "__main__":
    main()
