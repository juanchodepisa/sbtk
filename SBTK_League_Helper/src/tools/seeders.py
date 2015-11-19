from random import shuffle, sample

###########################
# ZIG-ZAG 
# SEEDERS
###########################

# Fair at the top
def snake_generator(players, groups):
    step = 1
    limits = {-1: 0 , 1: groups-1}
    n = 0
    while players > 0:
        players -= 1
        yield n
        if n == limits[step]:
            step *= -1
        else:
            n += step

# Fair at the bottom
def snake_inverted_generator(players, groups):
    step = 1
    limits = {-1: players % groups, 1: (players-1)%groups}
    n = 0
    while players > 0:
        players -= 1
        yield n
        if n == limits[step]:
            step *= -1
        else:
            n = (n + step) % groups

# Fair at the top and at the bottom
# Small disbalance in the middle (at the row where the jump occurs)
def snake_normalized_generator(players, groups, jump = 1):
    step = 1
    limits = {-1: 0 , 1: groups-1}
    n = 0
    
    phase1 = max(0, (players//groups - jump) * groups)
    
    while players > phase1:
        players -= 1
        yield n
        if n == limits[step]:
            step *= -1
        else:
            n += step
    
    # The jump:
    if players > 0:
        limits = {-step: n, step: (n-step)%groups}
    
    while players > 0:
        players -= 1
        yield n
        if n == limits[step]:
            step *= -1
        else:
            n = (n + step) % groups
 

##########################
# SLIDE
# SEEDER
##########################

# Equally fair at the top and at the bottom
# Gives the most predictable matches possible
# Emphasizes similar differences instead of better chances for the stronger players

def slide_generator(players, groups):
    for i in range(players):
        yield i%groups

#########################
# RANDOM
# SEEDER
#########################

def random_generator(players, groups)