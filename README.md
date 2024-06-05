# TicTacToeMultiplayer

Protocol Explanation:

Data Format:
Data consists of four parts separated by hyphens (-):
x (integer): X-coordinate

y (integer): Y-coordinate

yourturn (string) if yourturn=="yourturn": Client's turn.

Any other value: Opponent's turn.

playing (string): Represents the game state.

"True": Game is ongoing.

"False": Game has ended (win or draw).

Receive Data: It attempts to receive one byte of data at a time from the server using sock.recv(1)

Assemble Complete Message: A loop accumulates the received bytes (temp = sock.recv(1)) until it encounters "!", signifying the end of a message.

Decode and Split Data: The received data is decoded from bytes and then split into a list using '-'

Process Data: Individual components (x, y, yourturn, and playing) are extracted and used to update the game state:
The grid object is updated with the opponent's move at the specified coordinates (grid.set_cell_value(x, y, 'X')). This happens only if that square on the grid is empty

The turn variable is set to True if it's the client's turn based on the yourturn flag.

The game_over attribute of the grid object is set to True if the playing flag indicates the game has ended.


How I completed the project: 
1. Initially, I made the game without any sort of client-server based communication to build a base and made sure my algorithms were correct for the tictactoe game
2. After creating the game without any communication, I implemented into my game client-server communication and added a data communication protocol
3. Added an option to continue playing multiple rounds
