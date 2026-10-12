counter = 0

def game_bracket():
    global counter
    if counter < 10:
        counter += 1
        print("I")

while counter < 10:
    game_bracket()

print(f"Total counter: {counter}")
