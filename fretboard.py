import pygame

pygame.init()

#Just initializing all of the constants

AWIDTH, WIDTH, AHEIGHT, HEIGHT = 1240, 1200, 430, 300
screen = pygame.display.set_mode((AWIDTH, AHEIGHT))
RED = (255,0,0)
GREEN = (0,255,0)
GREY = (100,100,100)
BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.display.set_caption("Fretboard Visualizer")
FONT = pygame.font.SysFont('Segoe UI Symbol', 15)
CLOCK = pygame.time.Clock()

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

#Just a bunsh of variables that help to handle the math and modular stuff
tuning = TUNINGS[instruments[instrument_index]][:]

#searching is used to pick out the notes from the scale 
#switch is to handle the math for switching between the modes and stay on the same note
searching = [0,2,4,5,7,9,11]
switch = [2,2,1,2,2,2,1]
pos = 0
mode = 0
button = 0
string = 0

def scale(position,mode):
    #This handles all of the math for mapping out the notes and where they go on the fretboard
    notess = []
    searching = [0,2,4,5,7,9,11]
    fretboard = [[None for _ in range(12)] for _ in range(len(tuning))]
    for i, x in enumerate(searching):
        searching[i] = (x+position) % 12
        notess.append(SETON[(x+position) % 12].upper())
    for i, x in enumerate(tuning):
        for z in range(12):
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
            if key and root:
                frets.append((pygame.Rect(WIDTH//12*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//12,HEIGHT//(len(tuning))), RED, note))
            elif key and not root:
                frets.append((pygame.Rect(WIDTH//12*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//12,HEIGHT//(len(tuning))), GREY, note))
            else:
                frets.append((pygame.Rect(WIDTH//12*y,HEIGHT//(len(tuning))*((len(tuning)-1)-i),WIDTH//12,HEIGHT//(len(tuning))), WHITE, note))
    for i in range(mode):
        notess.append(notess.pop(0))

    return frets

#Just initializes everything
notess, fretboard = scale(pos,mode)
frets = visuals(fretboard, notess)

#running loop
running = True
while running:
    screen.fill(WHITE)

    #Draws the frets
    for i in frets:
        a, b, c = i
        pygame.draw.rect(screen, b, a)
        pygame.draw.rect(screen, BLACK, a, width=2)
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

    #Draws all of the text for the instructions and other visuals

    color = GREEN if button == 0 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 310))

    color = GREEN if button == 1 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 340))

    color = GREEN if button == 2 else RED
    tuning_text = FONT.render('⬛', True, color)
    screen.blit(tuning_text, (10, 370))

    scale_text = FONT.render(f'{SETON[(searching[mode] + pos) % 12].upper()} {MODES[mode]} | {notess[0]}, {notess[1]}, \
{notess[2]}, {notess[3]}, {notess[4]}, {notess[5]}, {notess[6]} ', True, (0, 0, 0))
    screen.blit(scale_text, (30, 310))

    tuning_text = FONT.render(f'Tuning: {"".join(tuning).upper()}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 340))

    tuning_text = FONT.render(f'Instrument: {instruments[instrument_index]}', True, (0, 0, 0))
    screen.blit(tuning_text, (30, 370))

    instructions = FONT.render('[LEFT/RIGHT] to change root note | [UP/DOWN] to change mode', True, (100, 100, 100))
    screen.blit(instructions, (320, 310))

    instructions = FONT.render('[LEFT/RIGHT] to tune the string | [UP/DOWN] to change string', True, (100, 100, 100))
    screen.blit(instructions, (320, 340))

    instructions = FONT.render('[LEFT/RIGHT] to change the instrument', True, (100, 100, 100))
    screen.blit(instructions, (320, 370))

    instructions = FONT.render('press [1] and [2] to switch between changing the tuning, changing the scale, and changing instrument | [3] to reset everything', True, (100, 100, 100))
    screen.blit(instructions, (320, 400))

    #Button inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #This block is for [1] and [2] going forward and backward on the options and [3] to reset everything back to standard tuning on the instrument
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                button = (button - 1) % 3
            if event.key == pygame.K_2:
                button = (button + 1) % 3
            if event.key == pygame.K_3:
                tuning = TUNINGS[instruments[instrument_index]][:]
                searching = [0,2,4,5,7,9,11]
                pos = 0
                mode = 0
                string = 0
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
                    
            #This block handles changning the instrument
            elif button == 2:
                if event.key == pygame.K_RIGHT:
                    instrument_index = (instrument_index + 1) % len(instruments)
                    tuning = TUNINGS[instruments[instrument_index]][:]
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                elif event.key == pygame.K_LEFT:
                    instrument_index = (instrument_index - 1) % len(instruments)
                    tuning = TUNINGS[instruments[instrument_index]][:]
                    notess, fretboard = scale(pos,mode)
                    frets = visuals(fretboard, notess)
                    
    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()