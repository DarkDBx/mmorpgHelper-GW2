from logging import debug, info, error
from random import uniform
from time import sleep
from pydirectinput import keyDown, keyUp, press
from os import path

from inc import image_helper, timer_helper, config_helper
from inc.timer_helper import TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"
PLAYER_POS_X = 760
PLAYER_POS_Y = 500
ATTACKDIST = 180
MELEEDIST = 60


effectRegion = (1018, 887, 1411, 994)
cfg = config_helper.read_config()
playerClass = cfg['playerClass']
comboKey = cfg['comboKey']
stompKey = cfg['stompKey']
weaponSwap = cfg['weaponSwap']
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


def test_effect(file_name, region):
    for i in range(1, 30):
        if not path.exists('.\\assets\\test\\' + file_name + str(i) + '.png'):
            image_helper.get_image_at_position(file_name + str(i), region=region)
            break


def is_effect(effect, confidence):
    x, y = image_helper.locate_needle('.\\assets\\effects\\' + effect + '.png', conf=confidence, loctype='c', region=effectRegion)
    if x != -1 and y != -1:
        #test_effect(effect, region=(x, y, 12, 12))
        return True
    return False


def use_skill(key, sleep_min, sleep_max):
    press(key)
    sleep_timing = uniform(sleep_min, sleep_max)
    info('Use ability ' + str(key) + ', next execution in ' + str(sleep_timing) + ' seconds')
    sleep(sleep_timing)


def use_skill_combo(key, sleep_min, sleep_max):
    keyDown(comboKey)
    press(key)
    keyUp(comboKey)
    sleep_timing = uniform(sleep_min, sleep_max)
    info('Use ability ' + str(comboKey) + ' + ' + str(key) + ', next execution in ' + str(sleep_timing) + ' seconds')
    sleep(sleep_timing)


def rotation():
    """set up the skill rotation for a specific class, by the config value"""
    if playerClass == 'Soulbeast PvP':
        combat_rotation('sb_pvp')
    elif playerClass == 'Soulbeast PvE':
        combat_rotation('sb_pve')
    else:
        error('No vaible class')


def combat_rotation(value):
    # target check
    if image_helper.pixel_matches_color(783,94, 147,33,18) or image_helper.pixel_matches_color(784,94, 79,16,8):
        if cfg['showHUD'] == '1':
            dist = image_helper.target_lines(ATTACKDIST, PLAYER_POS_X, PLAYER_POS_Y)
            info('Distance to target: ' + str(dist))
        else:
            dist = False
    
        # self downed state
        if image_helper.pixel_matches_color(800,900, 101,2,8):
            if value == 'sb_pvp' or value == 'sb_pve':
                if image_helper.locate_needle(SKILLPATH + value + '\\d03.png', conf=0.9):
                    use_skill('3', 0.1, 0.15)
                elif image_helper.locate_needle(SKILLPATH + value + '\\d01.png', conf=0.9):
                    use_skill('1', 0.1, 0.15)
        elif dist != -1:
            # test effects
            if is_effect('stun', 0.7):
                debug('STUNNED')
            if is_effect('daze', 0.7):
                debug('DAZED')
            if is_effect('immobile', 0.96):
                debug('IMMOBILE')
            if is_effect('chilled', 0.9):
                debug('CHILLED')
            if is_effect('stability', 0.6):
                debug('STABILITY')
            if is_effect('protection', 0.7):
                debug('PROTECTION')
            if is_effect('aegis', 0.8):
                debug('AEGIS')
            
            # stomp downed players in pvp
            if image_helper.pixel_matches_color(891,95, 81,16,8): # downed above 40% health
                use_skill(stompKey, 0.1, 0.15)
            # profile check
            elif value == 'sb_pvp':
                # https://guildjen.com/sic-em-soulbeast-pvp-build/
                # https://guildjen.com/sic-em-soulbeast-roaming-build/
                debug('Use soulbeast skillset')
                
                # health dependent
                if not image_helper.pixel_matches_color(929,1015, 134,15,5) and image_helper.locate_needle(SKILLPATH + value + '\\09.png', conf=0.9): # below 50%  or (is_stun() or is_immobile())
                    use_skill(skill9, 0.1, 0.15)
                elif not image_helper.pixel_matches_color(935,1002, 154,17,2) and image_helper.locate_needle(SKILLPATH + value + '\\07.png', conf=0.9): # below 60%  or (not is_stability() and is_stun())
                    use_skill(skill7, 0.1, 0.15)
                elif not image_helper.pixel_matches_color(933,994, 170,23,2) and image_helper.locate_needle(SKILLPATH + value + '\\06.png', conf=0.9): # heal below 70%
                    use_skill(skill6, 0.85, 0.9)
                # class skills
                elif image_helper.locate_needle(SKILLPATH + value + '\\s01-3.png', conf=0.9): # beastmode
                    use_skill_combo('5', 0.1, 0.15)
                elif not image_helper.pixel_matches_color(784,94, 79,16,8) and image_helper.locate_needle(SKILLPATH + value + '\\10.png', conf=0.9):
                    use_skill(skill10, 0.351, 0.4)
                elif not image_helper.pixel_matches_color(784,94, 79,16,8) and image_helper.locate_needle(SKILLPATH + value + '\\08.png', conf=0.9):
                    use_skill(skill8, 0.1, 0.15)
                # weapon and pet swap
                elif image_helper.locate_needle(SKILLPATH + 'swap.png', conf=0.9):
                    use_skill(weaponSwap, 0.1, 0.15)
                    use_skill_combo('4', 0.1, 0.15)
                # 2h bow
                elif image_helper.locate_needle(SKILLPATH + value + '\\04.png', conf=0.9) and (dist < MELEEDIST or dist == False):
                    use_skill(skill4, 0.6, 0.65)
                elif image_helper.locate_needle(SKILLPATH + value + '\\02.png', conf=0.9):
                    use_skill(skill2, 2.6, 2.65)
                # professions
                elif not image_helper.pixel_matches_color(784,94, 79,16,8) and image_helper.locate_needle(SKILLPATH + value + '\\s02.png', conf=0.9) and (dist > MELEEDIST or dist == False):
                    use_skill_combo('2', 0.1, 0.15)
                elif not image_helper.pixel_matches_color(784,94, 79,16,8) and image_helper.locate_needle(SKILLPATH + value + '\\s02-2.png', conf=0.9) and (dist > MELEEDIST or dist == False):
                    use_skill_combo('2', 1.1, 1.15)
                elif not image_helper.pixel_matches_color(784,94, 79,16,8) and image_helper.locate_needle(SKILLPATH + value + '\\s01.png', conf=0.9) and (dist < MELEEDIST or dist == False):
                    use_skill_combo('1', 0.85, 0.9)
                elif not image_helper.pixel_matches_color(784,94, 79,16,8) and image_helper.locate_needle(SKILLPATH + value + '\\s01-2.png', conf=0.9) and (dist < MELEEDIST or dist == False):
                    use_skill_combo('1', 0.6, 0.65)
                elif not image_helper.pixel_matches_color(784,94, 79,16,8) and image_helper.locate_needle(SKILLPATH + value + '\\s03.png', conf=0.9) and (dist < MELEEDIST or dist == False):
                    use_skill_combo('3', 0.85, 0.9)
                # 2h sword
                elif image_helper.locate_needle(SKILLPATH + value + '\\03-2.png', conf=0.9) and (dist > MELEEDIST or dist == False):
                    use_skill(skill3, 0.85, 0.9)
                elif image_helper.locate_needle(SKILLPATH + value + '\\02-2.png', conf=0.9) and (dist < MELEEDIST or dist == False):
                    use_skill(skill2, 0.85, 0.9)
                elif image_helper.locate_needle(SKILLPATH + value + '\\05-2.png', conf=0.9) and (dist < MELEEDIST or dist == False):
                    use_skill(skill5, 0.6, 0.65)
            # profile check
            elif value == 'sb_pve':
                # https://guildjen.com/power-soulbeast-build/
                pass

