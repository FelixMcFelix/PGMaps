import random

def dungeon_root():
    return ["obstacle", "treasure"]

dungeon = dungeon_root()
branches = []

def generate_obstacle():
    return random.choice([
        ["key", "obstacle", "lock", "obstacle"],
        ["monster", "obstacle"],
        ["room"],
        ["branch", "lock"],
    ])

# TODO: probably limit the depth of these (or not, for arbitrary complexity)
def generate_branch():
    return random.choice([
        #cycle
        ["root", "obstacle", "key", "obstacle", "root"],
        #branch
        ["root", "obstacle", "key"],
    ])

def recurse_dungeon(dungeon):
    while "obstacle" in dungeon:
        dungeon = process_dungeon(dungeon)

    return dungeon

def fill_branches(dungeon, branches=[], depth=0):
    for i, node in enumerate(dungeon):
        if node != "branch":
            continue
        elif depth > 2:
            # hard fix
            dungeon[i] = "key"
            continue

        num = len(branches)
        dungeon[i] = "branch-{}".format(num)

        new_branch = recurse_dungeon(generate_branch())
        branches.append([]) # placeholder for injection

        (inner_dungeon, branches) = fill_branches(new_branch, branches, depth=depth+1)
        branches[num] = inner_dungeon

    return (dungeon, branches)

def process_dungeon(dungeon):
    new_dungeon = []
    for i, node in enumerate(dungeon):
        if node == "obstacle":
            generated_obstacle = generate_obstacle()
            for element in generated_obstacle:
                new_dungeon += [element]
        else:
            new_dungeon += [dungeon[i]]
    return new_dungeon

dungeon = recurse_dungeon(dungeon)
(dungeon, branches) = fill_branches(dungeon)

print "--------"
print "Dungeon:"
print dungeon
print "--------"

if len(branches):
    print "--------"
    print "Branches:"
    for i, branch in enumerate(branches):
        print "{}:".format(i), branch
    print "--------"

#for i in range(1000):
#    results[random.randint(1,5)-1] += 1

#print results
