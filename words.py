# Open the text file and read all words into a list
with open('words.txt', 'r') as file:
    words = file.read().splitlines()

# Define the size of each group
group_size = 10

# Split the list into groups of 20 words each
groups = [words[i:i + group_size] for i in range(0, len(words), group_size)]

print("Give me a very short story using this word list. USE ALL THE WORDS in the list. It's OK not to finish the story in one go because I will let you continue writing the story. Bold the word in the list if you use it. Use those words in the list as compact as possible.")
print("The story itself should be very easy to understand and not using complicated language.")
# Print each group
for index, group in enumerate(groups):
    print(f"Group {index + 1}:")
    for word in group:
        print(word)
    print()  # Add a blank line between groups
    print("Keep writing this very short story using the new word list given. USE ALL THE WORDS in the list. It's OK not to finish the story in one go because I will let you continue writing the story. Bold the word in the list if you use it. Use those words in the list as compact as possible.")
    print("The story itself should be very easy to understand and not using complicated language.")