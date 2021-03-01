from game import TicTacToe
""" 
This initalizes the game with size three, this is the only size supported at the
moment. The plans where to try if we could make it larger but instead we spent
the weekend looking for bugs and it turned out that we had written the function
check_dig() with faulty logic and thus redering the enitre algorithm useless.
Also it is only possible for player 1 to start, the AI AInar isn't able to start
since the code is hardcoded towards the case when player1 (you) begin. It is a
quite buggy and messy code, but it gets the job done, feel free to try it.
"""

game = TicTacToe(size=3)
game.start()
