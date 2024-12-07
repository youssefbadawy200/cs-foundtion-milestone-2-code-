import random
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(start=50, end=200):
    primes = [n for n in range(start, end) if is_prime(n)]
    return random.choice(primes)

def find_primitive_root(p):
    if p == 2:
        return 1
    required_set = {num for num in range(1, p) if is_prime(num)}
    for g in range(2, p):
        actual_set = {pow(g, power, p) for power in range(1, p)}
        if len(actual_set) == p - 1: 
            return g
    return None

def generate_keys(p, g):
    private_key = random.randint(2, p - 2)
    h = pow(g, private_key, p)    
    return (p, g, h), private_key  

def encrypt(public_key, message):
    p, g, h = public_key
    k = random.randint(2, p - 2)  
    c1 = pow(g, k, p)            
    c2 = (message * pow(h, k, p)) % p  
    return c1, c2

def decrypt(private_key, p, c1, c2):
    s = pow(c1, private_key, p)   
    s_inv = pow(s, -1, p)         
    message = (c2 * s_inv) % p   
    return message


if __name__ == "__main__":
    p = generate_prime()
    g = find_primitive_root(p)
    
    if g is None:
        print(f"Failed to find a primitive root for prime number {p}")
        exit()
    
    print(f"Generated prime number (p): {p}")
    print(f"Primitive root (g): {g}")
    print("\nGenerating keys...")
    public_key, private_key = generate_keys(p, g)
    print("Public Key (p, g, h):", public_key)
    print("Private Key:", private_key)
    
    while True:
        print("\nOptions:")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")
        choice = input("Choose an option (1 or 2 or 3): ")
        
        if choice == "1":
            message = int(input(f"Enter a message (as an integer less than {p}): "))
            if message <= 0 or message >= p:
                print(f"Message must be more than 0 and less than {p}.")
            else:
                c1, c2 = encrypt(public_key, message)
                print(f"Encrypted message: (c1={c1}, c2={c2})")
        
        elif choice == "2":
            try:
                c1 = int(input("Enter c1: "))
                c2 = int(input("Enter c2: "))
                decrypted_message = decrypt(private_key, public_key[0], c1, c2)
                print(f"Decrypted message: {decrypted_message}")
            except ValueError:
                print("make sure that c1 and c2 are integers.")
        
        elif choice == "3":
            print("you left the menu")
            break
        
        else:
            print("Please select 1, 2, or 3.")
