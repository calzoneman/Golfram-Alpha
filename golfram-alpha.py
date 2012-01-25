import argparse
import pickle
from random import choice

import pygame

import golfram.config
from golfram.core import Level

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
parser.add_argument('-l', '--levelset',
                    help="the levelset file you wish to play")
parser.add_argument('--bunny', dest='bunny', action='store_true')
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
              "bare except clause.")
    else:
        print(choice(bunnies))

# Load the specified levelset, if requested
if args.levelset:
    # Create game object, load levels, whatever...

    # Set up a basic pygame window
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(GOLFRAM_ALPHA)

    # do stuff

    # exit
    pygame.quit()
