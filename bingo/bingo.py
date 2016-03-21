#!/usr/bin/env python3

import sys


class BingoCard:
    class Bingo:
        def __init__(self, type, location):
            # TODO Use Enum for type
            self.type = type
            self.location = location

        def __str__(self):
            return self.type + " in " + str(self.location)

    def __init__(self, data):
        self.data = data
        self.size = len(data)
        # Check size
        for row in data:
            if len(row) != self.size:
                raise ValueError("Data not square!")

        self.markings = [False] * self.size * self.size
        self.bingos = []

    def evaluate(self, numbers):
        # Clear everything
        self.bingos.clear()
        for i in range(0, len(self.markings)):
            self.markings[i] = False

        # Mark fields
        for number in numbers:
            for y in range(0, self.size):
                for x in range(0, self.size):
                    if number == self.data[y][x]:
                        self.markings[y * self.size + x] = True

        # Horizontal bingo
        for y in range(0, self.size):
            found = True
            for x in range(0, self.size):
                found = found and self.markings[y * self.size + x]
            if found:
                self.bingos.append(self.Bingo('horizontal', y+1))

        # Vertical bingo
        for x in range(0, self.size):
            found = True
            for y in range(0, self.size):
                found = found and self.markings[y * self.size + x]
            if found:
                self.bingos.append(self.Bingo('vertical', x+1))

        # Diagonal bingo
        found_left = True
        found_right = True
        for i in range(0, self.size):
            found_left = found_left and self.markings[i * self.size + i]
            found_right = found_right and self.markings[i * self.size
                                                        + self.size - 1 - i]
        if found_left:
            self.bingos.append(self.Bingo('diagonal', 'upper left'))
        if found_right:
            self.bingos.append(self.Bingo('diagonal', 'upper right'))

    def __str__(self):
        result = ""

        # Print bingos
        result += "Bingos:\n"
        for bingo in self.bingos:
            result += str(bingo) + '\n'

        # Get largest number
        max_len = 0
        for row in self.data:
            for number in row:
                if max_len < len(str(number)):
                    max_len = len(str(number))

        # Print unmarked
        result += "\nAll:\n"
        for row in self.data:
            result += ' '.join(map(lambda x: str(x).rjust(max_len), row)) + '\n'

        # Print marked
        result += "\nMissing:\n"
        for y in range(0, self.size):
            sep = ''
            for x in range(0, self.size):
                if self.markings[y * self.size + x]:
                    result += sep + ' ' * max_len
                else:
                    result += sep + str(self.data[y][x]).rjust(max_len)
                sep = ' '
            result += '\n'

        return result


# Must have card and number paths
if len(sys.argv) < 3:
    print("Not enough parameters!")
    exit()

# Read paths
card_path = sys.argv[1]
number_path = sys.argv[2]

# Read cards
cards = []
with open(card_path) as file:
    data = []
    for line in file:
        # empty line -> new card
        if not line or line.isspace():
            if data:
                try:
                    cards.append(BingoCard(data))
                except ValueError:
                    print("Error reading card no.", len(cards)+1)
            data = []
            continue

        # Add numbers per row
        row_rough = line.split(',')
        data.append([])
        for number in row_rough:
            try:
                data[-1].append(int(number))
            except Exception:
                pass

    if data:
        try:
            cards.append(BingoCard(data))
        except ValueError:
            print("Error reading card no.", len(cards)+1)

# Read numbers
numbers = []
with open(number_path) as file:
    for line in file:
        try:
            numbers.append(int(line.split(',')[0]))
        except Exception:
            pass

# mark all cards, look for bingo
for i in range(0, len(cards)):
    cards[i].evaluate(numbers)
    print("Card", i+1)
    print(cards[i], '\n')
