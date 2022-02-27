#Gamify - Aidan Liu & Jake Bastin

def initialize():
    '''Initialize the global variables needed for the simulation and set
    variables to their initial values/states.'''

    global cur_hedons
    global cur_health

    global cur_time
    global last_activity
    global last_activity_duration

    global last_finished
    global bored_with_stars

    global cur_star
    global cur_star_activity

    global tiredness

    global counter_running

    global counter_resting

    global oldest_star
    global older_star
    global new_star

    counter_resting = 0

    oldest_star = -1
    older_star = -1
    new_star = 0

    cur_hedons = 0
    cur_health = 0

    cur_star = None
    cur_star_activity = None

    bored_with_stars = False

    last_activity = None
    last_activity_duration = 0

    tiredness = False

    counter_running = 0

    cur_time = 0


def get_cur_hedons():
    '''Return the current value of hedons.'''
    return cur_hedons

def get_cur_health():
    '''Return the current value of health. '''
    return cur_health

def star_interest():
    '''Evaluate the frequency of stars offered within a set time and if the user
     is bored with stars.'''
    global oldest_star
    global older_star
    global new_star
    global cur_time
    global bored_with_stars

    if bored_with_stars == True:
        return

    new_star = cur_time

    if new_star - oldest_star < 120 and oldest_star != -1:
        bored_with_stars = True
        return

    oldest_star = older_star
    older_star = new_star

def offer_star(activity):
    '''Offer stars for activity (parameter).'''
    global cur_star
    global cur_star_activity
    global counter_star

    star_interest()

    if activity == "running":
        cur_star = True
        cur_star_activity = "running"
    elif activity == "textbooks":
        cur_star = True
        cur_star_activity = "textbooks"
    else:
        return

def star_can_be_taken(activity):
    '''Return true iff a star can be used to obtain more hedons for activity
    (parameter). '''
    if cur_star_activity == activity and bored_with_stars == False:
        return True
    else:
        return False

def perform_running(duration):
    '''Perform the activity (running) for a set time defined by the duration
    parameter.'''
    global cur_time
    global cur_hedons
    global cur_health
    global counter_running
    global last_activity
    global last_activity_duration
    global cur_star
    global cur_star_activity
    global tiredness
    global counter_resting

    '''Health Points for Running'''

    if last_activity != "running":
        counter_running = 0
    if duration + counter_running > 180:
        if counter_running > 180:
            cur_health += 1 * duration
        else:
            cur_health += 3 * (180 - counter_running)
            cur_health += duration + counter_running - 180
    elif duration + counter_running <= 180:
        cur_health += 3 * duration

    counter_running += duration

    '''Hedons for Running'''

    if tiredness == False:
        if cur_star_activity == "running" and bored_with_stars == False:
            if duration > 10:
                cur_hedons += 5 * 10 - 2 * (duration - 10)
            elif duration <= 10:
                cur_hedons += 5 * duration
        elif cur_star_activity == "running" and bored_with_stars == True:
            if duration > 10:
                cur_hedons += 2 * 10 - 2 * (duration - 10)
            elif duration <= 10:
                cur_hedons += 2 * duration
        else:
            if duration > 10:
                cur_hedons += 2 * 10 - 2 * (duration - 10)
            elif duration <= 10:
                cur_hedons += 2 * duration

    elif tiredness == True:
        if cur_star_activity == "running" and bored_with_stars == False:
            if duration > 10:
                cur_hedons += 1 * 10 - 2 * (duration - 10)
            elif duration <= 10:
                cur_hedons += 1 * duration
        elif cur_star_activity == "running" and bored_with_stars == True:
            cur_hedons += -2 * duration
        else:
            cur_hedons += -2 * duration

    tiredness = True
    counter_resting = 0

def perform_textbooks(duration):
    '''Perform the activity (textbooks) for a set time defined by the duration
    parameter.'''
    global cur_time
    global cur_hedons
    global cur_health
    global last_activity
    global last_activity_duration
    global cur_star
    global cur_star_activity
    global tiredness
    global counter_resting

    '''Health Points for Textbooks'''

    cur_health += 2 * duration

    '''Hedons for Textbooks'''

    if tiredness == False:
        if cur_star_activity == "textbooks" and bored_with_stars == False:
            if duration > 20:
                cur_hedons += 4 * 10 + 1 * 10 - 1 * (duration - 20)
            elif duration > 10 and duration <= 20:
                cur_hedons += 4 * 10 + 1 * (duration - 10)
            elif duration <= 10:
                cur_hedons += 4 * duration
        elif cur_star_activity == "textbooks" and bored_with_stars == True:
            if duration > 20:
                cur_hedons += 1 * 20 - 1 * (duration - 20)
            elif duration <= 20:
                cur_hedons += 1 * duration
        else:
            if duration > 20:
                cur_hedons += 1 * 20 - 1 * (duration - 20)
            elif duration <= 20:
                cur_hedons += 1 * duration

    elif tiredness == True:
        if cur_star_activity == "textbooks" and bored_with_stars == False:
            if duration > 10:
                cur_hedons += 1 * 10 - 2 * (duration - 10)
            elif duration <= 10:
                cur_hedons += 1 * duration
        elif cur_star_activity == "textbooks" and bored_with_stars == True:
            cur_hedons += -2 * duration
        else:
            cur_hedons += -2 * duration

    tiredness = True
    counter_resting = 0

def perform_resting(duration):
    '''Perform the activity (resting) for a set time defined by the duration
    parameter.'''
    global counter_resting
    global tiredness

    counter_resting += duration

    if counter_resting >= 120 or last_activity == None:
        tiredness = False

def perform_activity(activity, duration):a
    '''Perform the activity for a specified duration of time passed through the
    activity and duration parameters.'''
    global cur_hedons
    global cur_health
    global last_activity
    global last_activity_duration
    global cur_star
    global cur_star_activity
    global cur_time

    if activity == "running":
        perform_running(duration)
    elif activity == "textbooks":
        perform_textbooks(duration)
    elif activity == "resting":
        perform_resting(duration)

    last_activity = activity
    last_activity_duration = duration
    cur_time += duration
    cur_star = None
    cur_star_activity = None

def most_fun_activity_minute():
    '''Return the activity that gives the most hedons for the next minute. '''
    if tiredness == False:
        if cur_star_activity == "running" and bored_with_stars == False:
            return "running"
        elif cur_star_activity == "running" and bored_with_stars == True:
            return "running"
        elif cur_star_activity == "textbooks" and bored_with_stars == False:
            return "textbooks"
        elif cur_star_activity == "textbooks" and bored_with_stars == True:
            return "running"
        else:
            return "running"

    elif tiredness == True:
        if cur_star_activity == "running" and bored_with_stars == False:
            return "running"
        elif cur_star_activity == "running" and bored_with_stars == True:
            return "resting"
        elif cur_star_activity == "textbooks" and bored_with_stars == False:
            return "textbooks"
        elif cur_star_activity == "textbooks" and bored_with_stars == True:
            return "resting"
        else:
            return "resting"
