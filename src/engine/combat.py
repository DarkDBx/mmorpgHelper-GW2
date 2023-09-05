from logging import debug, info, error
from random import uniform
from time import sleep
from pydirectinput import keyDown, keyUp, press

from helper import image_helper, timer_helper, config_helper
from helper.timer_helper import TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"


cfg = config_helper.read_config()
class_var = cfg['class']
comboKey = cfg['comboKey']
swap = cfg['swap']
skill1 = cfg['skill01']
skill2 = cfg['skill02']
skill3 = cfg['skill03']
skill4 = cfg['skill04']
skill5 = cfg['skill05']
skill6 = cfg['skill06']
skill7 = cfg['skill07']
skill8 = cfg['skill08']
skill9 = cfg['skill09']
skill10 = cfg['skill10']

timer1 = timer_helper.TimerHelper('timer1')


def press_combo(key):
    keyDown(comboKey)
    press(key)
    keyUp(comboKey)


def rotation():
    """set up the skill rotation for a specific class, by the config value"""
    if class_var == 'Harbinger':
        combat_rotation('har')
    elif class_var == 'Willbender':
        combat_rotation('wil')
    elif class_var == 'Vindicator':
        combat_rotation('vin')
    elif class_var == 'Untamed':
        combat_rotation('unt')
    elif class_var == 'Soulbeast':
        combat_rotation('sb')
    elif class_var == 'Specter':
        combat_rotation('spe')
    else:
        error('No vaible class')


def combat_rotation(value):
    # target check
    if image_helper.pixel_matches_color(783,94, 147,33,18, 50) or image_helper.pixel_matches_color(783,99, 147,33,18, 50): # or image_helper.line_detection('mob') != False:
        # class check
        if value == 'unt':
            # https://guildjen.com/power-untamed-pvp-build/
            debug('Use untamed skillset')
            pass
        elif value == 'sb':
            # https://guildjen.com/sic-em-soulbeast-pvp-build/
            debug('Use soulbeast skillset')
            # health check
            if not image_helper.pixel_matches_color(960,1006, 156,19,2) and image_helper.locate_needle(SKILLPATH+value+'\\06.png', conf=0.9): # heal below 60%
                press(skill6)
                sleep_timing = uniform(0.8, 0.85)
                info('Use ability 6, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif not image_helper.pixel_matches_color(960,995, 178,27,5) and image_helper.locate_needle(SKILLPATH+value+'\\07.png', conf=0.9): # below 70%
                press(skill7)
                sleep_timing = uniform(0.05, 0.1)
                info('Use ability 7, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif not image_helper.pixel_matches_color(960,987, 181,25,5) and image_helper.locate_needle(SKILLPATH+value+'\\09.png', conf=0.9): # below 80%
                press(skill9)
                sleep_timing = uniform(0.05, 0.1)
                info('Use ability 9, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+value+'\\10.png', conf=0.9):
                press(skill10)
                sleep_timing = uniform(0.3, 0.35)
                info('Use ability 10, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\08.png', conf=0.9):
                press(skill8)
                sleep_timing = uniform(0.05, 0.1)
                info('Use ability 8, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\s01.png', conf=0.9):
                press_combo('1')
                sleep_timing = uniform(0.8, 0.85)
                info('Use ability shift+1, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\s01-2.png', conf=0.9):
                press_combo('1')
                sleep_timing = uniform(0.55, 0.6)
                info('Use ability shift+1, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\s02.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\s02-2.png', conf=0.9):
                press_combo('2')
                sleep_timing = uniform(1.05, 1.1)
                info('Use ability shift+2, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\s03.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\s03-2.png', conf=0.9):
                press_combo('3')
                sleep_timing = uniform(0.8, 0.85)
                info('Use ability shift+3, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+'swap.png', conf=0.9):
                press(swap)
                sleep_timing = uniform(0.3, 0.35)
                info('Use ability weapon swap, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
                press_combo('4')
                sleep_timing = uniform(0.3, 0.35)
                info('Use ability pet swap, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
                if image_helper.locate_needle(SKILLPATH+value+'\\s05.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\s05-2.png', conf=0.9):
                    press_combo('5')
                    sleep_timing = uniform(0.3, 0.35)
                    info('Use ability shift+5, next execution in ' + str(sleep_timing) + ' seconds')
                    sleep(sleep_timing)
            # standard rotation
            elif image_helper.locate_needle(SKILLPATH+value+'\\03.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\03-2.png', conf=0.9):
                press(skill3)
                sleep_timing = uniform(0.55, 0.6)
                info('Use ability 3, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\02.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\02-2.png', conf=0.9):
                press(skill2)
                sleep_timing = uniform(0.55, 0.6)
                info('Use ability 2, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\05.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\05-2.png', conf=0.9):
                press(skill5)
                sleep_timing = uniform(0.55, 0.6)
                info('Use ability 5, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)
            elif image_helper.locate_needle(SKILLPATH+value+'\\04.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\04-2.png', conf=0.9):
                press(skill4)
                sleep_timing = uniform(0.55, 0.6)
                info('Use ability 4, next execution in ' + str(sleep_timing) + ' seconds')
                sleep(sleep_timing)

