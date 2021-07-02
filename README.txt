Greetings, user!

This is a program written to simulate baseball games between fictional teams, 
built by Derek Ward-Colston and programmed by Griffin Lynch. It was written to use 
Python 3.8.2, but it doesn't do anything fancy so I imagine it'll work for a lot of 
prior and future versions.

To run the program, you'll need two .csv files. There are at least two in the folder, 
called 'PittPanthers.csv' and 'DCDorks.csv'. To simulate a game where the Panthers play against the Dorks,
you would run this command from your command prompt:

python BaseballSimulator.py PittPanthers.csv DCDorks.csv

If you had a .csv file for the Chicago Cubs, named 'ChicagoCubs.csv' and one for the 
White Sox, named 'ChicagoWhiteSox.csv', you would run this command:

python BaseballSimulator.py ChicagoCubs.csv ChicagoWhiteSox.csv

The first team will be the home team, so they will bat second.




Here are a list of the commands and explanations of what they do:
	- quit: ends the program without exporting any game data
	- help: lists out the commands
	- game_report: gives a report of the game (score, inning, outs, and a description of the current at-bat)
	- positions: reports what players (jersey number and name) are at what positions 
		on the team currently playing Defense
	- stats <team_name> <player_jersey_number>: Gives the numerical statistics of the player with the given jersey 
		number on the given team
	- substitute_player <position> <fresh_player_number>: Replaces the player on the field with
		the given jersey number with a fresh player (with the second jersey number)
	- simulate_pitch: Runs one iteration of the simulation
	- sp: shorthand for simulate_pitch
	- simulate_at_bat: Runs the simulation until the batter is no longer the batter
	- sb: shorthand for simulate_at_bat
	- simulate_half_inning: Runs the simulation until the batting team is no longer the batting team
	- sh: shorthand for simulate_half_inning
	- simulate_inning: Runs the simulation until the top of the next inning
	- si: simulate_inning shorthand
	- simulate_game: Runs until the end of an inning greater than 8 where the scores are unequal









Now that you understand how to run the program, let's talk about how the CSV files are 
structured. You should be able to open them in any basic text editor (like Notepad).
Microsoft Excel should work, but make sure any edits are still saved as .csv since .xls
files are weird and complicated.

The player's stats are separated by commas as follows:
Name, Handedness, Jersey Number, Hit Strength, Throw Strength, Hit Consistency, Throw Consistency,
	Pitch Judgement, Speed, Reaction, Confidence, Cool, Risk Tolerance, Righty/Lefty Killer

There are no restrictions on the name except it should only have normal alphanumeric characters (especially no commas!)

Handedness must be either 'R' or 'L' or 'S' (switch hitter).

The jersey number must be unique on the team. There cannot be two number 12's or else things will get weird.

Risk tolerance is in a range from 0 to 25

Righty/Lefty Killer is in a range from -10 to 10. If -10 they're a great lefty killer, if 10 they're a great righty killer

Other than that the stats are in the range 0 to 20



The next several lines are the base coach stats. They are separated by commas as follows:
Name, id_num, Risk Tolerance

Same deal for these people's names

id_num must be unique within the team as well. It's never printed anywhere so you can assign them arbitrarily

Risk Tolerance is in a range from 0 to 60


The third to last line determines the positions at the start of the game, so it must include exactly 9 numbers. 
They refer to the jersey numbers of the players starting in a particular position. In order, those positions are:
Pitcher, Catcher, 1st Base, 2nd Base, 3rd Base, Short Stop, Left Field, Center Field, Right Field

The second to last line determines the batting order at the start of the game also by jersey number.
It can be any length.

The last line must be only 2 numbers, and they are the id_numbers of the base coaches. The first is 
assigned to 1st base, the 2nd is assigned to be the 3rd base coach.