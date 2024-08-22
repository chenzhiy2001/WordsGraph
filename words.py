# Open the text file and read all words into a list
with open('words.txt', 'r') as file:
    words = file.read().splitlines()

# Define the size of each group
group_size = 20

# Split the list into groups of 20 words each
groups = [words[i:i + group_size] for i in range(0, len(words), group_size)]

# Print each group
for index, group in enumerate(groups):
    print(f"Group {index + 1}:")
    for word in group:
        print(word)
    print()  # Add a blank line between groups