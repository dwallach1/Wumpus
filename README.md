# Wumpus

Agent.py uses the game defined in updatewumpusNowWithRocks.py to develop a knowledge base and every move the bot makes it updates that knowledge base. It does this by using an inference engine to use past and current knoweldge to define safe moves. 

Rules for Wumpus are that if you walk into a pit or into the wumpus you die. In every adjacent cell to the wumpus, you will be notified of a smell. For the adjacent cells to the pits, you will feel a breeze. You have 1 arrow that can be used to kill the wumpus and 5 rocks that can be used to tell if there is a pit in the cell you throw it into. Every move returns a set of perceptions detailing what your player senses from that move. 

The goal is to get the treasure (denoted by a perception of glitter) and kill the wumpus and then return to the starting cell. Once there, you are supposed to call exit and the game will have been won. 

This game uses knoweldge representation, reasoning and logic. It expresses knowledge in a copmuter tracebale format so that the player (the agent) can move around the map and complete its mission without dying. 
