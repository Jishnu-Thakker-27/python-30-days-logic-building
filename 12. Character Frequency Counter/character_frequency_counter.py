word = input("Write Any One Word: ").lower()
result = {}

for letter in word:
    result[letter] = word.count(letter)

print(result)
