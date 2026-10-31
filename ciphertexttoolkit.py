def shift_upper(ch: str, k: int) -> str:
    if len(ch) != 1 or not ch.isupper() or not ch.isalpha():
        raise ValueError("ch must be a single uppercase letter")
    shifted = (ord(ch) - ord("A") + k) % 26
    return chr(ord("A") + shifted)


def shift_char(ch: str, k: int) -> str:
    if "A" <= ch <= "Z":
        base = "A"
    elif "a" <= ch <= "z":
        base = "a"
    else:
        return ch
    shifted = (ord(ch) - ord(base) + k) % 26
    return chr(ord(base) + shifted)


def caesar(text: str, k: int) -> str:
    parts = []
    for ch in text:
        parts.append(shift_char(ch, k))
    return "".join(parts)


def decrypt(text: str, k: int) -> str:
    return caesar(text, -k)


def get_rail_indices(length: int, num_rails: int) -> list[int]:
    if length == 0:
        return []
    if num_rails <= 1:
        return [0] * length

    result = []
    floor = 0
    step = 1

    for i in range(length):
        result.append(floor)
        if floor == num_rails - 1:
            step = -1
        elif floor == 0 and i != 0:
            step = 1
        floor += step

    return result


def rail_fence_encrypt(text: str, num_rails: int) -> str:
    if len(text) == 0 or num_rails <= 1:
        return text

    line_numbers = get_rail_indices(len(text), num_rails)

    boxes = []
    for _ in range(num_rails):
        boxes.append([])

    for i in range(len(text)):
        letter = text[i]
        box_num = line_numbers[i]
        boxes[box_num].append(letter)

    scrambled_text = ""
    for box in boxes:
        for letter in box:
            scrambled_text += letter

    return scrambled_text


def rail_fence_decrypt(ciphertext: str, num_rails: int) -> str:
    if len(ciphertext) == 0 or num_rails <= 1:
        return ciphertext

    line_numbers = get_rail_indices(len(ciphertext), num_rails)

    box_counts = [0] * num_rails
    for num in line_numbers:
        box_counts[num] += 1

    boxes = []
    for _ in range(num_rails):
        boxes.append([])

    char_index = 0
    for box_num in range(num_rails):
        how_many = box_counts[box_num]
        for _ in range(how_many):
            boxes[box_num].append(ciphertext[char_index])
            char_index += 1

    original_text = ""
    for box_num in line_numbers:
        original_text += boxes[box_num].pop(0)

    return original_text


def letter_frequency(text: str) -> dict[str, int]:
    count = {}
    for ch in text.upper():
        if "A" <= ch <= "Z":
            if ch not in count:
                count[ch] = 1
            else:
                count[ch] += 1
    return count


def crack_caesar(ciphertext: str) -> str:
    freq = letter_frequency(ciphertext)
    if not freq:
        return ciphertext

    most_frequent_letter = max(freq, key=freq.get)
    estimated_k = (ord(most_frequent_letter) - ord("E")) % 26
    return decrypt(ciphertext, estimated_k)


print("Running Block 1 Tests (Caesar)...")
assert shift_upper("D", 3) == "G"
assert shift_upper("Y", 3) == "B"
assert shift_upper("A", 0) == "A"
assert caesar("Hello, World!", 3) == "Khoor, Zruog!"
assert caesar("Hello", -3) == "Ebiil"
assert decrypt("Khoor, Zruog!", 3) == "Hello, World!"
for k in range(-30, 31):
    for t in ["", "abc", "Hello, World!", "xyz XYZ"]:
        assert decrypt(caesar(t, k), k) == t
print("Block 1 Passed!")

print("Running Block 2 Tests (Rail Fence)...")
assert get_rail_indices(6, 3) == [0, 1, 2, 1, 0, 1]
assert rail_fence_encrypt("SECRET", 3) == "SEERTC"
assert rail_fence_decrypt("SEERTC", 3) == "SECRET"

for rails in range(1, 5):
    for t in ["HELLO", "PYTHON PROGRAMMING", "SECRET MESSAGE"]:
        assert rail_fence_decrypt(rail_fence_encrypt(t, rails), rails) == t
print("Block 2 Passed!")


assert letter_frequency("HELLO") == {"H": 1, "E": 1, "L": 2, "O": 1}

secret = "THE SECRET TREASURE IS HIDDEN DEEP INSIDE THE GREEN FOREST"
scrambled = caesar(secret, 4)


print("Original Secret:  ", secret)
print("Scrambled (Key=4):", scrambled)

cracked_message = crack_caesar(scrambled)
print("Cracked (No Key!):", cracked_message)

assert cracked_message == secret
print("Block 3 Passed!")
