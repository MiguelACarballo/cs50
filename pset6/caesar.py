import cs50
import sys

key = int(sys.argv[1])

print("plaintext: ", end="")
text = cs50.get_string()
cypher = ""

for i in text:
    if str.isalpha(i):
        if str.isupper(i):
            fooText = ord(i)
            cypher += chr((((fooText + key) - 65) % 26) + 65)
        else:
            fooText = ord(i)
            cypher += chr((((fooText + key) - 97) % 26) + 97)
    else:
        cypher += i

print("ciphertext")
print(cypher)
