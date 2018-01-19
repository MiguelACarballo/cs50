import cs50

while True:
    print("Height: ", end="")
    height = cs50.get_int()
    if height > 0 and height < 24:
        break;

spaces = height - 1
hashes = 2

for i in range(height):
    print (" " * spaces, end="")
    print ("#" * hashes)
    hashes = hashes + 1
    spaces = spaces - 1


