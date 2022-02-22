import hashlib
def encrypt(text, passw):
    return " ".join([hex([int(hashlib.sha256(passw.encode("UTF-8")).hexdigest()[i:i+2], 16) for i in range(0, 64, 2)][i%32] ^ [ord(text[i]) if i < len(text) else 0 for i in range(0, len(text) if len(text) % 32 == 0 else (len(text) // 32 + 1) * 32)][i])[2:] for i in range(0, len([ord(text[i]) if i < len(text) else 0 for i in range(0, len(text) if len(text) % 32 == 0 else (len(text) // 32 + 1) * 32)]))])
def decrypt(cipher, passw):
    return "".join([chr(i) if i != 0 else "" for i in [[int(hashlib.sha256(passw.encode("UTF-8")).hexdigest()[i:i+2], 16) for i in range(0, 64, 2)][i%32] ^ [int(i, 16) for i in cipher.split(" ")][i] for i in range(0, len(cipher.split(" ")))]])