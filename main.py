import os
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
from src.env_crawler import EnvCrawler 
from src.ec_elgamal import ECElgamal, ellipticcurve
from typing import Dict

def encrypt() -> dict:
    pathfile = input("Please insert your .env file you want to encrypt: ")
    
    env = EnvCrawler(pathfile)
    env.read_file()
    key_val = env.get_key_val()

    ec = ECElgamal()
    ec.generate_key_from_input()

    new_key_val = {}

    for key in key_val:
      val = key_val[key]
      val_encoded = val.encode("latin-1")
      c1, c2 = ec.encrypt(val_encoded)

      new_key_val[key] = (c1.to_bytes().hex(), l2b(c2).hex())
    
    env.set_key_val(new_key_val)
    env.write_file()

def decrpyt() -> Dict:
    pathfile = input("Please insert your .env you want to decrypt: ")
    
    env = EnvCrawler(pathfile)
    env.read_file()
    key_val = env.get_key_val()

    ec = ECElgamal()
    ec.generate_key_from_input()

    new_key_val = {}

    for key in key_val:
      val = eval(key_val[key])

      c1 = bytes.fromhex(val[0])
      c2 = bytes.fromhex(val[1])

      c1 = ellipticcurve.PointJacobi.from_bytes(curve=ec.get_eliptic_curve(), data=c1)
      c2 = b2l(c2)

      decrypted = ec.decrypt(c1, c2)
      decrypted = decrypted.decode("latin-1")
      new_key_val[key] = decrypted

    env.set_key_val(new_key_val)
    env.write_file(decrypt=True)

def menu() -> None:
    print("Welcome to secure env")
    print("What do you want to do?")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")

def main():
    menu()
    print("Input only the number")
    your_input = input(">> ")

    while your_input not in ['1', '2', '3']:
        print("Wrong input!")
        print("Please input the correct input")
        your_input = input(">> ")
    
    if your_input == '1':
        encrypt()
    elif your_input == '2':
        decrpyt()
    elif your_input == '3':
        print("Thank you for using secure-env")
        exit(0)

if __name__ == "__main__":
    main()