from time import sleep

# Lists of good and bad verbs
goodVerbs = ['eat', 'walk', 'sing', 'swim', 'sew', 'draw', 'climb', 'swim', 'talk', 'party', 'cook', 'drink', 'train']
badVerbs = ['complain', 'run', 'fight', 'work', 'box', 'steal', 'jump', 'cry', 'study', 'punch', 'slap']


# Function to call each bot function at a time
def callBots(name, suggestVerb):
    sleep(2)
    if name == 'toyota':
        return toyota(suggestVerb)
    elif name == 'honda':
        return honda(suggestVerb)
    elif name == 'suzuki':
        return suzuki(suggestVerb)
    elif name == 'matsuda':
        return matsuda(suggestVerb)
    else:
        return "ERROR: Something wrong happened in callBots."


# Function to return Toyota's response
def toyota(suggestVerb):
    response = "Toyota: I don't care."  # Default response

    if suggestVerb in goodVerbs:
        response = f"Toyota: I think {suggestVerb}ing sounds great, let's do it!"
    elif suggestVerb in badVerbs:
        response = f"Toyota: Hmmmm I'm not in the mood to {suggestVerb} right now, maybe another time."

    return response + '}'  # Add the character '}' for marking the end of the message


# Function to return Honda's response
def honda(suggestVerb):
    response = "Honda: I'm not sure."

    if suggestVerb in goodVerbs:
        response = f"Honda: Why not? I've been waiting for this moment to {suggestVerb}!"
    elif suggestVerb in badVerbs:
        response = f"Honda: I don't particularly like {suggestVerb}ing."

    return response + '}'


# Function to return Suzuki's response
def suzuki(suggestVerb):
    response = "Suzuki: Doesn't look like anything to me."

    if suggestVerb in goodVerbs:
        response = f"Suzuki: There's always time for some {suggestVerb}ing!"
    elif suggestVerb in badVerbs:
        response = f"Suzuki: No I don't want to {suggestVerb} now honestly, I'm too tired."

    return response + '}'


# Function to return Matsuda's response
def matsuda(suggestVerb):
    response = "Matsuda: I cannot fathom what you are on about."

    if suggestVerb in goodVerbs:
        response = f"Matsuda: I have no interest in {suggestVerb}ing whatsoever."
    elif suggestVerb in badVerbs:
        response = f"Matsuda: Splendid! We’ll have a jolly good time {suggestVerb}ing!"

    return response + '}'
