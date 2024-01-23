# A baseball sim program conceptualized by Derek Ward-Colston and Griffin Lynch
# Python code by Griffin Lynch

# program arguments: team_sheet_1, team_sheet_2
# note the first team will be the Home team

import sys
import csv
import random

# Setting up a data structure to keep track of each player's stats
# The values assigned are defaults
class Player:
    name = "default_player"     # The player's name, a string
    handedness = "R"            # ONLY "L" or "R" or "S" (switch)
    jersey_number = 0           # The player's jersey number [0, 99]
    hit_str = 0                 # Hitting Strength [0, 20]
    throw_str = 0               # Throw Strength [0, 20]
    hit_cons = 0                # Hitting Consistency [0, 20]
    throw_cons = 0              # Throw Consistency [0, 20]
    pitch_judgement = 0         # How good they are at reading pitches [0, 20]
    speed = 0                   # The player's run speed [0, 20]
    reaction = 0                # The player's reaction speed [0, 20]
    confidence = 0              # The player's confidence (variable) [0, 20]
    cool = 0                    # The player's cool [0, 20]
    risk_tolerance = 0          # The player's risk tolerance [0, 25]
    rl_killer = 0               # Whether the player is a righty/lefty killer [-10, 10]
                                # -10 would be a perfect lefty killer
                                # 10 is a perfect righty killer

    def __init__(self, name, handedness, jersey_number, hit_str, throw_str, hit_cons, throw_cons, pitch_judgement, speed, reaction, confidence, cool, risk_tolerance, rl_killer):
        self.name = name
        self.handedness = handedness
        self.jersey_number = jersey_number
        self.hit_str = hit_str
        self.throw_str = throw_str
        self.hit_cons = hit_cons
        self.throw_cons = throw_cons
        self.pitch_judgement = pitch_judgement
        self.speed = speed
        self.reaction = reaction
        self.confidence = confidence
        self.cool = cool
        self.risk_tolerance = risk_tolerance
        self.rl_killer = rl_killer

# Coaches that factor into stealing bases
class BaseCoach:
    name = "default_bench_coach"    # Just the guy's name
    id_num = 0                      # the guy's unique (to the team) id number
    risk_tolerance = 0              # His risk tolerance [0, 60]

    def __init__(self, name, id_num, risk_tolerance):
        self.name = name
        self.id_num = id_num
        self.risk_tolerance = risk_tolerance

# Data structure for a team
class BaseballTeam:
    city = "default_team_city"      # Where the team is from
    name = "default_team_name"      # The name of the team
    score = 0                       # The number of runs this team has gotten
    players = []                    # The list of Players
    batting_order = []             # The order in which the players bat
    base_coaches = []               # The list of BaseCoaches
    # These will all be initialized to Player variables by the csv's starting lineup
    pitcher = 0
    catcher = 0
    first_baseman = 0
    second_baseman = 0
    third_baseman = 0
    shortstop = 0
    left_fielder = 0
    center_fielder = 0
    right_fielder = 0
    first_base_coach = 0
    third_base_coach = 0

    def __init__(self, city, name, players, base_coaches):
        self.city = city
        self.name = name
        self.players = players
        self.base_coaches = base_coaches

    # Returns the player with the given jersey number, or 0 if not found
    def getPlayer(self, jersey_number):
        for player in self.players:
            if player.jersey_number == jersey_number:
                return player

        return 0

    # Returns the base coach with the given id number, or 0 if not found
    def getCoach(self, id_num):
        for coach in self.base_coaches:
            if coach.id_num == id_num:
                return coach

        return 0

# Creating the other relevant variables
home_score = 0
away_score = 0
home_at_bat = 0
away_at_bat = 0
inning = 1
team_at_bat = 0
fielding_team = 0
outs = 0
strikes = 0
balls = 0
# To be initialized later
home_team = 0
away_team = 0
player_at_bat = 0
player_on_first = 0
player_on_second = 0
player_on_third = 0


# Reads in a team's data from a csv file and returns a BaseballTeam object
def readTeam(csv_filename):
    # Open the file
    csvfile = open(csv_filename, newline='')
    file_reader = csv.reader(csvfile)

    # The first line is just descriptive
    file_reader.__next__()

    # The second line tells us the team name
    line = file_reader.__next__()
    city_name = line[0]
    team_name = line[1]

    # Skip two lines
    file_reader.__next__()
    file_reader.__next__()

    # The third line tells us the number of players and base coaches on the team
    line = file_reader.__next__()
    num_players = int(line[0])
    num_base_coaches = int(line[1])

    # Skip two more lines
    file_reader.__next__()
    file_reader.__next__()

    # Now import all of the players
    players = []

    for x in range(0, num_players):
        line = file_reader.__next__() # read in the line and then extract the data
        # A very gross line that just creates a player object
        new_player = Player(line[0], line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7]), int(line[8]), int(line[9]), int(line[10]), int(line[11]), int(line[12]), int(line[13]))
        players.append(new_player)

    # Eat two lines, then do the same for each base coach
    file_reader.__next__()
    file_reader.__next__()

    base_coaches = []

    for x in range(0, num_base_coaches):
        line = file_reader.__next__()
        new_base_coach = BaseCoach(line[0], line[1], line[2])
        base_coaches.append(new_base_coach)

    # Create our Team object
    myTeam = BaseballTeam(city_name, team_name, players, base_coaches)

    # Eat two more lines, then set up our starting lineup using the next line (by jersey number)
    file_reader.__next__()
    file_reader.__next__()
    line = file_reader.__next__()
    myTeam.pitcher = myTeam.getPlayer(int(line[0]))
    myTeam.catcher = myTeam.getPlayer(int(line[1]))
    myTeam.first_baseman = myTeam.getPlayer(int(line[2]))
    myTeam.second_baseman = myTeam.getPlayer(int(line[3]))
    myTeam.third_baseman = myTeam.getPlayer(int(line[4]))
    myTeam.shortstop = myTeam.getPlayer(int(line[5]))
    myTeam.left_fielder = myTeam.getPlayer(int(line[6]))
    myTeam.center_fielder = myTeam.getPlayer(int(line[7]))
    myTeam.right_fielder = myTeam.getPlayer(int(line[8]))

    # The second to last line is the batting order
    file_reader.__next__()
    file_reader.__next__()
    line = file_reader.__next__()

    for stringy in line:
        if stringy != "":
            myTeam.batting_order.append(int(stringy))


    # Then the last line is the base coach assignments, by id
    file_reader.__next__()
    file_reader.__next__()
    line = file_reader.__next__()
    myTeam.first_base_coach = myTeam.getCoach(int(line[0]))
    myTeam.third_base_coach = myTeam.getCoach(int(line[1]))

    # Now close the file and return the team we've built!
    csvfile.close()
    return myTeam


# The function that'll do all the program work
def main():
    # First, read in the teams from the provided csv files
    print("Welcome to the baseball simulator! Reading team data...")
    home_team = readTeam(sys.argv[1])
    away_team = readTeam(sys.argv[2])
    start_string = "Successful! Welcome to today's matchup, between the " + home_team.city + " " + home_team.name + " and the " + away_team.city + " " + away_team.name + "!"
    print(start_string)
    print("It's looking to be an exciting matchup!")
    running = True

    # Setup the first at-bat
    player_at_bat = away_team.getPlayer(away_team.batting_order[away_at_bat])
    fielding_team = home_team
    team_at_bat = away_team


    # Begin our simulator loop
    while running:
        recognized = False
        print()
        print("> ", end="")
        input_string = input()
        print()

        # One if for each of the commands
        if input_string == "quit":
            recognized = 1
            print("Are you sure? There won't be a data export if you end the game early (y/n)")
            print("> ", end="")
            input_string = input()
            if input_string == "y":

                sys.exit()

        if input_string == "help":
            recognized = 1
            print("Here are a list of commands. See the local README.txt for further information.")
            print("quit") # Done
            print("help") # Done
            print("game_report") # Done
            print("positions") # Done
            print("stats <team> <player_jersey_number>") # Done
            print("substitute_player <position> <fresh_player_jersey_number> *") #done
            print("simulate_pitch") # Done
            print("simulate_at_bat") #To Do
            print("simulate_half_inning") # To Do
            print("simulate_inning") # To Do
            print("simulate_game") # To Do
            print()
            print("*For reference, the position names recognized by the simulator are 'catcher', 'pitcher', 'first_baseman', 'second_baseman', 'shortstop', 'third_baseman', 'right_fielder', 'center_fielder', 'left_fielder' (without the quotes).")


        if input_string == "game_report":
            recognized = 1
            print("This is a matchup between the " + home_team.city + " " + home_team.name + " and the " + away_team.city + " " + away_team.name + ".")
            print("The current score is " + home_team.name + ": " + str(home_score) + " and " + away_team.name + ": " + str(away_score) + ".")
            print("It is inning " + str(inning) + " and the " + team_at_bat + " team is at bat.")
            print("Number " + str(player_at_bat.jersey_number) + ", " + player_at_bat.name + " is at bat.")
            print("There are " + str(outs) + " outs, and the count is " + str(balls) + "-" + str(strikes) + ".")
            if player_on_first != 0: print("Number " + str(player_on_first.jersey_number) + ", " + player_on_first.name + " is on first.")
            if player_on_second != 0: print("Number " + str(player_on_second.jersey_number) + ", " + player_on_second.name + " is on first.")
            if player_on_third != 0: print("Number " + str(player_on_third.jersey_number) + ", " + player_on_third.name + " is on first.")

        if input_string.split()[0] == "stats":
            recognized = 1
            if len(input_string.split()) != 3:
                print("Error: not enough arguments specified")
                continue
            elif not input_string.split()[2].isdigit():
                print("Error: second argument must be an integer")
                continue

            which_team = 0
            if input_string.split()[1] == home_team.name: which_team = home_team
            elif input_string.split()[1] == away_team.name: which_team = away_team
            else:
                print("Sorry, you didn't specify a team. Your options are '" + home_team.name + "' or '" + away_team.name + "' (without the quotes).")
                continue

            # Get the player based on the entered number
            which_player = which_team.getPlayer(int(input_string.split()[2]))

            if which_player == 0: print("Sorry, I don't see that player on the " + which_team.name + ".")
            else:
                print("Name: " + which_player.name)
                print("Handedness: " + which_player.handedness)
                print("Jersey Number: " + str(which_player.jersey_number))
                print("Hit Strength: " + str(which_player.hit_str))
                print("Throw Strength: " + str(which_player.throw_str))
                print("Hit Consistency: " + str(which_player.hit_cons))
                print("Throw Consistency: " + str(which_player.throw_cons))
                print("Pitch Judgement: " + str(which_player.pitch_judgement))
                print("Speed: " + str(which_player.speed))
                print("Reaction: " + str(which_player.reaction))
                print("Confidence: " + str(which_player.confidence))
                print("Cool: " + str(which_player.cool))
                print("Risk Tolerance: " + str(which_player.risk_tolerance))
                print("Righty/Lefty Killer: " + str(which_player.rl_killer))

        if input_string == "positions":
            recognized = 1
            print("Pitcher: Number " + str(fielding_team.pitcher.jersey_number) + ", " + fielding_team.pitcher.name)
            print("Catcher: Number " + str(fielding_team.catcher.jersey_number) + ", " + fielding_team.catcher.name)
            print("First Base: Number " + str(fielding_team.first_baseman.jersey_number) + ", " + fielding_team.first_baseman.name)
            print("Second Base: Number " + str(fielding_team.second_baseman.jersey_number) + ", " + fielding_team.second_baseman.name)
            print("Third Base: Number " + str(fielding_team.third_baseman.jersey_number) + ", " + fielding_team.third_baseman.name)
            print("Shortstop: Number " + str(fielding_team.shortstop.jersey_number) + ", " + fielding_team.shortstop.name)
            print("Left Field: Number " + str(fielding_team.left_fielder.jersey_number) + ", " + fielding_team.left_fielder.name)
            print("Center Field: Number " + str(fielding_team.center_fielder.jersey_number) + ", " + fielding_team.center_fielder.name)
            print("Right Field: Number " + str(fielding_team.right_fielder.jersey_number) + ", " + fielding_team.right_fielder.name)

        if input_string.split()[0] == "substitute_player":
            recognized = 1
            fresh_player = fielding_team.getPlayer(int(input_string.split()[2]))
            position = input_string.split()[1]

            # Just catch a few error states (rather than crashing)
            if len(input_string.split()) != 3:
                print("Error: not enough arguments specified")
                continue
            elif not input_string.split()[2].isdigit():
                print("Error: second argument must be an integer")
                continue
            elif fresh_player == 0:
                print("Can't find that player, sorry!")
                continue

            if position == "catcher":
                fielding_team.catcher = fresh_player
            elif position == "pitcher":
                fielding_team.pitcher = fresh_player
            elif position == "first_baseman":
                fielding_team.first_baseman = fresh_player
            elif position == "second_baseman":
                fielding_team.second_baseman = fresh_player
            elif position == "shortstop":
                fielding_team.shortstop = fresh_player
            elif position == "third_baseman":
                fielding_team.third_baseman = fresh_player
            elif position == "right_fielder":
                fielding_team.right_fielder = fresh_player
            elif position == "center_fielder":
                fielding_team.center_fielder = fresh_player
            elif position == "left_fielder":
                fielding_team.left_fielder = fresh_player
            else:
                print("I don't recognize that position name, try the 'help' command for a list of positions.")
                continue

            print("Successful substitution!")

        if input_string == "simulate_pitch" or input_string == "sp":
            simulate_pitch()

        if not recognized:
            print("Sorry, I don't recognize that command. Type 'help' for a list of commands.")


# Simulates a pitch from first decision (whether runners steal) to the last (hitting the pitched ball)
def simulate_pitch():
    # Lots of importing to be done
    global home_score
    global away_score
    global home_at_bat
    global away_at_bat
    global inning
    global team_at_bat
    global fielding_team
    global outs
    global strikes
    global balls
    global home_team
    global away_team
    global player_at_bat
    global player_on_first
    global player_on_second
    global player_on_third

    # First see if base runners want to try to steal
    second_steal_sim()

    if outs == 3:
        end_half_inning()
        return

    first_steal_sim()

    if outs == 3:
        end_half_inning() # TODO this function
        return

    pitch_category = 0
    pitch_type = 0
    results = 0

    # Simulate the pitch choice
    if (balls == 0 or balls == 1 or balls == 2) and strikes == 0:
        results = low_stakes_pitch()
    elif (balls == 0 or balls == 1 or balls == 2) and strikes == 1:
        results = low_stakes_pitch()
    elif (balls == 0 or balls == 1 or balls == 2) and strikes == 2:
        results = probably_throw_ball()
    elif balls == 3 and (strikes == 0 or strikes == 1):
        results = probably_throw_strike()
    elif balls == 3 and strikes == 2:
        results = full_count_pitch()

    pitch_category = results[0]
    pitch_type = results[1]

    # Success is in a range from 0 to 50
    pitch_success = fielding_team.pitcher.throw_cons - random.randint(1, 20) + round(0.5 * fielding_team.pitcher.cool) + 20

    # Simulate actual pitch delivery
    pitch_category = simulate_delivery(pitch_category, pitch_success)

    # Decide whether to bunt
    am_i_bunting = decide_whether_to_bunt()

    if am_i_bunting:
        simulate_bunt()
        return

    # If batter didn't bunt, decide whether to swing
    am_i_swinging = decide_whether_to_swing()

    if am_i_swinging:
        simulate_swing()
        return

    # If batter didn't bunt or swing, figure out result
    simulate_no_swing()
    return


# Simulate whether the player on second wants to steal
def second_steal_sim():
    # Lots of importing to be done
    global home_score
    global away_score
    global home_at_bat
    global away_at_bat
    global inning
    global team_at_bat
    global fielding_team
    global outs
    global strikes
    global balls
    global home_team
    global away_team
    global player_at_bat
    global player_on_first
    global player_on_second
    global player_on_third

    # If there's nobody on second, that nobody can't steal
    if player_on_second == 0:
        return
    # If there's someone on third they won't try to steal
    if player_on_third == 0:
        return

    # If this number is above the third base coach's risk tolerance, then the decision is to steal
    steal_decision = round(30 + player_at_bat.speed - 0.5 * fielding_team.catcher.throw_str - fielding_team.catcher.throw_cons)
    if steal_deicision > team_at_bat.third_base_coach.risk_tolerance:
        steal_decision = 1
    else:
        steal_decision = 0

    # Now figure out if the pitcher is going to try to pick them off
    pickoff_decision = steal_decision * 5 + player_on_second.speed
    if pickoff_decision > fielding_team.pitcher.risk_tolerance:
        pickoff_decision = 1
    else:
        pickoff_decision = 0

    if steal_decision == 1 and pickoff_decision == 0:
        player_on_third = player_on_second
        player_on_second = 0
        print("Number " + str(player_on_third.jersey_number) + " has stolen 3rd!")
        return
    elif pickoff_decision == 0:
        return
    else:
        pickoff_result = steal_decision * 10 + fielding_team.pitcher.throw_cons - player_on_second.reaction + randint(10) + 21
        if pickoff_result < 11:
            player_on_third = player_on_second
            player_on_second = player_on_first
            player_on_first = 0
            print("The pitcher fumbled the ball and all runners advanced!")
            return
        elif pickoff_result < 41:
            player_on_third = player_on_second
            player_on_second = 0
            print("The runner on 2nd stole third!")
            return
        else:
            player_on_second = 0
            outs += 1
            print("The pitcher got the runner on 2nd out!")
            return

# Simulate whether the player on first wants to steal
def first_steal_sim():
    # Lots of importing to be done
    global home_score
    global away_score
    global home_at_bat
    global away_at_bat
    global inning
    global team_at_bat
    global fielding_team
    global outs
    global strikes
    global balls
    global home_team
    global away_team
    global player_at_bat
    global player_on_first
    global player_on_second
    global player_on_third

    # If there's nobody on first, that nobody can't steal
    if player_on_first == 0:
        return
    # If there's someone on second they won't try to steal
    if player_on_second == 0:
        return

    # Now figure out if the pitcher is going to try to pick them off
    pickoff_decision = steal_decision * 5 + player_on_first.speed
    if pickoff_decision > fielding_team.pitcher.risk_tolerance:
        pickoff_decision = 1
    else:
        pickoff_decision = 0

    if steal_decision == 1 and pickoff_decision == 0:
        player_on_second = player_on_first
        player_on_first = 0
        print("Number " + str(player_on_second.jersey_number) + " has stolen 2nd!")
        return
    elif pickoff_decision == 0:
        return
    else:
        pickoff_result = steal_decision * 10 + fielding_team.pitcher.throw_cons - player_on_first.reaction + randint(10) + 21
        if pickoff_result < 11:
            player_on_third = player_on_second
            player_on_second = player_on_first
            player_on_first = 0
            print("The pitcher fumbled the ball and all runners advanced!")
            return
        elif pickoff_result < 41:
            player_on_second = player_on_first
            player_on_first = 0
            print("The runner on 1st stole 2nd!")
            return
        else:
            player_on_second = 0
            outs += 1
            print("The pitcher got the runner on 1st out!")
            return

# At three outs, switch sides, update the inning, etc
def end_half_inning():
    # Lots of importing to be done
    global home_score
    global away_score
    global home_at_bat
    global away_at_bat
    global inning
    global team_at_bat
    global fielding_team
    global outs
    global strikes
    global balls
    global home_team
    global away_team
    global player_at_bat
    global player_on_first
    global player_on_second
    global player_on_third

    player_on_first = 0
    player_on_second = 0
    player_on_third = 0
    temp_team = team_at_bat
    team_at_bat = fielding_team
    fielding_team = temp_team
    if team_at_bat == away_team:
        inning += 1
        player_at_bat = away_at_bat
    else:
        player_at_bat = home_at_bat

    return

# Simulates the actual delivery of a pitch
def simulate_delivery(pitch_category, pitch_success):
    if pitch_category == "strike":
        if pitch_success < 6:
            pitch_category = "meatball"
        elif pitch_success < 21:
            pitch_category = "ball"
        else:
            pitch_category = "strike"
    elif pitch_category == "ball":
        if pitch_success < 6:
            pitch_category = "wild"
        elif pitch_success < 16:
            pitch_category = "strike"
        else:
            pitch_category = "ball"
    elif pitch_category == "garbage":
        if pitch_success < 11:
            pitch_category = "wild"
        else:
            pitch_category = "garbage"

    return pitch_category


# This is technically the beginning of the program
# If there aren't enough arguments, print an error and quit
if len(sys.argv) < 3:
    print("use: python DerekBaseballProgram.py <team_sheet1.csv> <team_sheet2.csv>")
    sys.exit()
else: # Play ball!
    main()
