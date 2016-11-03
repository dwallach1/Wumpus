import random, json, os

# We are assuming the following moves:

# Moves that change your orientation
# Up 
# Down
# Left
# Right

# A move that changes your position
# Step

# The move that allows you to exit the board
# Exit

# Other actions that change the world aside from your position
# PickUp
# Shoot

# The function update will return a vector of strings that represent:

# (smell, air, glitter, bump, scream, location, orientation, status, score)
# The possible values are:

# Smell - clean|nasty
# Air - calm|breeze
# Glitter - bare|glitter
# Bump - no_bump|bump
# Scream - quiet|scream
# Location - unique identifier for current square
# Orientation - the direction you are facing
# Status - living|dead|won
# Score - current score


# You get precept vectors by calling take_action with the name of your world and the
# move you want to take.

def take_action(world_token,move):

    world = get_world(world_token)
    location = world["location"]
    orientation = world["orientation"]
    points = world["points"]
    status = world["status"]
    arrows = world["arrows"]
    
    print "\n*********************************\n"
 
    if status == "dead":
        print "You are dead.  Start a new game"
        return
    elif move == "Exit":
        update = update_location(world, location, orientation)
        if world["location"] != "Cell 11":
            print "You need to get back to Cell 11 to exit"
        elif world["points"] == 0:
            print "You need to score some points in order to exit"
        else:
            update[7] = "won"
    elif move == "Toss":
        if world["rocks"] <= 0:
            print "You are out of rocks"
            return 
        else:   
            world["rocks"] = world["rocks"] - 1 
            print "Tossing a rock. You have " + str(world["rocks"]) + " left."
            store_world(world_token,world)
            cell_state = world[world[location][orientation]]
            if cell_state["Pit"] is True:
                return "Quiet"
            else:
                return "Clink"
    elif move == "Step":
        print "Taking a step"
        new_location = world[location][orientation]
        if new_location == "Void":
            print "You bumped your head on the edge of the world."
            update = update_location(world, location, orientation)
            update[3] = "bump"         
        else:
            print "Moving to " + str(new_location)
            update = update_location(world, new_location, orientation)
            world["location"] = new_location
    elif move in["Up","Down","Left","Right"]:
        print "Turing to face " + move
        update = update_location(world, location, move)
        world["orientation"] = move
    elif move == "PickUp":
        print "Trying to pick up gold"
        if got_gold(world, location):
            print "You've picked up some gold!"
            print "You get 1000 more points!"
            update = update_location(world, location, orientation)
            update[2] = "bare"
            world[location]["Gold"] = False
            world["points"] = world["points"]+1000
        else:
            print "There is no gold here!"
            update = update_location(world, location, orientation)
    elif move == "Shoot":
        print "Trying to shoot the Wumpus"
        if world["arrows"] <= 0:
           print "You are out of arrows"
        elif wumpus_in_sight(world,location, orientation):
            print "You killed the Wumpus!"
            print "You get 100 more points!"
            wumpus_location = where_is_the_Wumpus(world,location,orientation)
            world[wumpus_location]["Wumpus"] = False
            world["points"] = world["points"]+100
        else:
            print "You missed the Wumpus!"
        update = update_location(world, location, orientation)
        world["arrows"] = world["arrows"] - 1
    print "Perception = (" + ", ".join(update) + ")"
    world["status"] = update[7] 
    store_world(world_token,world)
    update[8] = world["points"]
    return update


# Update_location figures out the perceptual elements associated with a location by
# checking for gold, pits and the Wumpus

def update_location(world,location,orientation):
    location_info = world[location]
    baseline = ["clean","calm","bare","no_bump","quiet",location, orientation, "living", str(world["points"])]
    
    if got_gold(world, location):
        print "There is a lovely glitter in the room"
        baseline[2] = "glitter"    
          
    if got_breeze(world, location):
        print "There is a breeze running through this room"
        baseline[1] = "breeze"  
        
    if got_smell(world, location):
        print "There is a nasty smell in here"
        baseline[0] = "nasty"    
                 
    if location_info["Wumpus"] is True:
        print "You got killed by the Wumpus and it was shockingly painful"
        baseline[7] = "dead"
        
    elif location_info["Pit"] is True:
        print "You fell into a pit and died a slow and scary death"
        baseline[7] = "dead"

    return baseline

# Various tests to figure out precept list.  

# Is there gold in this cell?

def got_gold(world, location):
    return world[location]["Gold"]

# Do any of the adjacent cells have Pits in them?
    
def got_breeze(world,location):
    for x in world[location]["Next"]:
        if world[x]["Pit"]:
            return True
    return False


# Do any of the adjacent cells have the Wumpus?
    
def got_smell(world,location):
    for x in world[location]["Next"]:
        if world[x]["Wumpus"] is True:
            return True
    return False  
  
  
# Is there are Wumpus in the agent's line of sight?
    
def wumpus_in_sight(world, location, orientation):
    next_location = world[location][orientation]
    if world[location]["Wumpus"] is True:
        return True
    elif next_location == "Void":
        return False
    else:
        return wumpus_in_sight(world, next_location, orientation)


# Where is the Wumpus in the agent's line of sight?
    
def where_is_the_Wumpus(world, location, orientation):
    next_location = world[location][orientation]
    if world[location]["Wumpus"] is True:
        return location
    else:
        return where_is_the_Wumpus(world, next_location, orientation)
# look_ahead

def look_ahead(world_token):
    world = get_world(world_token)
    return world[world["location"]]["Next"]

# Build out the dictionary that makes up the simple world that we have been looking at
    
def build_world(gold, wumpus, pits):
    layout = {}
    height = 4
    width = 4
    for x in range(1,width+1):
        for y in range(1,height+1):
            new_cell = {}
            new_cell["Up"] = "Void"
            new_cell["Down"] = "Void"
            new_cell["Left"] = "Void"
            new_cell["Right"] = "Void"
            new_cell["Wumpus"] = False
            new_cell["Pit"] = False
            new_cell["Gold"] = False    
            new_cell["Next"] = []    
            if y < 4:
                new_cell["Up"] = "Cell " + str(x) + str(y+1)
                new_cell["Next"].append(new_cell["Up"])
            if y > 1:
                new_cell["Down"] = "Cell " + str(x) + str(y-1)
                new_cell["Next"].append(new_cell["Down"])
            if x < 4:
                new_cell["Right"] = "Cell " + str(x+1) + str(y)
                new_cell["Next"].append(new_cell["Right"])
            if x > 1:
                new_cell["Left"] = "Cell " + str(x-1) + str(y)
                new_cell["Next"].append(new_cell["Left"])
            layout["Cell "+str(x)+str(y)] = new_cell      
    layout[wumpus]["Wumpus"]=True  
    print "There is a Wumpus in cell " + wumpus + "."     
    layout[gold]["Gold"]=True 
    print "There is Gold in cell " + gold + "."  
    for cell in pits:
        layout[cell]["Pit"]=True 
        print "There is a Pit in cell " + cell + "."    
    print
    return layout 


# In order to have a persistant world, we are going to store and update it as the 
# game progresses.

# We first initialize the state of the world and return a random token to the user
# so that they can refer to the world that they are playing in

def intialize_world():
    world_name = "Wumpus" + str(random.randint(0,10000))
    print "\n*********************************\n"
    print "Initializing your new Wumpus world!"
    print "Your new world is called: "+ world_name
    if not os.path.exists("WumpusWorldDataFolder"):
        os.makedirs("WumpusWorldDataFolder")
    world=build_world("Cell 32", "Cell 13", ["Cell 31","Cell 33","Cell 44"])
    world["location"] = "Cell 11"
    world["orientation"] = "Right"
    world["status"] = "living"
    world["points"] = 0
    world["arrows"] = 1
    world["rocks"] = 5

    print "You are starting in Cell 11, looking to the Right."
    print "You are starting with 0 points, " + str(world["arrows"]) + " arrow(s)."
    print "You have " + str(world["rocks"]) + " rocks."
    print "You are alive."
    with open("WumpusWorldDataFolder/"+world_name+".json", 'w') as worldfile:
        json.dump(world, worldfile)
        worldfile.close()    
    return world_name

# In order to have a persistant world, we are going to store and update it as the 
# game progresses.

# We first initialize the state of the world and return a random token to the user
# so that they can refer to the world that they are playing in

def intialize_my_world(gold,wumpus,pits):
    world_name = "Wumpus" + str(random.randint(0,10000))
    print "\n*********************************\n"
    print "Initializing your own Wumpus world!"
    print "Your new world is called: "+ world_name
    if not os.path.exists("WumpusWorldDataFolder"):
        os.makedirs("WumpusWorldDataFolder")
    world=build_world(gold,wumpus,pits)
    world["location"] = "Cell 11"
    world["orientation"] = "Right"
    world["status"] = "living"
    world["points"] = 0
    world["arrows"] = 1
    world["rocks"] = 5

    print "You are starting in Cell 11, looking to the Right."
    print "You are starting with 0 points, " + str(world["arrows"]) + " arrow(s)."
    print "You have " + str(world["rocks"]) + " rocks."
    print "You are alive."
    with open("WumpusWorldDataFolder/"+world_name+".json", 'w') as worldfile:
        json.dump(world, worldfile)
        worldfile.close()    
    return world_name



# At the beginning of each turn, we load the last state of the world so we know 
# what precepts to return in response the actions.
        
def get_world(world_name):
    with open("WumpusWorldDataFolder/"+world_name+".json") as worldfile:    
        world = json.load(worldfile)
        worldfile.close()
    return world


# As things change in response to actions, we update and store the world in response to 
# actions that have been taken

def store_world(world_name,world):
    with open("WumpusWorldDataFolder/"+world_name+".json", 'w') as worldfile:
        json.dump(world, worldfile)
        worldfile.close()
