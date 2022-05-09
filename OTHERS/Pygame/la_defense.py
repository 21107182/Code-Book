import pygame, sys, csv
import random
from colors import rgb, hex

# Function to translate coordinates to screen pixel
def mapCoordinates(latlon):
    y = screen_centre[1] - ((float(latlon[0]) - map_centre[1]) * scaling)
    x = screen_centre[0] + ((float(latlon[1]) - map_centre[0]) * scaling)
    return[int(x),int(y)]

# Class to define photo object
class Building:
    def __init__(self, name, built_year, use, height, levels, lat, lon, address):
        self.name = name
        self.built_year = built_year
        self.use = use
        self.height = height
        self.levels = levels
        self.lat = lat
        self.lon = lon
        self.address = address

    # function to draw a building dot
    def draw(self, screen, colour, size):
        centre = mapCoordinates([self.lat,self.lon])
        pygame.draw.circle(screen, colour, centre, size)
    
    # function to show label of a budiling
    def label(self, screen, colour, size):
        centre = mapCoordinates([self.lat,self.lon])
        label_font = pygame.freetype.SysFont('Arial', size)
        if centre[0] < screen_centre[0]:
            label_font.render_to(screen, (centre[0]-10, centre[1]+5), self.name, colour)
        else:
            label_font.render_to(screen, (centre[0]-25, centre[1]+5), self.name, colour)
        
    # function to show building information
    def info(self, screen, y):
        info_font = pygame.freetype.SysFont('Arial', 15)
        info_font.render_to(screen, (screen_width-text_x, y + 25 * 0), 'Name: ' + self.name, (0, 0, 0))
        info_font.render_to(screen, (screen_width-text_x, y + 25 * 1), 'Built Year: ' + self.built_year, (0, 0, 0))
        info_font.render_to(screen, (screen_width-text_x, y + 25 * 2), 'Use: ' + self.use, (0, 0, 0))
        info_font.render_to(screen, (screen_width-text_x, y + 25 * 3), 'Height: ' + self.height, (0, 0, 0))
        info_font.render_to(screen, (screen_width-text_x, y + 25 * 4), 'Levels: ' + self.levels, (0, 0, 0))

# Define Game parameters
# screen size
screen_width = 1120
screen_height = 630
screen_centre = [screen_width/2, screen_height/2]
buffer = int(screen_height/100)
ps = int(buffer/10)

# information box
show_im = False
box_x = 320
box_y = 20
text_x = 320 - 15
text_y = 20 + 15

# Contrast mode
contrast_mode = False

'''photoIndex = 0'''

# Set the coordinate frame you want to visualise
lim_coord = [48.8840894, 2.2300521, 48.8983561, 2.254052]
lim_width = lim_coord[3]-lim_coord[1]
lim_height = lim_coord[2]-lim_coord[0]
map_centre = [lim_width/2 + lim_coord[1], lim_height/2 + lim_coord[0]]
scaling = min(screen_width/lim_width, screen_height/lim_height)

# List of buildings read in from the csv file
buildings = []
with open('la_defense_buildings.csv') as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
        name = row['Name']
        built_year = row['Built']
        use = row['Use']
        height = row['Height_metres']
        levels = row['Levels']
        lat = row['Latitude']
        lon = row['Longitude']
        address = row['Address']
        buildings.append(Building(name, built_year, use, height, levels, lat, lon, address))

# Selected Buildings
sel_buildings = []

# Initialise the game window
pygame.init()
pygame.display.set_caption('La Defense Map')

# Set the game surface
screen = pygame.display.set_mode((screen_width, screen_height))

# Extra surfacse overlayed for curser and photo interaction
building_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
sel_building_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
box_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
label_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
mouse_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
info_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)

# A clock to keep track of the game progress
clock = pygame.time.Clock()

# Any commands that draw the initial state of the game
screen.fill(pygame.Color('black'))

# Set background images
backgr_image = pygame.image.load('static.png')
backgr_image = pygame.transform.scale(backgr_image, (screen_width, screen_height))

# Update before the first frame
pygame.display.update()

# Draw all buildings from the start
building_surface.fill((0,0,0,0))
for b in buildings:
    b.draw(building_surface, (100,100,100), 2)
    b.label(label_surface, (100,100,100), 10)

# The game loop, in here the behaviour of the game is defined.
# This loop is executed every frame.
while True:
    # wipe mouse surface:
    mouse_surface.fill((0,0,0,0))

    # Get key events to check if something is going on through some form of input.
    events = pygame.event.get()
    for event in events:
        # Check exit through x button window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Go through all key presses, which you can use to controll the game.
        elif event.type == pygame.KEYDOWN:
            # Check exit through esc
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Switch between map mode and contrast mode
            if event.key == pygame.K_c:
                contrast_mode = True
                info_surface.fill((0,0,0,0))
                box_surface.fill((0,0,0,0))
                sel_building_surface.fill((0,0,0,0))
                sel_buildings.clear()
            if event.key == pygame.K_m:
                contrast_mode = False
                info_surface.fill((0,0,0,0))
                sel_building_surface.fill((0,0,0,0))
                box_surface.fill((0,0,0,0))
                sel_buildings.clear()

    # Define any drawings
    # draw buildings gradually
    """for i in range(photoIndex, min(photoIndex + 100, len(photos))):
        photos[i].draw(screen, 1)"""
    # update variables
    """if photoIndex < len(photos):
        photoIndex += 100"""

    # draw mouse
    mouseP = pygame.mouse.get_pos()
    pygame.draw.line(mouse_surface, (100,100,100), (mouseP[0], 0), (mouseP[0], screen_height), 1)
    pygame.draw.line(mouse_surface, (100,100,100), (0, mouseP[1]), (screen_width, mouseP[1]), 1)
    
    
    # Map mode: select a building and press the left mouse button to display its information
    if contrast_mode == False:
        title_font = pygame.freetype.SysFont('Arial', 15)
        title_font.render_to(box_surface, (20,20), 'MAP MODE', (0, 0, 0))
        for b in buildings:
            xb, yb = mapCoordinates([b.lat, b.lon])
            if mouseP[0] - 5 <= xb <= mouseP[0] + 5 and mouseP[1] - 5 <= yb <= mouseP[1] + 5:
                b.draw(mouse_surface, (150, 50, 50), 5)
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(info_surface, (0,0,0,80), pygame.Rect(screen_width-box_x, box_y,300, 590))
                    b.info(info_surface,text_y)
                    try:
                        cell_image = pygame.image.load('Dataset/' + b.address + '/Image_1.jpg')
                        im_width, im_height = cell_image.get_size()
                        f = 270 / im_width
                        cell_image = pygame.transform.scale(cell_image, (int(f * im_width), int(f * im_height)))
                        show_im = True
                    except FileNotFoundError:
                        show_im = False
                    
            # Press the right mouse button to stop displaying information           
            if pygame.mouse.get_pressed()[2]:
                info_surface.fill((0,0,0,0))
                show_im = False
                
    # Contrast mode: select no more than 3 buildings and compare their information
    if contrast_mode == True:
        show_im = False
        title_font = pygame.freetype.SysFont('Arial', 15)
        title_font.render_to(box_surface, (20,20), 'CONTRAST MODE', (0, 0, 0))
        pygame.draw.rect(box_surface, (0,0,0,80), pygame.Rect(screen_width-box_x, box_y,300, 590))
        
        # Press the left mouse button to compare building informations
        for b in buildings:
            xb, yb = mapCoordinates([b.lat, b.lon])
            if mouseP[0] - 5 <= xb <= mouseP[0] + 5 and mouseP[1] - 5 <= yb <= mouseP[1] + 5:
                b.draw(mouse_surface, (150, 50, 50), 5)
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.circle(sel_building_surface, (150, 50, 50), mapCoordinates([b.lat,b.lon]), 5)
                    sel_buildings.append(b)
                    b.info(info_surface,text_y*(sel_buildings.index(b)*0.4 + 1))
        
        # Press the right mouse button to stop comparing
        if pygame.mouse.get_pressed()[2]:
            info_surface.fill((0,0,0,0))
            sel_building_surface.fill((0,0,0,0))
            sel_buildings.clear()

    # At the end of the loop update the screen and game time.
    screen.blit(backgr_image, [0,0])
    screen.blit(building_surface, [0,0])
    screen.blit(box_surface, [0,0])
    screen.blit(sel_building_surface, [0,0])
    screen.blit(label_surface, [0,0])
    screen.blit(mouse_surface, [0,0])
    screen.blit(info_surface, [0,0])
    if show_im:
        screen.blit(cell_image, [screen_width - text_x, text_y + 25 * 5])
    pygame.display.update()
    clock.tick()
