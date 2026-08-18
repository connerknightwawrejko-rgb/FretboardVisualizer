import pygame

pygame.init()

#Just initializing all of the constants

AWIDTH, WIDTH, AHEIGHT, HEIGHT = 1240, 1200, 670, 300
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

CID_TOG_DICT = {
    0: 'Chord ID',
    1: 'Note Highlighter',
}

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
cid_toggle = 0
fretboard_len = 12
chord_show = [None]*len(tuning)
highlighted_notes = []
evil_highlight = []

#just because i dont want to have to keep refixing all of the placements for the instructions
ainfo = 490

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
            if cid_toggle == 0:
                if chord_show[i] == y:
                    selected = True
                if key and root:
                    frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), RED, note, selected))
                elif key and not root:
                    frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), GREY, note, selected))
                else:
                    frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), WHITE, note, selected))
            if cid_toggle == 1:
                if NOTES[note] in highlighted_notes:
                    if key and root:
                        frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), RED, note, selected))
                    elif key and not root:
                        frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), GREY, note, selected))
                    else:
                        frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), (200,200,200), note, selected))
                else:
                    frets.append((pygame.Rect(WIDTH//fretboard_len*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//fretboard_len,HEIGHT//(len(tuning))), (230,230,255), note, selected))

    for i in range(mode):
        notess.append(notess.pop(0))

    return frets

#This looks like quite a lot but its really just a big block of if/elif/else statements to handle specific theory rules
#The rest is honestly pretty self explanatory.
def chord_id(notes):

    actual_notes = notes
    

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
        if 2 in a_list and 'sus2' not in name:
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

def negative_harmony(position, highlights):

    searching = [0,2,4,5,7,9,11]
    for i, x in enumerate(searching):
        searching[i] = (x+position) % 12

    tunering = [SETON[searching[0]]]
    notesy = []
    evil_notes = []
    actual_evil_notes = []

    dict_harmony = {
        1: 2,
        12: 3,
        11: 4,
        10: 5,
        9: 6,
        8: 7
    }

    ynomrah_tcid = {v: k for k, v in dict_harmony.items()}

    thingers = 'c g d a e b f# c# g# d# a# f'.split(' ')
    go = True
    while go:
        if thingers[0] != tunering[0]:
            thingers.append(thingers.pop(0))
        else:
            go = False

    for i in highlights:
        x = thingers.index(SETON[i])+1
        try:
            evil_notes.append(dict_harmony[x])
        except:
            evil_notes.append(ynomrah_tcid[x])


    for i in evil_notes:
        actual_evil_notes.append(NOTES[thingers[i-1]])

    for i in actual_evil_notes:
        notesy.append(SETON[i])

    return actual_evil_notes, ' '.join(notesy)

#Just initializes everything
notess, fretboard = scale(pos,mode)
frets = visuals(fretboard, notess)

#running loop
running = True
while running:

    evil_highlight = []
    if cid_toggle == 0:
        if any(x != None for x in chord_show):
            for i, x in enumerate(chord_show):
                if x != None:
                    y = (NOTES[tuning[i]] + x) % 12
                    if y not in evil_highlight:
                        evil_highlight.append(y)

    elif cid_toggle == 1:
        evil_highlight = highlighted_notes[:]

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

    color = GREEN if button == 4 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 460))

    abseref = ', '.join(notess)
    scale_text = FONT.render(f'{SETON[(searching[mode] + pos) % 12].upper()} {MODES[mode]} | {abseref} ', True, (0, 0, 0))
    screen.blit(scale_text, (30, 340))

    tuning_text = FONT.render(f'Tuning: {"".join(tuning).upper()}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 370))

    tuning_text = FONT.render(f'Instrument: {instruments[instrument_index]}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 400))

    tuning_text = FONT.render(f'Fret Amount: {fretboard_len}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 430))

    tuning_text = FONT.render(f'Mode: {CID_TOG_DICT[cid_toggle]}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 460))

    instructions = FONT.render('[LEFT/RIGHT] to change root note | [UP/DOWN] to change mode', True, (100, 100, 100))
    screen.blit(instructions, (320, 340))

    instructions = FONT.render('[LEFT/RIGHT] to tune the string | [UP/DOWN] to change string', True, (100, 100, 100))
    screen.blit(instructions, (320, 370))

    instructions = FONT.render('[LEFT/RIGHT] to change the instrument', True, (100, 100, 100))
    screen.blit(instructions, (320, 400))

    instructions = FONT.render('[LEFT/RIGHT] to change the amount of frets shown (This includes the 0th fret)', True, (100, 100, 100))
    screen.blit(instructions, (320, 430))

    instructions = FONT.render('Additional Info:', True, (0, 0, 0))
    screen.blit(instructions, (10, ainfo))

    instructions = FONT.render('press [1] and [2] to switch between changing the tuning, changing the scale, and etc | [3] to reset to standards, and [4] to clear all selected frets', True, (100, 100, 100))
    screen.blit(instructions, (10, ainfo+30))

    instructions = FONT.render('Click on the frets to select notes for chord identification/highlighting depending on mode', True, (100, 100, 100))
    screen.blit(instructions, (10, ainfo+60))

    if cid_toggle == 0:

        a_chord_show = []
        if any(x != None for x in chord_show):
            for i, x in enumerate(chord_show):
                if x != None:
                    y = (NOTES[tuning[i]] + x) % 12
                    if y not in a_chord_show:
                        a_chord_show.append(y)

        chord = chord_id(a_chord_show)
        chord = "Awaiting input..." if not chord else chord
        
        instructions = FONT.render(f'Potential Chord Names: {chord}', True, (0, 0, 0))
        screen.blit(instructions, (10, ainfo+90))

    evil, also_evil = negative_harmony(pos, evil_highlight)
        
    evil_chord = chord_id(evil)
    evil_chord = "Awaiting input..." if not evil_chord else evil_chord
        
    instructions = FONT.render(f'Negetive Harmony: {evil_chord}, ({also_evil})', True, (0, 0, 0))
    screen.blit(instructions, (10, ainfo+150))

    if cid_toggle == 1:
        notes_selected = []
        highlighted_notes.sort()
        for i in highlighted_notes:
            notes_selected.append(SETON[i].upper())
        notes_selected = ', '.join(notes_selected)

        notes_selected = notes_selected if notes_selected else 'Awaiting Input...'
        
        instructions = FONT.render(f'Selected Notes: {notes_selected}', True, (0, 0, 0))
        screen.blit(instructions, (10, ainfo+90))

    instructions = FONT.render(f'Chord Functions: {CHORD_FUNCTIONS[mode+1]}', True, (0, 0, 0))
    screen.blit(instructions, (10, ainfo+120))

    #Button inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #This block is for [1] and [2] going forward and backward on the options and [3] to reset everything back to standard tuning on the instrument
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                button = (button - 1) % 5
            if event.key == pygame.K_2:
                button = (button + 1) % 5
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
                highlighted_notes = []
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
                    list_cuz_max_doesnt_work = []
                    for i in chord_show:
                        if i != None:
                            list_cuz_max_doesnt_work.append(i)
                    if not list_cuz_max_doesnt_work:
                        list_cuz_max_doesnt_work.append(0)
                    chord_show_max = max(list_cuz_max_doesnt_work)
                    if fretboard_len - 1 > chord_show_max:
                        fretboard_len -= 1
                        notess, fretboard = scale(pos,mode)
                        frets = visuals(fretboard, notess)

            elif button == 4:
                if event.key == pygame.K_RIGHT:
                    cid_toggle = (cid_toggle + 1) % 2
                    chord_show = [None]*len(tuning)
                    highlighted_notes = []
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_LEFT:
                    cid_toggle = (cid_toggle - 1) % 2
                    chord_show = [None]*len(tuning)
                    highlighted_notes = []
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

                if cid_toggle == 0:
                    if chord_show[string] == fret:
                        chord_show[string] = None
                    else:
                        chord_show[string] = fret

                else:
                    if (NOTES[tuning[string]]+fret)%12 not in highlighted_notes:
                        highlighted_notes.append((NOTES[tuning[string]]+fret)%12)
                    elif (NOTES[tuning[string]]+fret)%12 in highlighted_notes:
                        highlighted_notes.remove((NOTES[tuning[string]]+fret)%12)

                notess, fretboard = scale(pos,mode)
                frets = visuals(fretboard, notess)
                
                      
    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()