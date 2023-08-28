from logging import debug, info, error
from random import uniform
from time import sleep

from helper import input_helper, image_helper, timer_helper, config_helper
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
    input_helper.keyDown(comboKey)
    input_helper.press(key)
    input_helper.keyUp(comboKey)


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
                input_helper.press(skill6)
                info('Execute ability 6')
                sleep(.75)
            elif not image_helper.pixel_matches_color(960,995, 178,27,5) and image_helper.locate_needle(SKILLPATH+value+'\\07.png', conf=0.9): # below 70%
                input_helper.press(skill7)
                info('Execute ability 7')
            elif not image_helper.pixel_matches_color(960,987, 181,25,5) and image_helper.locate_needle(SKILLPATH+value+'\\09.png', conf=0.9): # below 80%
                input_helper.press(skill9)
                info('Execute ability 9')
            # class skill checks
            elif image_helper.locate_needle(SKILLPATH+value+'\\10.png', conf=0.9):
                input_helper.press(skill10)
                info('Execute ability 10')
                sleep(.25)
            elif image_helper.locate_needle(SKILLPATH+value+'\\08.png', conf=0.9):
                input_helper.press(skill8)
                info('Execute ability 8')
            elif image_helper.locate_needle(SKILLPATH+value+'\\s01.png', conf=0.9):
                press_combo('1')
                info('Execute ability shift+1')
                sleep(.75)
            elif image_helper.locate_needle(SKILLPATH+value+'\\s01-2.png', conf=0.9):
                press_combo('1')
                info('Execute ability shift+1')
                sleep(.5)
            elif image_helper.locate_needle(SKILLPATH+value+'\\s02.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\s02-2.png', conf=0.9):
                press_combo('2')
                info('Execute ability shift+2')
                sleep(1)
            elif image_helper.locate_needle(SKILLPATH+value+'\\s03.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\s03-2.png', conf=0.9):
                press_combo('3')
                info('Execute ability shift+3')
                sleep(.75)
            elif image_helper.locate_needle(SKILLPATH+'swap.png', conf=0.9):
                input_helper.press('q')
                info('Execute ability weapon swap')
                sleep(.25)
                press_combo('4')
                info('Execute ability pet swap')
                sleep(.25)
                if image_helper.locate_needle(SKILLPATH+value+'\\s05.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\s05-2.png', conf=0.9):
                    press_combo('5')
                    info('Execute ability shift+5')
                    sleep(.25)
            # standard rotation
            elif image_helper.locate_needle(SKILLPATH+value+'\\03.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\03-2.png', conf=0.9):
                input_helper.press(skill3)
                info('Execute ability 3')
                sleep(.5)
            elif image_helper.locate_needle(SKILLPATH+value+'\\02.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\02-2.png', conf=0.9):
                input_helper.press(skill2)
                info('Execute ability 2')
                sleep(.5)
            elif image_helper.locate_needle(SKILLPATH+value+'\\05.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\05-2.png', conf=0.9):
                input_helper.press(skill5)
                info('Execute ability 5')
                sleep(.5)
            elif image_helper.locate_needle(SKILLPATH+value+'\\04.png', conf=0.9) or image_helper.locate_needle(SKILLPATH+value+'\\04-2.png', conf=0.9):
                input_helper.press(skill4)
                info('Execute ability 4')
                sleep(.5)

