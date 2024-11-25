import os

import colorama

from features.utils.console import draw_string
from colorama import Fore

Y = Fore.LIGHTBLACK_EX
R = Fore.LIGHTBLACK_EX
RS = Fore.RESET
W = Fore.LIGHTWHITE_EX

ART = f"""
    {R}.------. .------. {Y}.------.
    {R}|{W}L{R}.--. | |{W}L{R}.--. | {Y}|{W}S{Y}.--. |
    {R}| :{W}/\\{R}: |{R} | :{W}/\\{R}: | {Y}| :{W}/\\{Y}: |
    {R}| {W}(__){R} | | {W}(__){R} | {Y}| :{W}\/{Y}: |
    {R}| '--'{W}L{R}| | '--'{W}L{R}| {Y}| '--'{W}S{Y}|
    {R}`------' `------' {Y}`------'
{RS}"""


def draw_art():
    print(ART)


def render_gui():
    draw_string("Main menu, select action: \n")
    draw_string("1: Encrypt a block of data")
    draw_string("2: Unmount encrypted data block")
    draw_string("3: LLS Settings")
    draw_string("4: Password Manager")
    draw_string("5: Hash bruteforce")
    draw_string("6: Shutdown")
