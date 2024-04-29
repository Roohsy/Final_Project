import random

def generate_random_instructions(num_instructions):
    instructions = []
    for _ in range(num_instructions):
        instruction_type = 'put' if random.random() < 0.4 else 'get'

        if instruction_type == 'put':
            num1 = random.randint(0, 150)
            num2 = random.randint(0, 10000)
            instructions.append(f"{instruction_type} {num1} {num2}")
        else:
            num1 = random.randint(0, 150)
            instructions.append(f"{instruction_type} {num1}")

    return instructions

def gen():
    random_instructions = generate_random_instructions(10000)
    with open('instructions.txt', 'w') as file:
        for instruction in random_instructions:
            file.write(instruction + '\n')

if __name__ == "__main__":
    gen()