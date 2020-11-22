"""
Author: Lin Sze Khoo
Created on: 21/11/2020
Last modified on: 22/11/2020
Description: This program is a solo terminal scrabble game. Run the program and start playing.
"""

import exception

BOARD = []
DICTIONARY = []             # Stores a list of valid words
SCORES = {}                 # A map with letters as keys and scores as values
TILES = []                  # Tiles to be placed on the board
CELL_WIDTH = 3              # Width of each cell on the board
TILES_COUNT = 7             # Number of tiles to be chosen from in each turn
USED_TILES = 0              # Number of tiles used
BOARD_OCCUPIED_TILES = 0    # Number of tiles occupied on the board
TOTAL_SCORE = 0             # Total score of player

def welcomeMessage():
    """
    Prints welcome message and reads from "rules.txt" to print the game rules.
    """
    print("GOOD DAY! WELCOME TO THE SCRABBLE GAME!")
    print("-" * 50)
    print("Here are some rules:")
    rulesFile = open("rules.txt")
    for line in rulesFile:
        print(line.strip())
    rulesFile.close()

def initializeBoard(boardSize=5):
    """
    Initializes board with a default value of 5.

    :param boardSize: The board's size, between 5 and 15, defaults to 5
    :type boardSize: int, optional
    """
    assert 5 <= boardSize <= 15, "Board size should be between 5 and 15!"

    for _ in range(boardSize):
        row = []
        for _ in range(boardSize):
            row.append("")
        BOARD.append(row)

def createDictionary():
    """
    Reads from "dictionary.txt" and construct a list of valid words.
    """
    dictionaryFile = open("dictionary.txt")
    for line in dictionaryFile:
        line = line.strip()
        DICTIONARY.append(line)
    dictionaryFile.close()

def createScoreMap():
    """
    Reads from "scores.txt" and construct a map with letters as keys and scores as values.
    """
    scoreFile = open("scores.txt")
    for line in scoreFile:
        line = line.strip()
        line = line.split(" ")
        SCORES[line[0]] = int(line[1])
    scoreFile.close()

def createTiles():
    """
    Reads from "tiles.txt" and construct a list of tiles.
    """
    tilesFile = open("tiles.txt")
    for line in tilesFile:
        line = line.strip()
        TILES.append(line)
    tilesFile.close()

def padString(string, c):
    """
    Pads left and right of the input string with character c so that the length makes up the cell width.

    :param string: String to pad

    :param c: Character to pad with
    """
    global CELL_WIDTH
    string = str(string)
    remaining = CELL_WIDTH - len(string)
    remaining = remaining // 2
    string = c * remaining + string
    remaining = CELL_WIDTH - len(string)
    return string + c * remaining

def printBoard():
    """
    Prints the board.
    """
    print("\nBOARD:")
    boardColumnHeader =  "  |" + "|".join(padString(index + 1, " ") for index in range(len(BOARD))) + "|"
    boardSeparator = "--|" + "|".join(padString("", "-") for _ in range(len(BOARD))) + "|"

    print(boardColumnHeader)
    print(boardSeparator)
    
    for i in range(len(BOARD)):
        row = str(i + 1) + " " * (2 - len(str(i))) + "|"
        for j in range(len(BOARD)):
            row += padString(BOARD[i][j], " ") + "|"
        print(row)
        print(boardSeparator)

def getCurrentTiles(currentTiles):
    """
    Generates tiles for the current move.
    Only a maximum of 7 tiles are returned and should consist of the unused tiles from the previous move.

    :param currentTiles: List to contain the generated tiles.
    """
    global USED_TILES, TILES_COUNT
    while len(currentTiles) < TILES_COUNT and USED_TILES < len(TILES):
        currentTiles.append(TILES[USED_TILES])
        USED_TILES += 1

def printTiles(currentTiles):
    """
    Prints tiles for the current turn with their scores.

    :param currentTiles: List of tiles to be printed.
    """
    tiles = ""
    scores = ""

    for letter in currentTiles:
        tiles += letter + "  "
        currentScore = SCORES[letter]
        if currentScore > 9:
            scores += str(currentScore) + " "
        else:
            scores += str(currentScore) + "  "

    print("\nTiles : " + tiles)
    print("Scores: " + scores + "\n")

def isLetterFromBoard(word):
    """
    Determines whether a specific letter already exists in the board.

    :param letter: Letter to be checked.
    """
    letters = []
    for letter in word:
        for i in range(len(BOARD)):
            for j in range(len(BOARD)):
                if BOARD[i][j] == letter:
                    if not [letter, i, j] in letters:
                        letters.append([letter, i, j])
    
    if (len(letters) == 0):
        return False
    return letters

def canBeMadeWithTiles(word, currentTiles):
    tilesToCompare = currentTiles.copy()
    for letter in word:
        try:
            tilesToCompare.index(letter)
            tilesToCompare.remove(letter)
        except ValueError:
            return False
    return True

def wordIsValid(word, currentTiles):
    """
    Determines whether the input word is valid.

    :param word: Valid word with pure alphabets, exists in the dictionary list and \
    uses letters from the current tiles or existing ones on the board.

    :param currentTiles: Tiles to be used in the current turn.
    """
    # Word should not contain number, white space or special characters
    if not word.isalpha():
        return False

    # Word should be in the dictionary
    try:
        DICTIONARY.index(word)
    except ValueError:
        return False
    
    if not canBeMadeWithTiles(word, currentTiles):
        if not isLetterFromBoard(word):
            return False
    
    return True

def locationValidFormat(loc):
    """
    Determines whether the location is in valid format.
    Returns a list of [int, int, String] of the split coordinates.

    :param loc: Location string with the format of "_:_:H" or "_:_:V".
    """
    loc = loc.split(":")
    assert len(loc) == 3, "Location should be in the form of _:_:H or _:_:V !"

    for i in range(len(loc)):
        loc[i] = loc[i].strip()
        if i == 0 or i == 1:
            if loc[i].isnumeric():
                loc[i] = int(loc[i])
            else:
                raise AssertionError("Location should be numeric!")
        elif i == 2:
            if not (loc[i] == "H" or loc[i] == "V"):
                raise AssertionError("Invalid direction!")
    
    return loc

def locationIsValid(loc, word, currentTiles, firstMove):
    """
    Determines whether the input location is valid.
    Valid location is in the correct format and within the range of the board.

    :param loc: Location string to place the word in the board.

    :param word: Chosen word string for the current move.

    :param currentTiles: List of tiles to be used in the current turn.

    :param firstMove: Boolean of whether the current turn is the first move.
    """
    loc = locationValidFormat(loc)

    assert (0 < loc[0] <= len(BOARD) and 0 < loc[1] <= len(BOARD)), \
        "Please select a location within the board!"
    
    assert (loc[2] == "H" and len(word) + loc[1] - 1 <= len(BOARD)) or \
        (loc[2] == "V" and len(word) + loc[0] - 1 <= len(BOARD)), \
        "The word could not fit into the board!"

    placeTilesOnBoard(loc, word, currentTiles, firstMove)
    return True

def placeTilesOnBoard(loc, word, currentTiles, firstMove):
    """
    Places tiles of the selected word onto the board.
    Reverts and raises exception if the word does not use at least one existing tile.

    :param loc: List of selected location.

    :param word: Selected word for the current move.

    :param currentTiles: List of tiles to be used in the current turn.

    :param firstMove: Boolean of whether the current turn is the first move.
    """
    global BOARD_OCCUPIED_TILES
    existingTiles = []

    if loc[2] == "H":
        row = loc[0] - 1
        startCol = loc[1] - 1
        endCol = loc[1] + len(word) - 2
        wordIndex = 0
        for i in range(startCol, endCol + 1):
            if (BOARD[row][i] != ""):
                if (BOARD[row][i] != word[wordIndex]):
                    raise exception.TilesError("You must not overwrite existing tiles on the board!")
                else:
                    existingTiles.append(word[wordIndex])
            else:
                try:
                    currentTiles.remove(word[wordIndex])
                    BOARD_OCCUPIED_TILES += 1
                # A special case where an existing tile seems to be used but is actually not
                except ValueError:
                    if len(existingTiles) > 0:
                        for i in range(startCol, startCol + wordIndex):
                            if (BOARD[row][i] not in existingTiles):
                                BOARD[row][i] = ""
                                BOARD_OCCUPIED_TILES -= 1
                            else:
                                existingTiles.remove(BOARD[row][i])
                    else:
                        for i in range(startCol, startCol + wordIndex):
                            BOARD[row][i] = ""
                            BOARD_OCCUPIED_TILES -= 1
                    raise exception.TilesError("You must only use the existing or given tiles!")

            BOARD[row][i] = word[wordIndex]
            wordIndex += 1
        
        # Revert if no existing tile is used
        if not firstMove and len(existingTiles) == 0:
            for i in range(startCol, endCol + 1):
                BOARD[row][i] = "" 
            BOARD_OCCUPIED_TILES -= len(word)
            raise exception.TilesError("You must use at least one existing tile!")

    elif loc[2] == "V":
        col = loc[1] - 1
        startRow = loc[0] - 1
        endRow = loc[0] + len(word) - 2
        wordIndex = 0
        for i in range(startRow, endRow + 1):
            if (BOARD[i][col] != ""):
                if (BOARD[i][col] != word[wordIndex]):
                    raise exception.TilesError("You must not overwrite existing tiles on the board!")
                else:
                    existingTiles.append(word[wordIndex])
            else:
                try:
                    currentTiles.remove(word[wordIndex])
                    BOARD_OCCUPIED_TILES += 1
                # A special case where an existing tile seems to be used but is actually not
                except ValueError:
                    if len(existingTiles) > 0:
                        for i in range(startRow, startRow + wordIndex):
                            if (BOARD[i][col] not in existingTiles):
                                BOARD[i][col] = ""
                                BOARD_OCCUPIED_TILES -= 1
                            else:
                                existingTiles.remove(BOARD[i][col])
                    else:
                        for i in range(startRow, startRow + wordIndex):
                            BOARD[i][col] = ""
                            BOARD_OCCUPIED_TILES -= 1
                    raise exception.TilesError("You must only use the existing or given tiles!")

            BOARD[i][col] = word[wordIndex]
            wordIndex += 1
        
        # Revert if no existing tile is used
        if not firstMove and len(existingTiles) == 0:
            for i in range(startRow, endRow + 1):
                BOARD[i][col] = "" 
            BOARD_OCCUPIED_TILES -= len(word)
            raise exception.TilesError("You must use at least one existing tile!")

    printScore(word, existingTiles)

def getCurrentScore(word, existingTiles):  
    """
    Computes and returns the score of the current move by neglecting the existing tiles used.

    :param word: Word string for the current move.

    :param existingTiles: A list of existing tiles used.
    """
    score = 0
    for letter in word:
        if letter in existingTiles:
            existingTiles.remove(letter)
        else:
            score += SCORES[letter]
    return score

def printScore(word, existingTiles):
    """
    Computes and prints the current and total scores.

    :param word: Word string for the current move.

    :param existingTiles: A list of existing tiles used.
    """
    global TOTAL_SCORE

    currentScore = getCurrentScore(word, existingTiles)
    print("Your score for this move: " + str(currentScore))

    TOTAL_SCORE += currentScore
    print("Total score: " + str(TOTAL_SCORE))

def getLocationWithBestScore(word, existingTiles, firstMove):
    if firstMove:
        if (len(word) <= len(BOARD)):
            return ["1:1:H", getCurrentScore(word, [])]
        else:
            return None
    else:
        bestScore = 0
        bestLocation = ""
        usedTiles = []
        # Attempt to place word into the board using existing tiles
        for letterLoc in existingTiles:
            for i in range(len(word)):
                if (word[i] == letterLoc[0]):
                    if (letterLoc[1] - i < 0 and letterLoc[2] - i < 0):
                        continue

                    elif letterLoc[1] - i >= 0 and letterLoc[1] - i + len(word) - 1 < len(BOARD):
                        wordIndex = 0
                        for j in range(letterLoc[1] - i, letterLoc[1] - i + len(word)):
                            if (BOARD[j][letterLoc[2]] != "" and BOARD[j][letterLoc[2]] != word[wordIndex]):
                                break 
                            elif BOARD[j][letterLoc[2]] != "":
                                usedTiles.append(word[wordIndex])
                            wordIndex += 1
                        if wordIndex == len(word):
                            currentScore = getCurrentScore(word, usedTiles)
                            if (currentScore > bestScore):
                                bestScore = currentScore
                                bestLocation = str(letterLoc[1] - i + 1) + ":" + str(letterLoc[2] + 1) + ":V"
                        
                    elif letterLoc[2] - i >= 0 and letterLoc[2] - i + len(word) - 1 < len(BOARD):
                        wordIndex = 0
                        for j in range(letterLoc[2] - i, letterLoc[2] - i + len(word)):
                            if (BOARD[letterLoc[1]][j] != "" and BOARD[letterLoc[1]][j] != word[wordIndex]):
                                continue 
                            elif BOARD[letterLoc[1]][j] != "":
                                usedTiles.append(word[wordIndex])
                        if wordIndex == len(word):
                            currentScore = getCurrentScore(word, usedTiles)
                            if (currentScore > bestScore):
                                bestScore = currentScore
                                bestLocation = str(letterLoc[1] + 1) + ":" + str(letterLoc[2] - i + 1) + ":H"

        if bestScore == 0:
            return None
        return [bestLocation, bestScore]

def getCurrentBest(currentTiles, firstMove):
    """
    Generates move with the maximum score.

    :param currentTiles: List of tiles to be used in the current turn.

    :param firstMove: Boolean of whether the current turn is the first move.
    """
    bestWord = ""
    bestScore = 0
    bestLocation = None

    for validWord in DICTIONARY:
        if canBeMadeWithTiles(validWord, currentTiles):
            existingTiles = []
            if not firstMove:
                existingTiles = isLetterFromBoard(validWord)
                if not existingTiles:
                    continue
            locationWithScore = getLocationWithBestScore(validWord, existingTiles, firstMove)
            if locationWithScore is not None:
                if locationWithScore[1] > bestScore:
                    bestWord = validWord
                    bestScore = locationWithScore[1]
                    bestLocation = locationWithScore[0]

    return [bestWord, bestScore, bestLocation]

def playGame():
    createDictionary()
    createScoreMap()
    createTiles()
    welcomeMessage()

    # Prompts for board size
    validBoard = False
    while not validBoard:
        inputBoardSize = input("\nEnter your board size (5 - 15): ")
        try:
            if (inputBoardSize.isnumeric()):
                initializeBoard(int(inputBoardSize))
            else:
                initializeBoard()
            validBoard = True
        except AssertionError as message:
            print(message)

    printBoard()

    userInput = ""
    quit = False
    move = 1
    currentTiles = []
    getCurrentTiles(currentTiles)     # Generates tiles for the current move

    # Game ends when player quits or wins the game
    while not quit and BOARD_OCCUPIED_TILES < int(inputBoardSize) ** 2:
        printTiles(currentTiles)    
        [bestWord, bestScore, bestLocation] = getCurrentBest(currentTiles, move == 1)
        currentTilesCopy = currentTiles.copy()

        # Prompts for word
        validWord = False
        while not validWord:
            userInput = input("Enter a word: ").upper()
            if (userInput == "***"):
                quit = True
                break
            validWord = wordIsValid(userInput, currentTiles)
            currentWord = userInput
            if (not validWord):
                print("Invalid word! You must use letters from the tiles!")
        
        # Prompts for location
        validLocation = False
        while validWord and not validLocation:
            userInput = input("Enter the location of your word (_:_:H or _:_:V): ").upper()
            if (userInput == "***"):
                quit = True
                break
            try:
                validLocation = locationIsValid(userInput, currentWord, currentTiles, move == 1)
            # Assertion error is raised if requires new location input
            except AssertionError as message:
                print(message)
            # TilesError is raised if requires new word and location input
            except exception.TilesError as message:
                print(message)
                currentTiles = currentTilesCopy
                break
        
        # Prints the board if a move is successfully completed
        if (validWord and validLocation):
            print("Maximum possible score in this move is " + str(bestScore) + " using the word " + bestWord + 
            " at " + bestLocation)
            printBoard()
            move += 1
            getCurrentTiles(currentTiles)
        
        if BOARD_OCCUPIED_TILES == int(inputBoardSize) ** 2:
            print("You won the game!")
            break

    print("Hope you had fun, do come back again!")

playGame()