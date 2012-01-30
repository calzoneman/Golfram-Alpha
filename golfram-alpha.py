import argparse
import pickle
from random import choice

import pygame

import golfram.config
from golfram.core import Level
from golfram.util import error, get_path, info

# Some constants that should maybe eventually be relocated.
# Maybe to a Settings class.
GOLFRAM_ALPHA = 'Golfram Alpha'
VERSION = 'golfram-alpha-0.1'
RESOLUTION = [640,480]

# Load golfram settings
golfram.config.load('settings.ini')

# Parse command line arguments
parser = argparse.ArgumentParser(description="Play a nice game of minigolf.")
parser.add_argument('-v', '--version', action='version', version=VERSION)
parser.add_argument('-l', '--levelset', action='store', dest='levelset',
                    help="the levelset file you wish to play")
parser.add_argument('--bunny', action='store_true', dest='bunny')
args = parser.parse_args()

if not args.bunny and not args.levelset:
    parser.print_usage()

# Print a bunny, if requested
if args.bunny:
    try:
        bunnies = pickle.load(open('bunnies', 'r'))
    except:
        print("Bunnies are unavailable. No further information is available " +
              "because the code in this area is hacked together and uses a " +
              "bare except clause that catches numerous types of errors.")
    else:
        print(choice(bunnies))

# Load the specified levelset, if requested
if args.levelset:
    #info("Loading levelset {}".format(args.levelset))
    info("Ignoring levelset {}; loading demo.lvl".format(args.levelset))
    # Create game object, load levels, whatever...
    TEST_LEVEL = get_path('demo.lvl', filetype='level')
    level = Level.load_file(TEST_LEVEL)

    # Set up a basic pygame window
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(GOLFRAM_ALPHA)

    # Draw the level
    level_surface = pygame.Surface(screen.get_size()).convert()
    level.draw_on_surface(level_surface)
    screen.blit(level_surface, dest=(0, 0))
    pygame.display.flip()

    # exit
    pygame.quit()
