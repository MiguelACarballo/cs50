import cs50

while True:
    print("O hai! How much change is owed?")
    owed = cs50.get_float()
    if owed > 0:
        break;
count = 0;
round_owed = round(owed * 100);
while round_owed // 25 > 0:
    round_owed -= 25
    count += 1

while round_owed // 10 > 0:
    round_owed -= 10
    count += 1

while round_owed // 5 > 0:
    round_owed -= 5
    count += 1

while round_owed // 1 > 0:
    round_owed -= 1
    count += 1

print(count)
