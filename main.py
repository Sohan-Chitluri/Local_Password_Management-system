import json
import os
import random
import hashlib

def check_or_create_json_file(filename):
     if not os.path.exists(filename):
        data = {
            "sequences": [],
            "website": [],
            "username": [],
            "base_hash": [],
            "sequence_hash": [],
            "length_of_password":[]
        }
        print(f"Created new JSON file: {filename}")
        sequence_generator(data)  # Pass data to sequence_generator
        save_data_to_file(data, filename)
     else:
        print(f"JSON file already exists: {filename}")
        with open(filename, 'r') as f:
            data = json.load(f)
     return data

def sequence_generator(data):              
    for _ in range(25):
        number = random.randint(10**20, (10**21) - 1)
        data["sequences"].append(number)

def save_data_to_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to gather user inputs
def gather_user_inputs(filename, R_or_N):
    website = False
    username = input("Enter your username:")
    retry_count = 0  
    max_retries = 3  

    if R_or_N in ["r", "R"]:
        while not website and retry_count < max_retries:
            entered_website = input("Website:")
            website = check_website_existence(filename, entered_website)
            if not website:
                retry_count += 1
                print(f"Attempt {retry_count}/{max_retries}. Website not found.")

        if retry_count == max_retries and not website:
            print("Max retries reached. Would you like to Retrieve a password or make a new one")
            return gather_user_inputs(filename, Retrieval_or_New())  

    elif R_or_N in ["n", "N"]:
        website = input("Website:")

    favorite_color = input("What's your favorite color?:")
    code_word = input("Code_word:")
    incorrect_input = True

    while incorrect_input:
        Correct_details = input("Confirm you have entered correct details (y/N):")
        if Correct_details in ["y", "Y"]:
            incorrect_input = False
            return username, website, favorite_color, code_word
        elif Correct_details in ["n", "N"]:
            print("You can refill details now")
            return gather_user_inputs(filename, R_or_N)
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def Retrieval_or_New():
     R_or_N = input("Retrieval of password or Making a New password (r/n)")
     retry_count = 0  
     max_retries = 5
     while R_or_N not in ["r","R","n","N"] and retry_count < max_retries:
            if R_or_N not in ["r","R","n","N"]:
               retry_count += 1
               print(f"Attempt {retry_count}/{max_retries}. Invalid Input.")
               Retrieval_or_New()
     return R_or_N

def length_of_password(data):
    length = -1  
    while length < 8 or length > 20:
        length = int(input("length_of_password (8-20): "))  
        if 8 <= length <= 20:
            data["length_of_password"].append(length)
        else:
            print("Please enter a valid length between 8 and 20.")



def generate_answers(username, website, favorite_color, code_word):
    answers = []
    # Generate 5 different answers
    answers.append(username + website + favorite_color)  
    answers.append(website[2:3] + favorite_color[4:5] + code_word)
    answers.append(f"{username}_{website}")       
    answers.append(f"{favorite_color}_{website}")        
    answers.append(f"{username[:3]}{favorite_color}{website[-3:]}")  
    
    return answers


def check_website_existence(filename, website):
        
    existing_websites = data["website"]

    
    # Check if website exists
    if website in existing_websites:
        print(f"You do have an account for: {website}")
        return website
    else:
          # Check for similar websites (typos)
          Accuracy=70
          probable_websites=[]
          for w in existing_websites:
               Acc_counter=0
               for i in range(min(len(website), len(w))):
                    if website[i]==w[i]:
                         Acc_counter+=1
               if (Acc_counter/len(website))*100>Accuracy:
                    probable_websites.append(w)
          if len(probable_websites)!=0:
               for j in range(len(probable_websites)):
                    print(f"{j}){probable_websites[j]}")
                    if len(probable_websites)>1:
                         Number_of_website=input("Enter the number of the website")
                         return probable_websites[Number_of_website]
                    else:
                         return probable_websites[0]
          else:
               print("No such website")
               return False
          del probable_websites  

def First_Hash_generator(answers, username, website, R_or_N):
     if R_or_N in ["N" ,"n"]:
          selected_Answers=random.choice(answers)
          creation_sequence=random.choice(data["sequences"])
          hashed_value = hashlib.sha256(selected_Answers.encode()).hexdigest()
          creation_hash = hashlib.sha256(str(creation_sequence).encode()).hexdigest()
          data["username"].append(username)
          data["website"].append(website)
          data["base_hash"].append(hashed_value)
          data["sequence_hash"].append(creation_hash)
          temp_website_index=-1
          for l in range(len(answers)):
               if (data["base_hash"][temp_website_index] == hashlib.sha256(answers[l].encode()).hexdigest()):
                    return temp_website_index,l
          print(hashed_value)
          print(hashed_value)

     elif R_or_N in ["r" ,"R"]:
          for k in range(len(data["website"])):
               if data["website"][k]==website:
                    temp_website_index=k


          for l in range(len(answers)):
               if (data["base_hash"][temp_website_index] == hashlib.sha256(answers[l].encode()).hexdigest()):
                    return temp_website_index,l

def sequence_finder(website_index,R_or_N):
#     if R_or_N in ["r" ,"R"]:
     for k in data["sequences"]:
          if hashlib.sha256(str(k).encode()).hexdigest()==data["sequence_hash"][website_index]:
               return k
#     elif R_or_N in ["n" ,"N"]:
#          pass
# Transformation_Algorithm_list

     #Convert the character to its ASCII value.Divide by 26.Add the remainder to the ASCII value of a letter or special character.
def ascii_mod_transform(char, base='A'):
    ascii_val = ord(char)
    mod_val = ascii_val % 26
    new_char = chr(ord(base) + mod_val)
    return new_char
def ascii_mod_transform_2(char, base='0'):
    ascii_val = ord(char)     
    mod_val = ascii_val % 26
    new_char = chr(ord(base) + mod_val)
    return new_char
    # ASCII transformation: shifts the ASCII value of a character
def ascii_shift(character, shift_value=7):
   return chr((ord(character) + shift_value) % 128)

# Binary left shift transformation
def binary_left_shift(character):
    """Perform a binary left shift on the character's ASCII value."""
    if not isinstance(character, str) or len(character) != 1:
        # Return the ASCII value of the last character of the input
        return sum(ord(c) for c in str(character))  # Return the sum of ASCII values of the input characters

    char_value = ord(character)

    # Perform a binary left shift by 1
    shifted_value = (char_value << 1) % 128
    
    # Check if the output is a valid string, number, or special character
    if not (32 <= shifted_value <= 126):  # Check if it's a printable ASCII character
        return sum(ord(c) for c in str(character))  # Return the sum of ASCII values of the input characters
    
    return chr(shifted_value)

def binary_right_shift(character):
    """Perform a binary left shift on the character's ASCII value."""
    if not isinstance(character, str) or len(character) != 1:
        # Return the ASCII value of the last character of the input
        return sum(ord(c) for c in str(character))  # Return the sum of ASCII values of the input characters

    char_value = ord(character)

    # Perform a binary left shift by 1
    shifted_value = (char_value >> 1) % 128
    
    # Check if the output is a valid string, number, or special character
    if not (32 <= shifted_value <= 126):  # Check if it's a printable ASCII character
        return sum(ord(c) for c in str(character))  # Return the sum of ASCII values of the input characters
    
    return chr(shifted_value)

def rotate_character_fixed(char, value=3):
    if char.isdigit():
        return chr((ord(char) - 48 + value) % 10 + 48)  # Rotate digits
    if char.islower():
        return chr((ord(char) - 97 + value) % 26 + 97)
    return char

# def ascii_increment(char):
#      if char.isdigit():
#           char = chr((int(char) + 1 - 0) % 10 + 48)  
#      return chr((ord(char) + 1 - 97) % 26 + 97) if char.islower() else chr((ord(char) + 1 - 65) % 26 + 65)


# XOR transformation on ASCII values
def xor_with_number(character):
     xor_value = 5  # You can change this value as needed

     if character.isdigit():
        result = (ord(character) - 48) ^ fixed_xor_value  # Subtract 48 to shift '0' to 0
        return chr((result % 10) + 48)  # Map back to ASCII character
     else:
        # Perform XOR for letters
        return chr(ord(character) ^ xor_value)
#binary_inversion
def binary_inversion(character):
     return chr(~ord(character) & 0xFF)  # Invert bits and keep within 8 bits

def binary_xor_fixed(character):
    fixed_xor_value = 2
    return chr(ord(character) ^ fixed_xor_value)  # XOR with fixed value

def Transformation_Algorithm(char, transform_order):
     
    if transform_order == 0:
        return ascii_mod_transform(char, base='A')
    elif transform_order == 1:
        return ascii_mod_transform_2(char, base='0')
    elif transform_order == 2:
        return ascii_shift(char, 7)
    elif transform_order == 3:
        return binary_left_shift(char)
    elif transform_order == 4:
        return binary_right_shift(char)
    elif transform_order == 5:
        return rotate_character_fixed(char)
    elif transform_order == 6:
        return toggle_even_odd(char)
    elif transform_order == 7:
        return xor_with_number(char)
    elif transform_order == 8:
        return binary_inversion(char)
    elif transform_order == 9:
        return binary_xor_fixed(char)
    else:
        return char

def password_generation(Answer_position, Algo_sequence, answers, website_index):
     hash_object = hashlib.blake2s()
     hash_object.update(answers[Answer_position].encode('utf-8'))
     counter = 0
     Final_password = ""
     while counter < data["length_of_password"][website_index]:
        transformed_initial = hash_object.hexdigest()
        Final_password += str(Transformation_Algorithm(transformed_initial[counter], Algo_sequence))
        counter += 1
     return Final_password
     del Final_password
def main():
     global data
     json_filename = "password.json"  
     data=check_or_create_json_file(json_filename)

     R_or_N=Retrieval_or_New()
     length_of_password(data)
     username, website, favorite_color, code_word = gather_user_inputs(json_filename,R_or_N)
     print(f"Username: {username}, Website: {website}, Favorite Color: {favorite_color}") #Test Case code
     answers= generate_answers(username, website, favorite_color, code_word)
     website_index, Answer_position=First_Hash_generator(answers, username, website, R_or_N)
     Algo_sequence=sequence_finder(website_index,R_or_N)
     print(password_generation(Answer_position,Algo_sequence,answers,website_index))
main()
