#imports

import random, numpy as np

import pandas as pd

from random import randint

outside_Psychopy = 0

try:
   from psychopy import core, event, gui, visual
except:
   outside_Psychopy = 1

if outside_Psychopy == 0:
    # define instructions presentation function
    # present instructions, keys are defined as arguments (strings!)
    def navigate_instructions(win, instructions_list, left, right, escape, begin):
        page = 0
        lastPage = len(instructions_list)-1
        no_page = lastPage+1
        backForward = [left, right, escape, begin]
        while page < no_page:
            instruction = instructions_list[page]
            instruction.draw()
            win.flip()
            press = event.waitKeys(keyList = backForward)
            #print press
            if press == [left]:
                if page != 0:
                   page = page - 1
            elif press == [right]:
                    if page != lastPage:
                       page = page + 1
            elif press == [escape]:
                core.quit()
            elif press == [begin] and page == lastPage:
                page = no_page