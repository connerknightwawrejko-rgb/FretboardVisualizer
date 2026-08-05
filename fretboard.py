import pygame

pygame.init()

#Just initializing all of the constants

AWIDTH, WIDTH, AHEIGHT, HEIGHT = 1240, 1200, 610, 300
screen = pygame.display.set_mode((AWIDTH, AHEIGHT))
RED = (255,0,0)
GREEN = (0,255,0)
DARK_GREEN = (0,150,0)
GREY = (100,100,100)
BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.display.set_caption("Fretboard Visualizer")
FONT = pygame.font.SysFont('Segoe UI Symbol', 15)
CLOCK = pygame.time.Clock()

#Just here for easy visualization of the chord functions between modes
#This especially helps because I have yet to move from purely sharps/# to including flats/b as well
CHORD_FUNCTIONS = {
    1: 'I – ii – iii – IV – V – vi – vii°',
    2: 'i – ii – III – IV – v – vi° – VII',
    3: 'i – II – III – iv – v° – VI – vii',
    4: 'I – II – iii – iv° – V – vi – vii',
    5: 'I – ii – iii° – IV – v – vi – VII',
    6: 'i – ii° – III – iv – v – VI – VII',
    7: 'i° – II – iii – iv – V – VI – vii'
}

#Just every note in the chromatic scale. Standard 12 tet stuff.
NOTES = {
    'c': 0,
    'c#': 1,
    'd': 2,
    'd#': 3,
    'e': 4,
    'f': 5,
    'f#': 6,
    'g': 7,
    'g#': 8,
    'a': 9,
    'a#': 10,
    'b': 11,
}

#This is just backwards notes. I'm honestly not very good at naming variables
SETON = {v: k for k, v in NOTES.items()}

MODES = ['Ionian','Dorian','Phrygian','Lydian','Mixolydian','Aeolian','Locrian']

#This is just for indexing in the TUNINGS dictionary
instruments = ['Guitar','Bass Guitar','Ukulele','Mandolin']

instrument_index = 0
TUNINGS = {'Guitar': ['e','a','d','g','b','e'],
          'Bass Guitar': ['a','d','g','b'],
          'Ukulele': ['g','c','e','a'],
          'Mandolin': ['g','d','a','e']
}

#Just a bunch of variables that help to handle the math and modular stuff
tuning = TUNINGS[instruments[instrument_index]][:]

#searching is used to pick out the notes from the scale 
#switch is to handle the math for switching between the modes and stay on the same note
searching = [0,2,4,5,7,9,11]
switch = [2,2,1,2,2,2,1]
pos = 0
mode = 0
button = 0
string = 0
fretboard_len = 12
chord_show = [None]*len(tuning)

def scale(position,mode):
    #This handles all of the math for mapping out the notes and where they go on the fretboard
    notess = []
    searching = [0,2,4,5,7,9,11]
    fretboard = [[None for _ in range(fretboard_len)] for _ in range(len(tuning))]
    for i, x in enumerate(searching):
        searching[i] = (x+position) % 12
        notess.append(SETON[(x+position) % 12].upper())
    for i, x in enumerate(tuning):
        for z in range(fretboard_len):
            a = True if NOTES[x] in searching else False
            b = True if NOTES[x] == searching[mode] else False
            fretboard[i][z] = (x, a, b)
            x = SETON[(NOTES[x] + 1) % 12]

    return notess, fretboard

def visuals(fretboard,notess):
    #This handles the actual visuals for the UI and distinguishing the root notes, notes in the scale, and notes not in the scale
    frets = []
    for i, x in enumerate(fretboard):
        for y, z in enumerate(x):
            note, key, root = z
            selected = False
            if chord_show[i] == y:
                selected = True
            if key and root:
                frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), RED, note, selected))
            elif key and not root:
                frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), GREY, note, selected))
            else:
                frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), WHITE, note, selected))
    for i in range(mode):
        notess.append(notess.pop(0))

    return frets

#This looks like quite a lot but its really just a big block of if/elif/else statements to handle specific theory rules
#The rest is honestly pretty self explanatory.
def chord_id(notes):
    actual_notes = []
    if any(x != None for x in notes):
        for i, x in enumerate(notes):
            if x != None:
                y = (NOTES[tuning[i]] + x) % 12
                if y not in actual_notes:
                    actual_notes.append(y)

    finished_chords = []

    for i in range(len(actual_notes)):

        listem = actual_notes[:]
        a_list = []

        for x in range(i):
            listem.append(listem.pop(0))

        for note in listem:
            a_list.append((note - listem[0]) % 12)

        name = ""

        has_maj3 = 4 in a_list
        has_min3 = 3 in a_list
        has_maj7 = 11 in a_list
        has_min7 = 10 in a_list
        has_5 = 7 in a_list
        has_b5 = 6 in a_list
        has_s5 = 8 in a_list
    
        if has_min3 and has_b5 and not has_maj7 and not has_min7:
            name = "dim"
        elif has_maj3 and has_s5 and not has_maj7 and not has_min7:
            name = "aug"
        elif has_min3 and has_maj7:
                name = "m(maj7)"
        elif has_min3 and has_min7:
            name = "m7"
        elif has_maj3 and has_min7:
            name = "7"
        elif has_maj3 and has_maj7:
            name = "maj7"
        elif has_maj3:
                name = ""
        elif has_min3:
            name = "m"
        elif 5 in a_list and not has_maj3 and not has_min3 and has_min7:
            name = "7sus4"
        elif 5 in a_list and not has_maj3 and not has_min3:
            name = "sus4"
        elif 2 in a_list and not has_maj3 and not has_min3:
            name = "sus2"
        else:
            name = "(no 3rd)"

        if has_b5 and not has_5 and "dim" not in name:
            name += "(b5)"
            has_5 = True
        if has_s5 and not has_5 and "aug" not in name:
            name += "(#5)"

        extensions = []
        if 10 in a_list and 11 in a_list:
            extensions.append("addmaj7")
        if 1 in a_list:
            extensions.append("addb9")
        if 2 in a_list and ("7" in name or "9" not in name):
            extensions.append("add9")
        if 3 in a_list and has_maj3:
            extensions.append("add#9")
        if 5 in a_list and "sus4" not in name:
            extensions.append("add11")
        if 6 in a_list and has_5 and '(b5)' not in name:
            extensions.append("add#11")
        if 8 in a_list and has_5:
            extensions.append("addb13")
        if 9 in a_list and not 'dim' in name:
            extensions.append("add13")
        elif 9 in a_list and 'dim' in name:
                name += '7'
        
        if extensions:
            name += "(" + ",".join(extensions) + ")"

        if not name:
            name = 'maj'

        finished_chords.append(SETON[listem[0]].upper() + name)

    returning = ', '.join(finished_chords)
    if returning:
        returning = returning if len(actual_notes) >= 3 else returning + ' #Caution: Chord names may be innacurate with less than 3 different notes selected.'

    return returning
    

#Just initializes everything
notess, fretboard = scale(pos,mode)
frets = visuals(fretboard, notess)

#running loop
running = True
while running:
    screen.fill(WHITE)

    #Draws the frets
    for i in frets:
        a, b, c, d = i
        pygame.draw.rect(screen, b, a)
        pygame.draw.rect(screen, BLACK, a, width=2)
        if d:
            rad = min(a.width, a.height) // 3
            pygame.draw.circle(screen, GREEN, a.center, rad)
            pygame.draw.circle(screen, DARK_GREEN, a.center, rad, width=3)
        fret_note = FONT.render(c.upper(), True, BLACK)
        note_fret = fret_note.get_rect(center=a.center)
        screen.blit(fret_note, note_fret)

    #Draws the notes to go with the frets
    for x, i in enumerate(tuning):
        if button == 1 and string == x:
            string_text = FONT.render(i.upper(), True, (255, 0, 0))
        else:
            string_text = FONT.render(i.upper(), True, (0, 0, 0))

        screen.blit(string_text, (1215, HEIGHT//(len(tuning))*((len(tuning)-1)-x)+20))

    for i in range(fretboard_len):
        tehed = 5 if i < 10 else 7
        x = 1200//(fretboard_len*2)-tehed
        xx = 1200//fretboard_len*i
        fret_num = FONT.render(str(i), True, (0, 0, 0))
        screen.blit(fret_num, (x+xx, 310))

    #Draws all of the text for the instructions and other visuals

    color = GREEN if button == 0 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 340))

    color = GREEN if button == 1 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 370))

    color = GREEN if button == 2 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 400))

    color = GREEN if button == 3 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 430))

    abseref = ', '.join(notess)
    scale_text = FONT.render(f'{SETON[(searching[mode] + pos) % 12].upper()} {MODES[mode]} | {abseref} ', True, (0, 0, 0))
    screen.blit(scale_text, (30, 340))

    tuning_text = FONT.render(f'Tuning: {"".join(tuning).upper()}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 370))

    tuning_text = FONT.render(f'Instrument: {instruments[instrument_index]}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 400))

    tuning_text = FONT.render(f'Fret amound: {fretboard_len}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 430))

    instructions = FONT.render('[LEFT/RIGHT] to change root note | [UP/DOWN] to change mode', True, (100, 100, 100))
    screen.blit(instructions, (320, 340))

    instructions = FONT.render('[LEFT/RIGHT] to tune the string | [UP/DOWN] to change string', True, (100, 100, 100))
    screen.blit(instructions, (320, 370))

    instructions = FONT.render('[LEFT/RIGHT] to change the instrument', True, (100, 100, 100))
    screen.blit(instructions, (320, 400))

    instructions = FONT.render('[LEFT/RIGHT] to change the amount of frets shown (This includes the 0th fret)', True, (100, 100, 100))
    screen.blit(instructions, (320, 430))

    instructions = FONT.render('Additional Info:', True, (0, 0, 0))
    screen.blit(instructions, (10, 460))

    instructions = FONT.render('press [1] and [2] to switch between changing the tuning, changing the scale, and etc | [3] to reset to standards, and [4] to clear all selected frets', True, (100, 100, 100))
    screen.blit(instructions, (10, 490))

    instructions = FONT.render('Click on the frets to select notes for chord identification', True, (100, 100, 100))
    screen.blit(instructions, (10, 520))

    chord = chord_id(chord_show)
    chord = "Awaiting input..." if not chord else chord
    
    instructions = FONT.render(f'Potential Chord Names: {chord}', True, (0, 0, 0))
    screen.blit(instructions, (10, 550))

    instructions = FONT.render(f'Chord Functions: {CHORD_FUNCTIONS[mode+1]}', True, (0, 0, 0))
    screen.blit(instructions, (10, 580))

    #Button inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #This block is for [1] and [2] going forward and backward on the options and [3] to reset everything back to standard tuning on the instrument
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                button = (button - 1) % 4
            if event.key == pygame.K_2:
                button = (button + 1) % 4
            if event.key == pygame.K_3:
                tuning = TUNINGS[instruments[instrument_index]][:]
                searching = [0,2,4,5,7,9,11]
                pos = 0
                mode = 0
                string = 0
                fretboard_len = 12
                notess, fretboard = scale(pos,mode)
                frets = visuals(fretboard, notess)
            if event.key == pygame.K_4:
                chord_show = [None]*len(tuning)
                notess, fretboard = scale(pos,mode)
                frets = visuals(fretboard, notess)

            #This block handles changing scales
            if button == 0:
                if event.key == pygame.K_RIGHT:
                    pos = (pos + 1) % 12
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_LEFT:
                    pos = (pos - 1) % 12
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_UP:
                    pos = (pos - switch[mode]) % 12
                    mode = (mode + 1) % 7
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_DOWN:
                    mode = (mode - 1) % 7
                    pos = (pos + switch[mode]) % 12
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
            
            #This block handles chaning the tunings
            elif button == 1:
                if event.key == pygame.K_RIGHT:
                    tuning[string] = SETON[(NOTES[tuning[string]] + 1) % 12]
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_LEFT:
                    tuning[string] = SETON[(NOTES[tuning[string]] - 1) % 12]
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_UP:
                    string = (string + 1) % (len(tuning))
                elif event.key == pygame.K_DOWN:
                    string = (string - 1) % (len(tuning))
                    
            #This block handles changing the instrument
            elif button == 2:
                if event.key == pygame.K_RIGHT:
                    instrument_index = (instrument_index + 1) % len(instruments)
                    tuning = TUNINGS[instruments[instrument_index]][:]
                    chord_show = [None]*len(tuning)
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_LEFT:
                    instrument_index = (instrument_index - 1) % len(instruments)
                    tuning = TUNINGS[instruments[instrument_index]][:]
                    chord_show = [None]*len(tuning)
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                    
            #This block handles changing the amound of frets shown
            elif button == 3:
                if event.key == pygame.K_RIGHT:
                    fretboard_len += 1
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_LEFT:
                    chord_show_max = max(x for x in chord_show if x is not None)
                    if fretboard_len - 1 > chord_show_max:
                        fretboard_len -= 1
                        notess, fretboard = scale(pos,mode)
                        frets = visuals(fretboard, notess)

        #This handles all of the pressing the frets stuff
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x < WIDTH and y < HEIGHT:
                string = y//(HEIGHT//len(tuning))
                fret = x//(WIDTH//fretboard_len)
                string_actual = []
                for i in range(len(tuning)):
                    string_actual.append(len(tuning)-i-1)
                string = string_actual[string]
                if chord_show[string] == fret:
                    chord_show[string] = None
                else:
                    chord_show[string] = fret
                
                notess, fretboard = scale(pos,mode)
                frets = visuals(fretboard, notess)
                
                      
    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()