"""
Author: Lin Sze Khoo
Created on: 21/11/2020
Last modified on: 23/11/2020
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

    :returns padded string
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

    # Generates a maximum of 7 tiles and uses the previous unused tiles
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

def areLettersFromBoard(letterList):
    """
    Determines whether the letters already exists in the board.

    :param letterList: A list of letters to be checked.

    :returns a list of list, each consists of an alphabet with the x and y coordinates on the board, 
    if all letters exist in the board, false otherwise.
    """
    letters = []
    # Ensures that the tiles for all the letters are found
    foundLetters = [False for _ in range(len(letterList))]

    for m in range(len(letterList)):
        for i in range(len(BOARD)):
            for j in range(len(BOARD)):
                if BOARD[i][j] == letterList[m]:
                    # More than one tile for a letter might exist
                    if not [letterList[m], i, j] in letters:
                        foundLetters[m] = True
                        letters.append([letterList[m], i, j])
    
    if (len(letters) == 0):
        return False
    else:
        try:
            foundLetters.index(False)
            return False
        except ValueError:
            return letters

def canBeMadeWithTiles(word, currentTiles):
    """
    Determines whether the word can be constructed using the tiles given.

    :param word: A word string to be checked.
    
    :param currentTiles: A list of tiles to be checked against.

    :returns True if all of the words can be constructed with the given tiles, otherwise
    returns a list of tiles to be checked against the board and another with the tiles to be used.
    """
    tilesToCompare = currentTiles.copy()
    toCheckInBoard = []
    tilesToUse = []

    for letter in word:
        # Looks for letters in the tiles
        try:
            tilesToCompare.index(letter)
            tilesToCompare.remove(letter)
            tilesToUse.append(letter)
        
        # Stores letters that are not found to be checked if they exist in the board
        except ValueError:
            toCheckInBoard.append(letter)
    
    if (len(toCheckInBoard) > 0):
        return [toCheckInBoard, tilesToUse]

    return True

def wordIsValid(word, currentTiles, firstMove):
    """
    Determines whether the input word is valid.

    :param word: Valid word with pure alphabets, exists in the dictionary list and \
    uses letters from the current tiles or existing ones on the board.

    :param currentTiles: Tiles to be used in the current turn.

    :param firstMove: Boolean of whether the current turn is the first move.

    :returns True if the word only contains letters from the given tiles or existing tiles from the board.
    """
    # Word should not contain number, white space or special characters
    if not word.isalpha():
        return False

    # Word should be in the dictionary
    try:
        DICTIONARY.index(word)
    except ValueError:
        return False
    
    # Word in the first move should not contain any external tiles.
    if firstMove:
        if canBeMadeWithTiles(word, currentTiles):
            return True
        return False

    # Following move must use given tiles and at least one existing tile
    allLettersFromTiles = canBeMadeWithTiles(word, currentTiles)

    # All letters are found in tiles and some from the board.
    if (allLettersFromTiles == True):
        existingTiles = areLettersFromBoard(word)

    # Some letters are not found in tiles but are found from the board.
    elif isinstance(allLettersFromTiles, list):
        existingTiles = areLettersFromBoard(allLettersFromTiles[0])
    
    if isinstance(existingTiles, list):
        return True
    
    return False

def locationValidFormat(loc):
    """
    Determines whether the location is in valid format.
    Returns a list of [int, int, String] of the split coordinates.

    :param loc: Location string with the format of "_:_:H" or "_:_:V".

    :returns a list of split location if the input is a valid location.

    :raises AssertionError when the coordinates are not numeric or the direction is invalid.
    """
    loc = loc.split(":")
    assert len(loc) == 3, "Location should be in the form of _:_:H or _:_:V !"

    for i in range(len(loc)):
        loc[i] = loc[i].strip()

        # Checks the coordinates
        if i == 0 or i == 1:
            if loc[i].isnumeric():
                loc[i] = int(loc[i])
            else:
                raise AssertionError("Location should be numeric!")
        
        # Checks the direction
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

    :returns True if the location is valid and word is successfully placed into the board.

    :raises AssertionError if the location or the word is out of the range of the board.
    """
    loc = locationValidFormat(loc)

    # Ensures that the coordinates are within the board
    assert (0 < loc[0] <= len(BOARD) and 0 < loc[1] <= len(BOARD)), \
        "Please select a location within the board!"
    
    # Ensures that the word can fit into the board
    assert (loc[2] == "H" and len(word) + loc[1] - 1 <= len(BOARD)) or \
        (loc[2] == "V" and len(word) + loc[0] - 1 <= len(BOARD)), \
        "The word could not fit into the board!"

    # Attempts to place the word into the board
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

    :raises TilesError if an existing tile is overwritten, an existing tile is not used,
    or when neither an existing nor a given tile is used.
    """
    global BOARD_OCCUPIED_TILES
    existingTiles = []  # Keeps track of existing tile to avoid counting the scores in

    # If word is to be placed horizontally
    if loc[2] == "H":
        row = loc[0] - 1
        startCol = loc[1] - 1
        endCol = loc[1] + len(word) - 2
        wordIndex = 0

        for i in range(startCol, endCol + 1):
            # Ensures that no existing tile is overwritten
            if (BOARD[row][i] != ""):
                if (BOARD[row][i] != word[wordIndex]):
                    raise exception.TilesError("You must not overwrite existing tiles on the board!")
                else:
                    existingTiles.append(word[wordIndex])
            else:
                try:
                    # Removes used tile from the list
                    currentTiles.remove(word[wordIndex])
                    BOARD_OCCUPIED_TILES += 1

                # The tile exist in the board but is at a different location
                except ValueError:
                    if len(existingTiles) > 0:
                        # Restore the board into previous state without removing existing tiles
                        for i in range(startCol, startCol + wordIndex):
                            if (BOARD[row][i] not in existingTiles):
                                BOARD[row][i] = ""
                                BOARD_OCCUPIED_TILES -= 1
                            else:
                                existingTiles.remove(BOARD[row][i])
                    else:
                        # Restore the board into previous state
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

    # If word is to be placed vertically
    elif loc[2] == "V":
        col = loc[1] - 1
        startRow = loc[0] - 1
        endRow = loc[0] + len(word) - 2
        wordIndex = 0

        for i in range(startRow, endRow + 1):
            # Ensures that no existing tile is overwritten
            if (BOARD[i][col] != ""):
                if (BOARD[i][col] != word[wordIndex]):
                    raise exception.TilesError("You must not overwrite existing tiles on the board!")
                else:
                    existingTiles.append(word[wordIndex])
            else:
                try:
                    # Removes used tile from the list
                    currentTiles.remove(word[wordIndex])
                    BOARD_OCCUPIED_TILES += 1

                # The tile exist in the board but is at a different location
                except ValueError:
                    if len(existingTiles) > 0:
                        # Restore the board into previous state without removing existing tiles
                        for i in range(startRow, startRow + wordIndex):
                            if (BOARD[i][col] not in existingTiles):
                                BOARD[i][col] = ""
                                BOARD_OCCUPIED_TILES -= 1
                            else:
                                existingTiles.remove(BOARD[i][col])
                    else:
                        # Restore the board into previous state
                        for i in range(startRow, startRow + wordIndex):
                            BOARD[i][col] = ""
                            BOARD_OCCUPIED_TILES -= 1
                    raise exception.TilesError("You must only use the existing or given tiles!")
            
            # Places letter into the board
            BOARD[i][col] = word[wordIndex]
            wordIndex += 1
        
        # Revert if no existing tile is used
        if not firstMove and len(existingTiles) == 0:
            for i in range(startRow, endRow + 1):
                BOARD[i][col] = "" 
            BOARD_OCCUPIED_TILES -= len(word)
            raise exception.TilesError("You must use at least one existing tile!")
    
    # Prints the scores for the current turn
    printScore(word, existingTiles)

def getCurrentScore(word, existingTiles):  
    """
    Computes and returns the score of the current move by neglecting the existing tiles used.

    :param word: Word string for the current move.

    :param existingTiles: A list of existing tiles used.

    :returns score for the current word.
    """
    score = 0
    for letter in word:
        # Removes letters that have been accounted for
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

def getLocationWithBestScore(word, existingTiles, newTiles, firstMove):
    """
    Looks for valid location with the highest score to fit the given word into the board.

    :param word: A word string to fit into the board.
    
    :param existingTiles: A list of existing tiles on the board which should be used.

    :param newTiles: A list of tiles which are supposed to make up the word other than those on the board.
    
    :param firstMove: Boolean of whether the current turn is the first move.

    :returns: None if no location is found, otherwise returns a list with location string with its score.
    """
    # If current turn is the first move
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
                    
                    # Attempt to place word horizontally
                    elif letterLoc[1] - i >= 0 and letterLoc[1] - i + len(word) - 1 < len(BOARD):
                        wordIndex = 0
                        for j in range(letterLoc[1] - i, letterLoc[1] - i + len(word)):
                            # If an existing tile is overwritten
                            if (BOARD[j][letterLoc[2]] != "" and BOARD[j][letterLoc[2]] != word[wordIndex]):
                                break

                            # If an existing tile is used
                            elif BOARD[j][letterLoc[2]] != "":
                                usedTiles.append(word[wordIndex])
                                wordIndex += 1
                            
                            # If a tile given is used
                            elif word[wordIndex] in newTiles:
                                newTiles.remove(word[wordIndex])
                                wordIndex += 1
                            
                            # The tile is from the board but at another position
                            else:
                                break
                        
                        # Successful attempt
                        if wordIndex == len(word):
                            currentScore = getCurrentScore(word, usedTiles)
                            if (currentScore > bestScore):
                                bestScore = currentScore
                                bestLocation = str(letterLoc[1] - i + 1) + ":" + str(letterLoc[2] + 1) + ":V"
                    
                    # Attempt to place word vertically
                    elif letterLoc[2] - i >= 0 and letterLoc[2] - i + len(word) - 1 < len(BOARD):
                        wordIndex = 0
                        for j in range(letterLoc[2] - i, letterLoc[2] - i + len(word)):
                            # If an existing tile is overwritten
                            if (BOARD[letterLoc[1]][j] != "" and BOARD[letterLoc[1]][j] != word[wordIndex]):
                                break

                            # If an existing tile is used
                            elif BOARD[letterLoc[1]][j] != "":
                                usedTiles.append(word[wordIndex])
                                wordIndex += 1

                            # If a tile given is used
                            elif word[wordIndex] in newTiles:
                                wordIndex += 1
                            
                            # The tile is from the board but at another position
                            else:
                                break
                        
                        # Successful attempt
                        if wordIndex == len(word):
                            currentScore = getCurrentScore(word, usedTiles)
                            if (currentScore > bestScore):
                                bestScore = currentScore
                                bestLocation = str(letterLoc[1] + 1) + ":" + str(letterLoc[2] - i + 1) + ":H"
        
        # No valid location is found
        if bestScore == 0:
            return None
        return [bestLocation, bestScore]

def getCurrentBest(currentTiles, firstMove):
    """
    Generates move with the maximum score.

    :param currentTiles: List of tiles to be used in the current turn.

    :param firstMove: Boolean of whether the current turn is the first move.

    :returns a list consisting of word with maximum score, the score, and its location in the board.
    """
    bestWord = None
    bestScore = 0
    bestLocation = None

    for validWord in DICTIONARY:
        # If the current turn is the first move
        if firstMove:
            # If not all the letters are found from the tiles
            if isinstance(canBeMadeWithTiles(validWord, currentTiles), list):
                continue
            existingTiles = []
            newTiles = []
        
        else:
            checkedTiles = canBeMadeWithTiles(validWord, currentTiles)

            # If all letters are found from the tiles, checks if any letters exist in the board
            if (checkedTiles == True):
                existingTiles = areLettersFromBoard(validWord)

            # If some letters are found from the tiles, checks if those exist in the board
            elif isinstance(checkedTiles, list):
                existingTiles = areLettersFromBoard(checkedTiles[0])

            # If no existing tile is used
            if not isinstance(existingTiles, list):
                continue
            
            # If all letters are found from the tiles and some from the board
            elif (checkedTiles == True):
                newTiles = currentTiles.copy()
            
            # If some letters are found from the tiles and the rest are found from the board
            else:
                newTiles = checkedTiles[1]
        
        # Attempts to get a valid location with the highest score to place the word
        locationWithScore = getLocationWithBestScore(validWord, existingTiles, newTiles, firstMove)
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
    # Prompts until a valid board size is entered
    while not validBoard:
        inputBoardSize = input("\nEnter your board size (5 - 15): ")
        try:
            if (inputBoardSize.isnumeric()):
                initializeBoard(int(inputBoardSize))
            else:
                # Uses default value
                initializeBoard()
            validBoard = True

        # When board size is beyond the range
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

        # No possible move is found
        if (bestWord is None):
            print("No possible move found!")
            break

        # Prompts for word
        validWord = False
        # Prompts until a valid word is entered
        while not validWord:
            userInput = input("Enter a word: ").upper()
            if (userInput == "***"):
                quit = True
                break

            validWord = wordIsValid(userInput, currentTiles, move == 1)
            currentWord = userInput
            if (not validWord):
                print("Invalid word! You must use letters from the tiles!")
        
        # Prompts for location
        validLocation = False
        # Prompts until a valid location is entered
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
                # Restores the tiles that might have been removed
                currentTiles = currentTilesCopy
                break
        
        # Prints the board if a move is successfully completed
        if (validWord and validLocation):
            print("Maximum possible score in this move is " + str(bestScore) + " using the word " + bestWord + 
            " at " + bestLocation)
            printBoard()
            move += 1
            getCurrentTiles(currentTiles)
        
        # If all the tiles are occupied
        if BOARD_OCCUPIED_TILES == int(inputBoardSize) ** 2:
            print("You won the game!")
            break

    print("Hope you had fun, do come back again!")

playGame()