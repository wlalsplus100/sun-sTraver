from asyncio import shield
from math import trunc
from re import A, X
from tkinter import N, Y
from winsound import PlaySound
from aiohttp import ServerFingerprintMismatch
import pygame, sys, random, time
######################################################################################################
# 기본 초기화 (꼭 해야함)
pygame.init()
pygame.mixer.init()

#화면 크기 설정
screen_width = 720 #스크린 가로크기
screen_height = 720 #스크린 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("선이의 모험") #게임 이름

#FPS
clock = pygame.time.Clock()

######################################################################################################
#1.사용자 게임 초기화(배경화면,게임이미지,캐릭터,폰트,이동속도)
font_size = 15
font = pygame.font.Font('C:\\Windows\\Fonts\\batang.ttc',font_size)


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)



titles = pygame.image.load('.\\resource\\제목.png')
titles_size = titles.get_rect().size
titles_width = titles_size[0]
titles_height = titles_size[1]
titles_x_pos = 0
titles_y_pos = 0

new_game = pygame.image.load('.\\resource\\새게임.jpg')
new_game_size = new_game.get_rect().size
new_game_width = new_game_size[0]
new_game_height = new_game_size[1]
new_game_x_pos = screen_width / 2 - new_game_width / 2
new_game_y_pos = 500

following = pygame.image.load('.\\resource\\이어하기.jpg')
following_size = following.get_rect().size
following_width = following_size[0]
following_height = following_size[1]
following_x_pos = screen_width / 2 - following_width / 2
following_y_pos = 565

exit = pygame.image.load('.\\resource\\게임종료.jpg')
exit_size = exit.get_rect().size
exit_width = exit_size[0]
exit_height = exit_size[1]
exit_x_pos = screen_width / 2 - exit_width / 2
exit_y_pos = 630

gameui = pygame.image.load('.\\resource\\게임UI.png')
gameui_x_pos = 0
gameui_y_pos = 0

items = pygame.image.load('.\\resource\\아이템.png')
items_size = items.get_rect().size
items_width = items_size[0]
items_height = items_size[1]
items_x_pos = 5
items_y_pos = 100

skills = pygame.image.load('.\\resource\\스킬버튼.png')
skills_size = skills.get_rect().size
skills_width = skills_size[0]
skills_height = skills_size[1]
skills_x_pos = 5
skills_y_pos = 200

dialog = pygame.image.load('.\\resource\\대화창.png')

common_sword = pygame.image.load('.\\resource\\weapons\\평범한검.png')
common_healthy = pygame.image.load('.\\resource\\weapons\\평범한갑옷.png')
common_shield = pygame.image.load('.\\resource\\weapons\\평범한방패.png')
lightning_sword = pygame.image.load('.\\resource\\weapons\\번개의검.png')
grass_healthy = pygame.image.load('.\\resource\\weapons\\풀의갑옷.png')
iron_shield = pygame.image.load('.\\resource\\weapons\\철제방패.png')
dagger = pygame.image.load('.\\resource\\weapons\\단도.png')
lion_head_shield = pygame.image.load('.\\resource\\weapons\\곰방패.png')
copper_healthy = pygame.image.load('.\\resource\\weapons\\구리갑옷.png')
obsidian_sword = pygame.image.load('.\\resource\\weapons\\흑요석검.png')
platinum_healthy = pygame.image.load('.\\resource\\weapons\\백금갑옷.png')
wolf_head_shield = pygame.image.load('.\\resource\\weapons\\늑대방패.png')
shadow_sword = pygame.image.load('.\\resource\\weapons\\그림자검.png')
undead_shield = pygame.image.load('.\\resource\\weapons\\언데드방패.png')
emerald_healthy = pygame.image.load('.\\resource\\weapons\\에메랄드갑옷.png')
toxic_dagger = pygame.image.load('.\\resource\\weapons\\독묻은단검.png')
night_shield = pygame.image.load('.\\resource\\weapons\\밤의방패.png')
garnet_healthy = pygame.image.load('.\\resource\\weapons\\석류석갑옷.png')
fire_sword = pygame.image.load('.\\resource\\weapons\\불의검.png')
afternoon_shield = pygame.image.load('.\\resource\\weapons\\낮의방패.png')
sapphire_healthy = pygame.image.load('.\\resource\\weapons\\강옥갑옷.png')
star_sword = pygame.image.load('.\\resource\\weapons\\별의검.png')
dawn_shield = pygame.image.load('.\\resource\\weapons\\새벽의방패.png')
moonstone_healthy = pygame.image.load('.\\resource\\weapons\\문스톤갑옷.png')
optimization_sword = pygame.image.load('.\\resource\\weapons\\최적화검.png')
optimization_shield = pygame.image.load('.\\resource\\weapons\\최적화방패.png')
optimization_healthy = pygame.image.load('.\\resource\\weapons\\최적화갑옷.png')



swords = [common_sword, common_sword, lightning_sword, dagger, obsidian_sword, shadow_sword, toxic_dagger, fire_sword, star_sword, optimization_sword]
shields = [common_shield, common_shield, iron_shield, lion_head_shield, wolf_head_shield, undead_shield, night_shield, afternoon_shield, dawn_shield, optimization_shield]
healthys = [common_healthy, common_healthy, grass_healthy, copper_healthy, platinum_healthy, emerald_healthy, garnet_healthy, sapphire_healthy, moonstone_healthy, optimization_healthy]

#글테두리 만드는 함수에서 쓰는 함수(퍼옴)
_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points
#글테두리 만들 때 쓰는 함수(퍼옴)
def render(text, font, gfcolor=pygame.Color('yellow'), ocolor=(0, 0, 0), opx=1):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

weapons = {
    'sword' : common_sword,
    'shield' : common_shield,
    'healthy' : common_healthy
}

weapons_rating = {
    common_sword : font.render('common', True, (98, 98, 98)),
    lightning_sword : font.render('uncommon', True, (131, 255, 107)),
    common_shield : font.render('common', True, (98, 98, 98)),
    common_healthy : font.render('common', True, (98, 98, 98)),
    grass_healthy : font.render('uncommon', True, (131, 255, 107)),
    iron_shield : font.render('uncommon', True, (131, 255, 107)),
    dagger : font.render('uncommon', True, (131, 255, 107)),
    lion_head_shield : font.render('uncommon', True, (131, 255, 107)),
    copper_healthy : font.render('uncommon', True, (131, 255, 107)),
    obsidian_sword : font.render('uncommon', True, (131, 255, 107)),
    wolf_head_shield : font.render('uncommon', True, (131, 255, 107)),
    platinum_healthy : font.render('uncommon', True, (131, 255, 107)),
    shadow_sword : font.render('uncommon', True, (131, 255, 107)),
    undead_shield : font.render('uncommon', True, (131, 255, 107)),
    emerald_healthy : font.render('uncommon', True, (131, 255, 107)),
    toxic_dagger : font.render('epic', True, (75, 51, 98)),
    night_shield : font.render('epic', True, (75, 51, 98)),
    garnet_healthy : font.render('epic', True, (75, 51, 98)),
    fire_sword : font.render('epic', True, (75, 51, 98)),
    afternoon_shield : font.render('epic', True, (75, 51, 98)),
    sapphire_healthy : font.render('epic', True, (75, 51, 98)),
    star_sword : font.render('epic', True, (75, 51, 98)),
    dawn_shield : font.render('epic', True, (75, 51, 98)),
    moonstone_healthy : font.render('epic', True, (75, 51, 98)),
    optimization_sword : font.render('legendary', True, (255, 246, 53)),
    optimization_shield : font.render('legendary', True, (255, 246, 53)),
    optimization_healthy : font.render('legendary', True, (255, 246, 53))
}

big_images = {
    common_sword : pygame.image.load('.\\resource\\weapons\\image\\평범한검.png'),
    common_healthy : pygame.image.load('.\\resource\\weapons\\image\\평범한갑옷.png'),
    common_shield : pygame.image.load('.\\resource\\weapons\\image\\평범한방패.png'),
    lightning_sword : pygame.image.load('.\\resource\\weapons\\image\\번개의검.png'),
    grass_healthy : pygame.image.load('.\\resource\\weapons\\image\\풀의갑옷.png'),
    iron_shield : pygame.image.load('.\\resource\\weapons\\image\\철제방패.png'),
    dagger : pygame.image.load('.\\resource\\weapons\\image\\단도.png'),
    lion_head_shield : pygame.image.load('.\\resource\\weapons\\image\\곰방패.png'),
    copper_healthy : pygame.image.load('.\\resource\\weapons\\image\\구리갑옷.png'),
    obsidian_sword : pygame.image.load('.\\resource\\weapons\\image\\흑요석검.png'),
    platinum_healthy : pygame.image.load('.\\resource\\weapons\\image\\백금갑옷.png'),
    wolf_head_shield : pygame.image.load('.\\resource\\weapons\\image\\늑대방패.png'),
    shadow_sword : pygame.image.load('.\\resource\\weapons\\image\\그림자검.png'),
    undead_shield : pygame.image.load('.\\resource\\weapons\\image\\언데드방패.png'),
    emerald_healthy : pygame.image.load('.\\resource\\weapons\\image\\에메랄드갑옷.png'),
    toxic_dagger : pygame.image.load('.\\resource\\weapons\\image\\독묻은단검.png'),
    night_shield : pygame.image.load('.\\resource\\weapons\\image\\밤의방패.png'),
    garnet_healthy : pygame.image.load('.\\resource\\weapons\\image\\석류석갑옷.png'),
    fire_sword : pygame.image.load('.\\resource\\weapons\\image\\불의검.png'),
    afternoon_shield : pygame.image.load('.\\resource\\weapons\\image\\낮의방패.png'),
    sapphire_healthy : pygame.image.load('.\\resource\\weapons\\image\\강옥갑옷.png'),
    star_sword : pygame.image.load('.\\resource\\weapons\\image\\별의검.png'),
    dawn_shield : pygame.image.load('.\\resource\\weapons\\image\\새벽의방패.png'),
    moonstone_healthy : pygame.image.load('.\\resource\\weapons\\image\\문스톤갑옷.png'),
    optimization_sword : pygame.image.load('.\\resource\\weapons\\image\\최적화검.png'),
    optimization_shield : pygame.image.load('.\\resource\\weapons\\image\\최적화방패.png'),
    optimization_healthy : pygame.image.load('.\\resource\\weapons\\image\\최적화갑옷.png')
}

weapons_explanations = {
    common_sword : font.render('평범한 검.', True, black),
    lightning_sword : font.render('번개의 힘이 깃든 검.', True, black),
    common_shield : font.render('평범한 방패.', True, black) ,
    common_healthy : font.render('평범한 갑옷.', True, black) ,
    grass_healthy : font.render('풀의 가호를 받은 갑옷.', True, black),
    iron_shield : font.render('철을 둘러 더욱 단단해진 방패.', True, black),
    dagger : font.render('평범한 단도.', True, black),
    lion_head_shield : font.render('사자의 머리를 단 방패.', True, black),
    copper_healthy : font.render('구리로 만든 갑옷.', True, black),
    obsidian_sword : font.render('흑요석으로 만든 검.', True, black),
    wolf_head_shield : font.render('우두머리 늑대의 머리를 단 방패.', True, black),
    platinum_healthy : font.render('백금으로 만든 갑옷.', True, black),
    shadow_sword : font.render('그림자가 깃든 검.', True, black),
    undead_shield : font.render('해골의 머리를 전리품으로 단 방패.', True, black),
    emerald_healthy : font.render('에메랄드로 만든 갑옷.', True, black),
    toxic_dagger : font.render('독이 묻어 치명적인 단검.', True, black),
    night_shield : font.render('밤의 기운이 가득 담긴 방패.', True, black),
    garnet_healthy : font.render('붉은 석류석으로 만든 갑옷.', True, black),
    fire_sword : font.render('검신이 불로 뒤덮인 검.', True, black),
    afternoon_shield : font.render('낮의 기운이 가득 담긴 방패.', True, black),
    sapphire_healthy : font.render('연한 보라색 사파이어로 만든 갑옷.', True, black),
    star_sword : font.render('검신에 별의 기운이 깃든 검.', True, black),
    dawn_shield : font.render('새벽의 기운이 가득 담긴 방패.', True, black),
    moonstone_healthy : font.render('문스톤으로 만든 갑옷.', True, black),
    optimization_sword : font.render('직접 단조에 참여하여 만든 검.', True, black),
    optimization_shield : font.render('직접 단조에 참여하여 만든 방패.', True, black),
    optimization_healthy : font.render('직접 단조에 참여하여 만든 갑옷.', True, black)
}

abilitys = {
    common_sword : font.render('공격력 : 1', True, black),
    common_healthy : font.render('체력 : 15', True, black),
    common_shield : font.render('방어력 : 1', True, black),
    lightning_sword : font.render('공격력 : 2', True, black),
    grass_healthy : font.render('체력 : 20', True, black),
    iron_shield : font.render('방어력 : 2', True, black),
    dagger : font.render('공격력 : 2', True, black),
    lion_head_shield : font.render('방어력 : 2', True, black),
    copper_healthy : font.render('체력 : 20', True, black),
    obsidian_sword : font.render('공격력 : 2', True, black),
    platinum_healthy : font.render('체력 : 20', True, black),
    wolf_head_shield : font.render('방어력 : 2', True, black),
    shadow_sword : font.render('공격력 : 2', True, black),
    undead_shield : font.render('방어력 : 2', True, black),
    emerald_healthy : font.render('체력 : 20', True, black),
    toxic_dagger : font.render('공격력 : 3', True, black),
    night_shield : font.render('방어력 : 3', True ,black),
    garnet_healthy : font.render('체력 : 30', True, black),
    fire_sword : font.render('공격력 : 3', True, black),
    afternoon_shield : font.render('방어력 : 3', True, black),
    sapphire_healthy : font.render('체력 : 30', True, black),
    star_sword : font.render('공격력 : 3', True, black),
    dawn_shield : font.render('방어력 : 3', True, black),
    moonstone_healthy : font.render('체력 : 30', True, black),
    optimization_sword : font.render('공격력 : 5', True, black),
    optimization_shield : font.render('방어력 : 5', True, black),
    optimization_healthy : font.render('체력 : 40', True, black)
}

my_attack = 1
my_defence = 1

my_skills = {}

conversation_check = {}

item_list = {}

gold = 0


def conversation(character, number):
    global gameui
    global gameui_x_pos
    global gameui_y_pos
    global dialog
    global item_list
    global my_skills
    white = (255,255,255)
    black = (0,0,0)

    
    dialog_size = dialog.get_rect().size
    dialog_width = dialog_size[0]
    dialog_height = dialog_size[1]
    dialog_x_pos = 70
    dialog_y_pos = 520

    skip = pygame.image.load('.\\resource\\스킵버튼.png')
    skip_size = skip.get_rect().size
    skip_width = skip_size[0]
    skip_height = skip_size[1]
    skip_x_pos = 600
    skip_y_pos = 70


    next_sound = pygame.mixer.Sound('.\\resource\\sound\\대화창다음으로.wav')

    if character == 'tutorial' and number == 1:
        names = ['이 선', '이 선', '이 선', '이 선', '이 선', '이 선', '이 선', '이 선', '이 선', '이 선']
        scripts = ['내 이름은 이 선', '평범한 중학생이다.', '나는 어제 밤 마녀의 여행을 보았다', '그걸 본 이상 참을 수 없는 분노를 느꼈는데', '왜냐하면 마녀의 여행 주인공. 나의 사랑 일레이나짱이', '다른 녀석과 꽁냥거리는 것을 보았기 때문이다', '그래서 나는 일레이나짱을 찾으러 가기로 했다.', '그녀는 2차원 세계에 있을 것이다.', '듣자하니 먼 어느 곳에 세 지민중 한명이 차원에 대하여 연구한다고 들었다', '그라면 나를 2차원 세계로 보내주지 않을까?']
        character_image = pygame.image.load('.\\resource\\텅비어있음.png')
        background = pygame.image.load('.\\resource\\방.png')
        character_x_pos = 400
        character_y_pos = 70

    if character == 'jammin' and number == 1:
        names = ['', '잼민이', '이 선', '잼민이', '이 선']
        scripts = ['당신은 잼민이와의 싸움에서 이겼습니다', '님 좀 쎄신듯 쿠쿠루삥뽕', '하, 네가 너무 약한거다', '어쩔티비 저쩔티비 우짤래미 저짤래미', '어쩔 콩순이 주방놀이 세트']
        character_image = pygame.image.load('.\\resource\\enemy\\샌즈.png')
        background = pygame.image.load('.\\resource\\장소1.png')
        character_x_pos = 400
        character_y_pos = 70

    if character == 'sign' and number == 1:
        names = ['표지판', '표지판', '표지판']
        scripts = ['↑ 성당', '→ 대장장이의 집', '← 주의! 잼민이와 과몰입한 씹덕의 집, 숲']
        character_image = pygame.image.load('.\\resource\\텅비어있음.png')
        background = pygame.image.load('.\\resource\\장소3.png')
        character_x_pos = 400
        character_y_pos = 70

    if character == 'teemo' and number == 1:
        names = ['이 선', '요정', '이 선', '요정', '이 선', '요정', '이 선', '요정', '이 선', '요정']
        scripts = ['너는 누구냐', '나는 티모요정이다', '그게 뭔데 씹덕아', '니가 할 소리냐 씹덕아', '어떻게 알았지? 네녀석 스토커냐?', '난 모든걸 보고있지', '헉! 제자로 삼아주십시오!', '그럼 뼈 5개와 나뭇가지 10개를 가져와라']
        character_image = pygame.image.load('.\\resource\\요정.png')
        background = pygame.image.load('.\\resource\\장소2(나무).png')
        character_x_pos = 400
        character_y_pos = 70
    
    if character == 'teemo' and number >= 2:
        if '실명다트' not in my_skills:
            if item_list['나뭇가지'][0] >= 10 and item_list['뼈'][0] >= 5:
                names = ['요정', '이 선', '요정', '이 선', '요정', '']
                scripts = ['가지고 왔나?', '드...드리겠습니다', '좋아, 기꺼이 비천한 너의 스승이 되어주겠다.', '아리가또! 센세!', '내가 알려주는 이 기술을 잊지말아라', '당신은 무언가를 전수받았습니다']
                item_list['나뭇가지'][0] -= 10
                item_list['뼈'][0] -= 5
                my_skills['실명다트'] = [('attack', 'concentration', 'concentration'), 1]
            else:
                names = ['요정', '이 선', '요정', '이 선']
                scripts = ['가지고 왔나?', '아직 안가져 왔는데요', '죽고 싶나?', '히히 ㅈㅅ']
        else:
            names = ['요정', '이 선']
            scripts = ['더 볼일이 있나?', '아뇨...아무것도.']
        character_image = pygame.image.load('.\\resource\\요정.png')
        background = pygame.image.load('.\\resource\\장소2(나무).png')
        character_x_pos = 400
        character_y_pos = 70
    
    if character == 'cockroach' and number == 1:
        names = ['이 선', '바퀴벌레', '이 선', '이 선', '바퀴벌레']
        scripts = ['뭐야 넌, 바퀴벌레냐?', '...', '뭐? 오마에, 감히 와타시에게 [도전] 하다니...', '그 선택을 후회하게 해주마!', '...?']
        character_image = pygame.image.load('.\\resource\\enemy\\바퀴.png')
        background = pygame.image.load('.\\resource\\장소3.png')
        character_x_pos = 400
        character_y_pos = 70
    
    if character == 'youknow' and number == 1:
        names = ['이 선', '(아마도) 수녀', '이 선', '(아마도) 수녀', '이 선', '(아마도) 수녀', '(아마도) 수녀', '', '']
        scripts = ['오오...', '무슨 일로 오셨나요?', '저의 여친이자 모든 것. 일레이나짱을 찾고있습니다', '아...죄송하지만 그런 분은 여기 오시지 않았어요', '그렇군요', '꼭 찾으시길 바랍니다.', '신의 가호가 함께 하시길.', '그 말이 끝남과 동시에 왠지 모를 기운이 속에서 끓어넘친다.', '정말로 신의 가호가 향한 것일까?']
        my_skills['신의 가호'] = [('concentration', 'concentration', 'concentration'), 1]
        character_image = pygame.image.load('.\\resource\\요이미야.png')
        background = pygame.image.load('.\\resource\\성당내부.png')
        character_x_pos = 400
        character_y_pos = 70

    if character == 'youknow' and number >= 2:
        names = ['수녀', '이 선']
        scripts = ['더 볼일이 있으신가요?', '아뇨...아무것도.']
        character_image = pygame.image.load('.\\resource\\요이미야.png')
        background = pygame.image.load('.\\resource\\성당내부.png')
        character_x_pos = 400
        character_y_pos = 70
        

    if character == 'winline' and number == 1:
        names = ['이 선', '대장장이', '이 선', '대장장이', '대장장이']
        scripts = ['계십니까?', '누가 잘 자는 나를 깨워?', '여기 영업하나요?', '하, 대장장이로써의 명성은 여전하군.', '내 잠을 깨운 죄로 비싸게 사가셔야겠어.']
        character_image = pygame.image.load('.\\resource\\승선.png')
        background = pygame.image.load('.\\resource\\장소1.png')
        character_x_pos = 300
        character_y_pos = 70

    if character == 'junhyeok' and number == 1:
        names = ['곧혁', '이 선', '곧혁', '이 선', '곧혁', '이 선']
        scripts = ['깨달음을 얻거나, 목숨을 잃거나. 둘 중 하나지.', '뭐라고요?', '행동해서 깨달음을 얻는 법. 움직이지 않으면, 죽는다.', '네? 뭐라고요?', '움직이지 않으시겠다?', '어...? 잠시만요?']
        character_image = pygame.image.load('.\\resource\\enemy\\일라오이.png')
        background = pygame.image.load('.\\resource\\장소6.png')
        character_x_pos = 400
        character_y_pos = 70
    
    if character == 'junhyeok' and number == 2:
        names = ['곧혁', '곧혁', '이 선', '']
        scripts = ['가망이 아주 없는 녀석은 아니였군.', '다시, 전진해라.', '갑자기 싸움을 걸고서는...', '당신은 곧혁에게 무언가를 받았습니다']
        character_image = pygame.image.load('.\\resource\\enemy\\일라오이.png')
        background = pygame.image.load('.\\resource\\장소6.png')
        character_x_pos = 400
        character_y_pos = 70

    if character == 'junji' and number == 1:
        names = ['?', '이 선', '상인', '김준희', '이 선', '김준희', '김준희', '이 선']
        scripts = ['여~', '누구세요?', '물건 팔러 돌아다니는 상인이올시다.', '보부상 김준희라고 불러주시게', '아...네', '여기 좋은 물건 많이 들어왔는데 한 번 볼랑가?', '타국의 대장장이 준스케가 만든 무기 설계도들과 내 단골 음식집 사장 준지의 요리도 있다네.', '\'누군지 한 번도 들어보지는 못했지만 일단 사보자.\'']
        character_image = pygame.image.load('.\\resource\\준지.png')
        background = pygame.image.load('.\\resource\\장소8.png')
        character_x_pos = 540
        character_y_pos = 200
    
    if character == 'hyunwoo' and number == 1:
        names = ['윤경영', '이 선', '윤경영', '이 선', '윤경영', '이 선', '윤경영', '이 선', '윤경영']
        scripts = ['어서 오십쇼', '여긴 무슨 사무실인가요?', '이 곳은 저의 가르침을 받을 수 있는 곳이죠.', '무슨 가르침인데요?', '공중부양이나 무궁화발차기, 축지법 따위의 것들을 말합니다.', '우와! 저 정말 그런거 하고싶었어요!', '하하, 원한다면 가르쳐드릴 수 있습니다. 다만...', '다만?', '재료가 좀 필요합니다.']
        character_image = pygame.image.load('.\\resource\\텅비어있음.png')
        background = pygame.image.load('.\\resource\\현우.png')
        character_x_pos = 0
        character_y_pos = 0
        play = False
    
    if character == '독백' and number == 1:
        names = ['이 선', '이 선', '이 선', '이 선', '이 선', '이 선', '이 선']
        scripts = ['마침내 당도했다.', '이 곳이 세 지민이 살고 있을거랬다.', '탑 뷰를 보기 위해 꼭대기에 살고 있다는 걸 아는게 얼마나 다행인지...', '좋아, 내 앞을 막을 자들이 넘쳐나겠지.', '두렵다...두렵지만.', '전주 이씨의 명예를 걸고, 싸워나갈 것이다.', '나의 일레이나짱을 되찾을 것이다.']
        character_image = pygame.image.load('.\\resource\\텅비어있음.png')
        background = pygame.image.load('.\\resource\\장소8.png')
        character_x_pos = 0
        character_y_pos = 0

    if character == '독백' and number == 2:
        names = ['이 선', '이 선', '이 선', '이 선', '구름', '성현', '구름, 성현']
        scripts = ['여기가...1층?', '분명 천장이 있을텐데...', '어째서 하늘이 있는거지?', '천장이 보이지 않아.', '저거 봐, 성현! 또 멍청한 도전자가 왔어!', '탑에 도전할 생각이냐? 그렇다면...', '우리가 상대해주지.']
        character_image = pygame.image.load('.\\resource\\텅비어있음.png')
        background = pygame.image.load('.\\resource\\탑1층.png')
        character_x_pos = 400
        character_y_pos = 70
    
    if character == '독백' and number == 3:
        names = ['이 선', '이 선', '이 선']
        scripts = ['생각보다 쉬운 상대였다.', '이정도라면 생각보다 빠르게 올라갈 수 있을지도 모르겠군.', '어서 올라가자.']
        character_image = pygame.image.load('.\\resource\\텅비어있음.png')
        background = pygame.image.load('.\\resource\\탑1층.png')
        character_x_pos = 0
        character_y_pos = 0

    if character == 'minyoung' and number == 1:
        names = ['이 선', '이 선', '이 선', '???', '???', '', '이 선']
        scripts = ['여기가...탑 2층인가?', '어쩐지...익숙한 느낌이 드는데...', '여긴 혹시...?', '피냄새가 나는데...', '고립시켜서 먹어주지.', '기분나쁜 웃음소리가 들린다.', '크윽, 전투준비!']
        character_image = pygame.image.load('.\\resource\\텅비어있음.png')
        background = pygame.image.load('.\\resource\\탑2층.jpg')
        character_x_pos = 400
        character_y_pos = 70
        play = False
        play2 = False
        play3 = False
        play4 = False
    
    if character == 'blackcow' and number == 1:
        names = ['', '', '이 선', '흑우', '']
        scripts = ['당신은 마침내 탑 꼭대기에 도착했습니다.', '3가지 문 중 가장 검은 문을 선택한 당신은 벛꽃이 흩날리는 방에 들어섭니다', '사쿠라네?', '사쿠라야?', '당신의 앞에 등장한 마지막 관문은 검은 소였습니다.']
        character_image = pygame.image.load('.\\resource\\enemy\\장지.png')
        background = pygame.image.load('.\\resource\\탑꼭대기1.png')
        character_x_pos = 320
        character_y_pos = 70
    
    if character == 'ending' and number == 1:
        names = ['이 선', '장지', '이 선', '장지', '이 선', '장지', '이 선', '']
        scripts = ['자, 이제 나를 일레이나짱에게 보내줘!', '뭐? 그건 무슨소리야?', '마녀의 여행을 몰라? 하 정말.', '아니 그런거 말고 우리 전기톱맨을 보는건 어떤가?', '뭐? 전기톱맨?', '이 애니, 작화도 좋고 스토리도 멋지다고?', '오 그래? 그거 좋은데!', '그렇게 이 선은 전기톱맨에 빠져 일레이나짱을 잊고 행복하게 살았답니다.']
        character_image = pygame.image.load('.\\resource\\enemy\\장지.png')
        background = pygame.image.load('.\\resource\\탑꼭대기1.png')
        character_x_pos = 320
        character_y_pos = 70

    if character == 'ojimin' and number == 1:
        names = ['', '', '이 선', '오지', '', '']
        scripts =['당신은 마침내 탑 꼭대기에 도착했습니다.', '3가지 문 중 하늘색 문을 선택한 당신은 푸른 하늘이 펼쳐진 3차원 공간에 들어섭니다.', '와타시가 킷타!', '자, 덤벼', '당신의 앞에 등장한 마지막 관문은', '연어 머리와 흡혈귀 몸통을 가지고 시간의 방망이를 휘두르는 오지입니다.']
        character_image = pygame.image.load('.\\resource\\enemy\\오지.png')
        background = pygame.image.load('.\\resource\\탑꼭대기2.png')
        character_x_pos = 320
        character_y_pos = 70

    if character == 'ending' and number == 2:
        names = ['이 선', '오지', '이 선', '오지', '']
        scripts = ['자, 이제 나를 일레이나짱에게 보내줘!', '뭐, 뭐? 누구라고?', '일레이나짱 말이다! 내 사랑하는 일레이나짱에게 나를 보내줘!', '내가 이런 씹덕 따위에게 지다니 으윽, 수치스럽다!', '오지는 탑 창밖으로 몸을 던졌고, 이 선은 새로운 마왕 중 하나가 되어 행복하게 살았답니다.']
        character_image = pygame.image.load(".\\resource\\enemy\\오지.png")
        background = pygame.image.load('.\\resource\\탑꼭대기2.png')
        character_x_pos = 320
        character_y_pos = 70
        playsound3 = False

    script = font.render(scripts[0], True, black)
    nowscriptindex = 0
    scriptindexall = len(scripts)

    name = font.render(names[0], True, black)
    name_size = name.get_rect().size
    name_width = name_size[0]
    name_height = name_size[1]
    nownameindex = 0
    nameindexall = len(names)

    playsound = -1
    playsound2 = -1

    nowaudio = pygame.mixer.Sound('.\\resource\\sound\\소리없음.wav')

    running = True

    while running:
        dt = clock.tick(60)

        if character == 'junhyeok' and number == 1:
            if nowscriptindex == 0:
                if playsound == -1:
                    playsound = 1
            elif nowscriptindex == 1:
                nowaudio.stop()
            elif nowscriptindex == 2:
                if playsound == 0:
                    playsound = 2
            elif nowscriptindex == 3:
                nowaudio.stop()
            elif nowscriptindex == 4:
                if playsound == -2:
                    playsound = 3
            elif nowscriptindex == 5:
                nowaudio.stop()

        if character == '독백' and number == 2:
            if nowscriptindex == 4:
                character_image = pygame.image.load('.\\resource\\enemy\\성현.png')
        
        if character == 'minyoung':
            if number == 1:
                if play == False and nowscriptindex == 2:
                    nowaudio = pygame.mixer.Sound('.\\resource\\sound\\협곡진입.wav').play()
                    play = True
                elif play2 == False and nowscriptindex == 3:
                    nowaudio.stop()
                    nowaudio = pygame.mixer.Sound('.\\resource\\sound\\카직스대사1.wav').play()
                    play2 = True
                elif play3 == False and nowscriptindex == 4:
                    nowaudio.stop()
                    nowaudio = pygame.mixer.Sound('.\\resource\\sound\\카직스대사2.wav').play()
                    play3 = True
                elif play4 == False and nowscriptindex == 5:
                    nowaudio.stop()
                    nowaudio = pygame.mixer.Sound('.\\resource\\sound\\카직스대사3.wav').play()
                    play4 = True
        elif character == 'ending':
            if number == 2:
                if playsound3 == False and nowscriptindex == 5:
                    nowaudio.stop()
                    nowaudio = pygame.mixer.Sound('.\\resource\\sound\\오지비명.wav').play()
                    playsound3 = True 

                
        
                
        if playsound == 1:
            nowaudio = pygame.mixer.Sound('.\\resource\\sound\\일라오이대사첫번째.wav')
            nowaudio.play()
            playsound = 0
        elif playsound == 2:
            nowaudio = pygame.mixer.Sound('.\\resource\\sound\\일라오이대사두번째.wav')
            nowaudio.play()
            playsound = -2
        elif playsound == 3:
            nowaudio = pygame.mixer.Sound('.\\resource\\sound\\일라오이대사세번째.wav')
            nowaudio.play()
            playsound = -5


        if character == 'junhyeok' and number == 2:
            if nowscriptindex == 0:
                if playsound2 == -1:
                    playsound2 = 1
            elif nowscriptindex == 1:
                if playsound2 == 0:
                    playsound2 = 2
            elif nowscriptindex == 2:
                nowaudio.stop()

        if character == 'hyunwoo' and number == 1:
            if play == False:
                nowaudio = pygame.mixer.Sound('.\\resource\\sound\\종소리.wav').play()
                play = True

        if playsound2 == 1:
            nowaudio = pygame.mixer.Sound('.\\resource\\sound\\일라오이승리시대사첫번째.wav')
            nowaudio.play()
            playsound2 = 0
        elif playsound2 == 2:
            nowaudio = pygame.mixer.Sound('.\\resource\\sound\\일라오이승리시두번째대사.wav')
            nowaudio.play()
            playsound2 = -2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skip_x_pos < pygame.mouse.get_pos()[0] < skip_x_pos + skip_width and skip_y_pos < pygame.mouse.get_pos()[1] < skip_y_pos + skip_height:
                    next_sound.play()
                    if character == 'winline' and number == 1:
                        pygame.mixer.Sound('.\\resource\\sound\\대장간소리.wav').play()
                        smithy()
                    elif character == 'junji' and number == 1:
                        shop()
                    elif character == 'hyunwoo' and number == 1:
                        synthesis()
                    return
                else:
                    nowscriptindex += 1
                    if character == 'junhyeok' and number == 2:
                        if nowscriptindex == 1:
                            nowaudio.stop()
                    nownameindex += 1
                    if scriptindexall == nowscriptindex:
                        if character == 'winline' and number == 1:
                            pygame.mixer.Sound('.\\resource\\sound\\대장간소리.wav').play()
                            smithy()
                        elif character == 'junji' and number == 1:
                            shop()
                        elif character == 'hyunwoo' and number == 1:
                            synthesis()
                        return
                    if nameindexall == nownameindex:
                        return
                    script = font.render(scripts[nowscriptindex], True, black)
                    name = font.render(names[nownameindex], True, black)
                    name_size = name.get_rect().size
                    name_width = name_size[0]
                    name_height = name_size[1]
                    next_sound.play()
                

                
        
        screen.fill(white)
        screen.blit(background, (70, 70))
        screen.blit(gameui, (gameui_x_pos, gameui_y_pos))
        screen.blit(dialog, (dialog_x_pos, dialog_y_pos))
        screen.blit(character_image, (character_x_pos, character_y_pos))
        screen.blit(script, (85, 580))
        screen.blit(name, (160 - name_width / 2, 533))
        screen.blit(skip, (skip_x_pos, skip_y_pos))
        pygame.display.update()

def smithy():
    global screen_width
    global screen_height
    global items
    global item_list
    global white
    global black
    global red
    global green
    global blue
    global weapons
    global weapons_rating
    global abilitys

    background = pygame.image.load('.\\resource\\대장간내부.png')
    background_x_pos = 0
    background_y_pos = 0

    smithy_menu = pygame.image.load('.\\resource\\shop.png')
    smithy_menu_size = smithy_menu.get_rect().size
    smithy_menu_width = smithy_menu_size[0]
    smithy_menu_height = smithy_menu_size[1]
    smithy_menu_x_pos = screen_width / 2 - smithy_menu_width / 2
    smithy_menu_y_pos = screen_height / 2 - smithy_menu_height / 2

    close_button = pygame.image.load('.\\resource\\X버튼.png')
    close_button_size = close_button.get_rect().size
    close_button_width = close_button_size[0]
    close_button_height = close_button_size[1]
    close_button_x_pos = smithy_menu_x_pos + smithy_menu_width - close_button_width
    close_button_y_pos = smithy_menu_y_pos

    upgrade_button = pygame.image.load('.\\resource\\강화.png')
    upgrade_button_size = upgrade_button.get_rect().size
    upgrade_button_width = upgrade_button_size[0]
    upgrade_button_height = upgrade_button_size[1]
    upgrade_button_x_pos = 400
    upgrade_button_y_pos = 540

    attack_button = pygame.image.load('.\\resource\\공격무기업그레이드.png')
    attack_button_size = attack_button.get_rect().size
    attack_button_width = attack_button_size[0]
    attack_button_height = attack_button_size[1]
    attack_button_x_pos = 60 + smithy_menu_x_pos
    attack_button_y_pos = 168 + smithy_menu_y_pos

    gard_button = pygame.image.load('.\\resource\\방어무기업그레이드.png')
    gard_button_size = gard_button.get_rect().size
    gard_button_width = gard_button_size[0]
    gard_button_height = gard_button_size[1]
    gard_button_x_pos = 60 + smithy_menu_x_pos
    gard_button_y_pos = 291 + smithy_menu_y_pos

    healthy_button = pygame.image.load('.\\resource\\갑옷업그레이드.png')
    healthy_button_size = healthy_button.get_rect().size
    healthy_button_width = healthy_button_size[0]
    healthy_button_height = healthy_button_size[1]
    healthy_button_x_pos = 60 + smithy_menu_x_pos
    healthy_button_y_pos = 415 + smithy_menu_y_pos

    sword_size = weapons['sword'].get_rect().size
    sword_width = sword_size[0]
    sword_height = sword_size[1]
    sword_x_pos = attack_button_x_pos + 12
    sword_y_pos = attack_button_y_pos + 22

    healthy_size = weapons['healthy'].get_rect().size
    healthy_width = healthy_size[0]
    healthy_height = healthy_size[1]
    healthy_x_pos = healthy_button_x_pos + 12
    healthy_y_pos = healthy_button_y_pos + 22

    shield_size = weapons['shield'].get_rect().size
    shield_width = shield_size[0]
    shield_height = shield_size[1]
    shield_x_pos = gard_button_x_pos + 12
    shield_y_pos = gard_button_y_pos + 22

    now_upgrade = list(weapons.keys())[0]

    big_image = big_images[weapons['sword']]
    big_image_x_pos = smithy_menu_x_pos + 350
    big_image_y_pos = smithy_menu_y_pos + 168

    weapons_explanation = weapons_explanations[weapons['sword']]
    weapons_rating_text = weapons_rating[weapons['sword']]
    ability = abilitys[weapons['sword']]

    running = True

    while running:
        dt = clock.tick(60)

        #이벤트 처리
        for event in pygame.event.get(): #이벤트 수집
            if event.type == pygame.MOUSEBUTTONDOWN: #창이 닫히는 이벤트가 발생하였는가?
                if close_button_x_pos < pygame.mouse.get_pos()[0] < close_button_x_pos + close_button_width and close_button_y_pos < pygame.mouse.get_pos()[1] < close_button_y_pos + close_button_height:
                    pygame.mixer.Sound('.\\resource\\sound\\대화창다음으로.wav').play()
                    running = False #게임 실행 False
                elif attack_button_x_pos < pygame.mouse.get_pos()[0] < attack_button_x_pos + attack_button_width and attack_button_y_pos < pygame.mouse.get_pos()[1] < attack_button_y_pos + attack_button_height:
                    now_upgrade = list(weapons.keys())[0]
                    if weapons['sword'] == common_sword:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[common_sword]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == lightning_sword:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[lightning_sword]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == dagger:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[dagger]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == obsidian_sword:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[obsidian_sword]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == shadow_sword:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[shadow_sword]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == toxic_dagger:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[toxic_dagger]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == fire_sword:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[fire_sword]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == star_sword:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[star_sword]
                        ability = abilitys[weapons['sword']]
                    elif weapons['sword'] == optimization_sword:
                        big_image = big_images[weapons['sword']]
                        weapons_explanation = weapons_explanations[weapons['sword']]
                        weapons_rating_text = weapons_rating[optimization_sword]
                        ability = abilitys[weapons['sword']]
                elif gard_button_x_pos < pygame.mouse.get_pos()[0] < gard_button_x_pos + gard_button_width and gard_button_y_pos < pygame.mouse.get_pos()[1] < gard_button_y_pos + gard_button_height:
                    now_upgrade = list(weapons.keys())[1]
                    if weapons['shield'] == common_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[common_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == iron_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[iron_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == lion_head_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[lion_head_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == wolf_head_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[wolf_head_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == undead_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[undead_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == night_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[night_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == afternoon_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[afternoon_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == dawn_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[dawn_shield]
                        ability = abilitys[weapons['shield']]
                    elif weapons['shield'] == optimization_shield:
                        big_image = big_images[weapons['shield']]
                        weapons_explanation = weapons_explanations[weapons['shield']]
                        weapons_rating_text = weapons_rating[optimization_shield]
                        ability = abilitys[weapons['shield']]
                elif healthy_button_x_pos < pygame.mouse.get_pos()[0] < healthy_button_x_pos + healthy_button_width and healthy_button_y_pos < pygame.mouse.get_pos(0)[1] < healthy_button_y_pos + healthy_button_height:
                    now_upgrade = list(weapons.keys())[2]
                    if weapons['healthy'] == common_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[common_healthy]
                        ability = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == grass_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[grass_healthy]
                        ability = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == copper_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[copper_healthy]
                        ability = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == platinum_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[platinum_healthy]
                        ability = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == emerald_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[emerald_healthy]
                        ability = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == garnet_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[garnet_healthy]
                        ability = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == sapphire_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[sapphire_healthy]
                        ability = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == moonstone_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[moonstone_healthy]
                        abilitys = abilitys[weapons['healthy']]
                    elif weapons['healthy'] == optimization_healthy:
                        big_image = big_images[weapons['healthy']]
                        weapons_explanation = weapons_explanations[weapons['healthy']]
                        weapons_rating_text = weapons_rating[optimization_healthy]
                        abilitys = abilitys[weapons['healthy']]
                if upgrade_button_x_pos < pygame.mouse.get_pos()[0] < upgrade_button_x_pos + upgrade_button_width and upgrade_button_y_pos < pygame.mouse.get_pos()[1] < upgrade_button_y_pos + upgrade_button_height:
                    if item_list['단조 설계도'][0] > 0:
                        if now_upgrade == list(weapons.keys())[0]:
                            while True:
                                a = weapons['sword']
                                weapons['sword'] = random.choice(swords)
                                if a != weapons['sword']:
                                    break
                            pygame.mixer.Sound('.\\resource\\sound\\대장간소리.wav').play()
                            if weapons['sword'] == common_sword:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[weapons['sword']]
                                weapons_rating_text = weapons_rating[common_sword]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == lightning_sword:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[weapons['sword']]
                                weapons_rating_text = weapons_rating[lightning_sword]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == dagger:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[weapons['sword']]
                                weapons_rating_text = weapons_rating[dagger]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == obsidian_sword:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[weapons['sword']]
                                weapons_rating_text = weapons_rating[obsidian_sword]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == shadow_sword:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[weapons['sword']]
                                weapons_rating_text = weapons_rating[shadow_sword]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == toxic_dagger:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[weapons['sword']]
                                weapons_rating_text = weapons_rating[toxic_dagger]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == fire_sword:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[fire_sword]
                                weapons_rating_text = weapons_rating[fire_sword]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == star_sword:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[star_sword]
                                weapons_rating_text = weapons_rating[star_sword]
                                ability = abilitys[weapons['sword']]
                            elif weapons['sword'] == optimization_sword:
                                big_image = big_images[weapons['sword']]
                                weapons_explanation = weapons_explanations[optimization_sword]
                                weapons_rating_text = weapons_rating[optimization_sword]
                                ability = abilitys[weapons['sword']]
                        if now_upgrade == list(weapons.keys())[1]:
                            while True:
                                a = weapons['shield']
                                weapons['shield'] = random.choice(shields)
                                if a != weapons['shield']:
                                    break
                            pygame.mixer.Sound('.\\resource\\sound\\대장간소리.wav').play()
                            if weapons['shield'] == common_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[common_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == iron_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[iron_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == lion_head_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[lion_head_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == wolf_head_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[wolf_head_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == undead_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[undead_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == night_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[night_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == afternoon_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[afternoon_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == dawn_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[dawn_shield]
                                ability = abilitys[weapons['shield']]
                            elif weapons['shield'] == optimization_shield:
                                big_image = big_images[weapons['shield']]
                                weapons_explanation = weapons_explanations[weapons['shield']]
                                weapons_rating_text = weapons_rating[optimization_shield]
                                ability = abilitys[weapons['shield']]
                        if now_upgrade == list(weapons.keys())[2]:
                            while True:
                                a = weapons['healthy']
                                weapons['healthy'] = random.choice(healthys)
                                if a != weapons['healthy']:
                                    break
                            pygame.mixer.Sound('.\\resource\\sound\\대장간소리.wav').play()
                            if weapons['healthy'] == common_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[common_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == grass_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[grass_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == copper_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[copper_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == platinum_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[platinum_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == emerald_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[emerald_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == garnet_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[garnet_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == sapphire_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[sapphire_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == moonstone_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[moonstone_healthy]
                                ability = abilitys[weapons['healthy']]
                            elif weapons['healthy'] == optimization_healthy:
                                big_image = big_images[weapons['healthy']]
                                weapons_explanation = weapons_explanations[weapons['healthy']]
                                weapons_rating_text = weapons_rating[optimization_healthy]
                                ability = abilitys[weapons['healthy']]
                    
                            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print(pygame.mouse.get_pos())

        weapons_explanation_size = weapons_explanation.get_rect().size
        weapons_explanation_width = weapons_explanation_size[0]
        weapons_explanation_height = weapons_explanation_size[1]
        weapons_explanation_x_pos = 405 + (200 / 2) - weapons_explanation_width / 2
        weapons_explanation_y_pos = 430

        weapons_rating_text_size = weapons_rating_text.get_rect().size
        weapons_rating_text_width = weapons_rating_text_size[0]
        weapons_rating_text_height = weapons_rating_text_size[1]
        weapons_rating_text_x_pos = 405 + (200 / 2) - weapons_rating_text_width / 2
        weapons_rating_text_y_pos = 450
    
        ability_size = ability.get_rect().size
        ability_width = ability_size[0]
        ability_height = ability_size[1]
        ability_x_pos = 405 + (200 / 2) - ability_width / 2
        ability_y_pos = 470
        
    
        
        screen.blit(background, (background_x_pos, background_y_pos))
        screen.blit(smithy_menu, (smithy_menu_x_pos, smithy_menu_y_pos))
        screen.blit(close_button, (close_button_x_pos, close_button_y_pos))
        screen.blit(upgrade_button, (upgrade_button_x_pos, upgrade_button_y_pos))
        screen.blit(attack_button, (attack_button_x_pos, attack_button_y_pos))
        screen.blit(gard_button, (gard_button_x_pos, gard_button_y_pos))
        screen.blit(healthy_button, (healthy_button_x_pos , healthy_button_y_pos))
        screen.blit(weapons['sword'], (sword_x_pos, sword_y_pos))
        screen.blit(weapons['shield'], (shield_x_pos, shield_y_pos))
        screen.blit(weapons['healthy'], (healthy_x_pos, healthy_y_pos))
        screen.blit(big_image, (big_image_x_pos, big_image_y_pos))
        screen.blit(weapons_explanation, (weapons_explanation_x_pos, weapons_explanation_y_pos))
        screen.blit(weapons_rating_text, (weapons_rating_text_x_pos, weapons_rating_text_y_pos))
        screen.blit(ability, (ability_x_pos, ability_y_pos))
        
        pygame.display.update()

    
    return

def battle(character):
    global items
    global gameui
    global gameui_x_pos
    global gameui_y_pos
    global dialog
    global my_skills
    global weapons
    global weapons_rating
    global my_defence
    global my_attack
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    boss_hp_frame = pygame.image.load('.\\resource\\hp바.png')
    boss_hp_frame_x_pos = 250
    boss_hp_frame_y_pos = 80
    boss_hp_frame_width = boss_hp_frame.get_rect().size[0]
    boss_hp_coler = (0, 202, 0)

    boss_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
    boss_Ang1_x_pos = 75
    boss_Ang1_y_pos = 75
    boss_Ang1 = 0
    boss_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
    boss_Ang2_x_pos = 120
    boss_Ang2_y_pos = 75
    boss_Ang2 = 0
    boss_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')
    boss_Ang3_x_pos = 165
    boss_Ang3_y_pos = 75
    boss_Ang3 = 0

    my_hp_frame = pygame.image.load('.\\resource\\hp바.png')
    my_hp_frame_x_pos = 250
    my_hp_frame_y_pos = 670
    my_hp_frame_width = my_hp_frame.get_rect().size[0]
    my_hp_coler = (0, 202, 0)
    my_max_hp = 15
    now_my_hp = 15
    my_attack = 1
    my_defence = 1

    if weapons['healthy'] == grass_healthy or weapons['healthy'] == copper_healthy or weapons['healthy'] == platinum_healthy or weapons['healthy'] == emerald_healthy:
        my_max_hp = 20
        now_my_hp = 20
    elif weapons['healthy'] == garnet_healthy or weapons['healthy'] == sapphire_healthy or weapons['healthy'] == moonstone_healthy:
        my_max_hp = 30
        now_my_hp = 30
    elif weapons['healthy'] == optimization_healthy:
        my_max_hp = 40
        now_my_hp = 40
    
    if weapons['sword'] == lightning_sword or weapons['sword'] == dagger or weapons['sword'] == obsidian_sword or weapons['sword'] == shadow_sword:
        my_attack = 2
    elif weapons['sword'] == toxic_dagger or weapons['sword'] == fire_sword or weapons['sword'] == star_sword:
        my_attack = 3
    elif weapons['sword'] == optimization_sword:
        my_attack = 5
    
    if weapons['shield'] == iron_shield or weapons['shield'] == lion_head_shield or weapons['shield'] == wolf_head_shield or weapons['shield'] == undead_shield:
        my_defence = 2
    elif weapons['shield'] == night_shield or weapons['shield'] == afternoon_shield or weapons['shield'] == dawn_shield:
        my_defence = 3
    elif weapons['shield'] == optimization_shield:
        my_defence = 5

    my_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
    my_Ang1_x_pos = 75
    my_Ang1_y_pos = 650
    my_Ang1 = 0
    my_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
    my_Ang2_x_pos = 120
    my_Ang2_y_pos = 650
    my_Ang2 = 0
    my_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')
    my_Ang3_x_pos = 165
    my_Ang3_y_pos = 650
    my_Ang3 = 0

    attack_button = pygame.image.load('.\\resource\\공격버튼.png')
    attack_button_size = attack_button.get_rect().size
    attack_button_x_pos = 75
    attack_button_y_pos = 350
    attack_button_width = attack_button_size[0]
    attack_button_height = attack_button_size[1]
    gard_button = pygame.image.load('.\\resource\\방어버튼.png')
    gard_button_size = gard_button.get_rect().size
    gard_button_x_pos = 75
    gard_button_y_pos = 410
    gard_button_width = gard_button_size[0]
    gard_button_height = gard_button_size[1]
    concentration_button = pygame.image.load('.\\resource\\집중버튼.png')
    concentration_button_size = concentration_button.get_rect().size
    concentration_button_x_pos = 75
    concentration_button_y_pos = 470
    concentration_button_width = concentration_button_size[0]
    concentration_button_height = concentration_button_size[1]

    fight_log = pygame.image.load('.\\resource\\싸움로그.png')
    fight_log_x_pos = 558
    fight_log_y_pos = 480





    

    if character == 'jammin':
        background = pygame.image.load('.\\resource\\장소1.png')
        enemy = pygame.image.load('.\\resource\\enemy\\샌즈.png')
        boss_max_hp = 10
        now_boss_hp = 10
        boss_skills = {'마구 부수기' : ('attack', 'attack', 'attack'), '소음공해' : ('gard', 'concentration', 'gard')}
        boss_debuff = [None, 0]
        boss_buff = [None, 0]
        boss_attack = 1
        boss_defense = 1
        enemy_x_pos = 400
        enemy_y_pos = 70

    if character == 'cockroach':
        conversation('cockroach', 1)
        background = pygame.image.load('.\\resource\\장소3.png')
        enemy = pygame.image.load('.\\resource\\enemy\\바퀴.png')
        boss_max_hp = 7
        now_boss_hp = 7
        boss_skills = {'질긴 생존력' : ('gard', 'gard', 'concentration'), '민초 폭탄' : ('concentration', 'concentration', 'attack')}
        revive = True
        boss_debuff = [None, 0]
        boss_buff = [None, 0]
        boss_attack = 1
        boss_defense = 1
        enemy_x_pos = 400
        enemy_y_pos = 70

    if character == 'junhyeok':
        background = pygame.image.load('.\\resource\\장소6.png')
        enemy = pygame.image.load('.\\resource\\enemy\\일라오이.png')
        boss_max_hp = 25
        now_boss_hp = 25
        boss_skills = {'촉수 소환' : ('concentration', 'concentration', 'concentration'), '촉수 강타' : ('attack', 'attack', 'attack')}
        boss_debuff = [None, 0]
        boss_buff = [None, 0]
        boss_attack = 1
        boss_defense = 2
        enemy_x_pos = 400
        enemy_y_pos = 70

    if character == 'reddragon':
        background = pygame.image.load('.\\resource\\장소7.png')
        enemy = pygame.image.load('.\\resource\\지도용홍룡.png')
        boss_max_hp = 40
        now_boss_hp = 40
        boss_skills = {'화염브레스' : ('gard', 'concentration', 'attack'), '앞발공격' : ('gard', 'attack', 'attack'), '마법 봉인' : ('gard', 'concentration', 'gard')}
        boss_debuff = [None, 0]
        boss_buff = [None, 0]
        boss_attack = 3
        boss_defense = 2
        enemy_x_pos = 400
        enemy_y_pos = 70
    
    if character == 'sunghyun':
        background = pygame.image.load('.\\resource\\탑1층.png')
        enemy = pygame.image.load('.\\resource\\enemy\\성현.png')
        boss_max_hp = 40
        now_boss_hp = 40
        boss_skills = {'총공격' : ('attack', 'attack', 'attack'), '완벽한 분담' : ('attack', 'gard', 'attack'), '애니멀테라피' : ('gard', 'concentration', 'concentration')}
        boss_debuff = [None, 0]
        boss_buff = [None, 0]
        boss_attack = 3
        boss_defense = 3
        enemy_x_pos = 470
        enemy_y_pos = 70

    if character == 'minyoung':
        background = pygame.image.load('.\\resource\\탑2층.jpg')
        enemy = pygame.image.load('.\\resource\\enemy\\톱날.png')
        boss_max_hp = 25
        now_boss_hp = 25
        boss_skills = {'보이지 않는 위협': ('concentration', 'concentration', 'attack'), '공포 음미' : ('attack', 'attack', 'attack'), '공허의 가시' : ('gard', 'attack', 'gard')}
        boss_debuff = [None, 0]
        boss_buff = [None, 0]
        boss_attack = 4
        boss_defense = 1
        enemy_x_pos = 470
        enemy_y_pos = 70
    
    if character == 'blackcow':
        background = pygame.image.load('.\\resource\\탑꼭대기1.png')
        enemy = pygame.image.load('.\\resource\\enemy\\장지.png')
        boss_max_hp = 55
        now_boss_hp = 55
        boss_skills = {'몸통박치기': ('concentration', 'gard', 'attack'), '도발의 춤': ('gard', 'concentration', 'gard')}
        boss_debuff = [None, 0]
        boss_buff = ['친구부르기', 0]
        boss_attack = 1
        boss_defense = 5
        enemy_x_pos = 470
        enemy_y_pos = 70
        play_sound = False
        cooky = 0
        ito = 0

    if character == 'ojimin':
        background = pygame.image.load('.\\resource\\탑꼭대기2.png')
        enemy = pygame.image.load('.\\resource\\enemy\\오지.png')
        boss_max_hp = 35
        now_boss_hp = 35
        boss_skills = {'흡혈' : ('concentration', 'concentration', 'attack'), '뽀록' : ('gard', 'gard', 'gard'), '평행시간교차' : ('concentration', 'attack', 'gard')}
        boss_debuff = [None, 0]
        boss_buff = [None, 0]
        boss_attack = 4
        boss_defense = 4
        enemy_x_pos = 470
        enemy_y_pos = 70

    my_debuff = [None, 0]
    my_buff = [None, 0]

    used_skill = None
    boss_skill = None
        
    special_event = font.render('', True, white)
    special_event_x_pos = 570
    special_event_y_pos = 680



    #이벤트 루프
    running = True #게임이 진행중인가?

    while running:
        dt = clock.tick(60)

        if now_my_hp <= 0:
            return 0
        elif now_boss_hp <= 0:
            if character == 'jammin':
                conversation('jammin', 1)
            elif character == 'cockroach':
                if revive == True:
                    revive = False
                    special_event = font.render('질긴 생명력', True, white)
                    now_boss_hp = boss_max_hp
                    continue
                if revive == False:
                    special_event = font.render('', True, white)
            return 1
            
        if my_debuff == ['기절예고', 0]:
            my_debuff = ['기절', 3]

        if my_debuff[0] == '기절':
            special_event = font.render('기절했습니다', True, white)

        if boss_debuff[0] != None and boss_debuff[1] <= 0:
            boss_debuff = [None, 0]
        
        if boss_buff[0] != None and boss_buff[1] <= 0:
            if boss_buff[0] != '친구부르기':
                boss_buff = [None, 0]
        
        if my_debuff[0] != None and my_debuff[1] <= 0:
            my_debuff = [None, 0]
        
        if my_buff[0] != None and my_buff[1] <= 0:
            my_buff = [None, 0]

        if character == 'junhyeok':
            if boss_buff[0] == '촉수':
                boss_attack = 2
            else:
                boss_attack = 1
            if now_boss_hp > boss_max_hp:
                now_boss_hp = boss_max_hp

        my_debuff_font = font.render('현재 디버프 : {}'.format(my_debuff[0]), True, white)
        my_debuff_font_x_pos = 570
        my_debuff_font_y_pos = 520
        my_buff_font = font.render('현재 버프 : {}'.format(my_buff[0]), True, white)
        my_buff_font_x_pos = 570
        my_buff_font_y_pos = 540
        boss_debuff_font = font.render('상대 디버프 : {}'.format(boss_debuff[0]), True, white)
        boss_debuff_font_x_pos = 570
        boss_debuff_font_y_pos = 560
        boss_buff_font = font.render('상대 버프 : {}'.format(boss_buff[0]), True, white)
        boss_buff_font_x_pos = 570
        boss_buff_font_y_pos = 580

        my_hp_font = font.render('나의 HP : {}'.format(now_my_hp), True, white)
        my_hp_font_x_pos = 570
        my_hp_font_y_pos = 600
        boss_hp_font = font.render('상대의 HP : {}'.format(now_boss_hp), True, white)
        boss_hp_font_x_pos = 570
        boss_hp_font_y_pos = 620

        if character == 'blackcow' and boss_buff[1] % 8 == 4:
            if play_sound == False:
                pygame.mixer.Sound('.\\resource\\sound\\시노부대사.wav').play()
                play_sound = True
            special_event = font.render('쿠키 시노부의 도움', True, black)
            cooky += 1
            my_debuff = ['감전', cooky]
            if boss_max_hp < now_boss_hp + 10:
                now_boss_hp = boss_max_hp
            else:
                now_boss_hp += 10
            boss_buff[1] + 1
            play_sound = False
        if character == 'blackcow' and boss_buff[1] % 8 == 0 and int(boss_buff[1] / 8) != 0:
            if play_sound == False:
                pygame.mixer.Sound('.\\resource\\sound\\이토대사.wav').play()
                play_sound = True
            special_event = font.render('아라타키 이토의 도움', True, black)
            ito += 1
            now_my_hp -= ito * 5
            boss_buff[1] += 1
            play_sound = False

            



        

        #이벤트 처리
        for event in pygame.event.get(): #이벤트 수집
            if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
                pygame.quit()
                sys.exit() #게임 실행 False
            if event.type == pygame.KEYUP: #########################좌표 확인 용
                if event.key == pygame.K_p:
                    print(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if event.type == pygame.MOUSEBUTTONDOWN or my_debuff[0] == '기절':
                if 5 < pygame.mouse.get_pos()[0] < 5 + items_width and 100 < pygame.mouse.get_pos()[1] < 100 + items_height:
                    heal = item('battle')
                    if heal == '제육볶음':
                        now_my_hp += 10
                    elif heal == '민트초코':
                        now_my_hp += 3
                    elif heal == '오징어다리':
                        now_my_hp += 5
                if attack_button_x_pos < pygame.mouse.get_pos()[0] < attack_button_x_pos + attack_button_width and attack_button_y_pos < pygame.mouse.get_pos()[1] < attack_button_y_pos + attack_button_height and my_debuff[0] != '기절':
                    my_Ang = [my_Ang1, my_Ang2, my_Ang3]
                    if boss_buff[0] == '흡혈중':
                        boss_buff[1] = 0
                    if my_debuff[0] == '도발' and my_debuff[1] == my_Ang.index(0):
                        my_debuff[1] = 0
                    pygame.mixer.Sound('.\\resource\\sound\\기본공격.wav').play()
                    if my_debuff[0] == '업화의 화염':
                        my_debuff[1] -= 1
                        if my_buff != ['피의 결계', 1]:
                            now_my_hp -= boss_attack
                            if my_buff[0] == '화내기':
                                now_my_hp -= boss_attack
                    if my_debuff[0] == ['감전']:
                        if my_buff != ['피의 결계', 1]:
                            now_my_hp -= my_debuff[1]
                            if my_buff[0] == '화내기':
                                now_my_hp -= my_debuff[1]
                    if my_Ang1 == 0:
                        my_Ang1 = 'attack'
                        my_Ang1_image = pygame.image.load('.\\resource\\공격코스트.png')
                    elif my_Ang2 == 0:
                        my_Ang2 = 'attack'
                        my_Ang2_image = pygame.image.load('.\\resource\\공격코스트.png')
                    elif my_Ang3 == 0:
                        my_Ang3 = 'attack'
                        my_Ang3_image = pygame.image.load('.\\resource\\공격코스트.png')
                        used_skill = None
                        for my_skill in my_skills: #my_skill은 딕셔너리 키
                            if my_skills[my_skill][0] == (my_Ang1, my_Ang2, my_Ang3): #my_skills[my_skill][0]은 스킬 사용 경로
                                print('{} 스킬 시전'.format(my_skill))
                                used_skill = my_skill
                        my_Ang1 = 0
                        my_Ang2 = 0
                        my_Ang3 = 0
                        my_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                        my_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                        my_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')

                    #보스 스킬 관련 (현재 앙이 공격이라고 가정 할 때)
                    if boss_Ang1 == 0:
                        boss_cast = random.choice(list(boss_skills.keys()))
                        if character == 'junhyeok':
                            if boss_buff[0] == None:
                                boss_cast = list(boss_skills.keys())[0]
                            else:
                                boss_cast = list(boss_skills.keys())[1]
                        boss_Ang1 = boss_skills[boss_cast][0]
                        if boss_Ang1 == 'attack':
                            boss_Ang1_image = pygame.image.load('.\\resource\\공격코스트.png')
                            now_boss_hp -= my_attack
                            if boss_buff[0] == '촉수':
                                if boss_debuff[0] != '실명':
                                    now_boss_hp += boss_attack
                                boss_buff[1] -= 1
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                                now_my_hp -= 0
                            else:
                                if my_buff != ['피의 결계', 1]:
                                    now_my_hp -= boss_attack
                                    if my_buff[0] == '화내기':
                                        now_my_hp -= boss_attack
                        elif boss_Ang1 == 'gard':
                            boss_Ang1_image = pygame.image.load('.\\resource\\방어코스트.png')
                            if my_attack - boss_defense >= 0:
                                now_boss_hp -= my_attack - boss_defense
                                if my_buff[0] == '화내기':
                                    now_boss_hp -= my_attack - boss_defense
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                        elif boss_Ang1 == 'concentration':
                            boss_Ang1_image = pygame.image.load('.\\resource\\집중코스트.png')
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            now_boss_hp -= my_attack
                            if my_buff[0] == '화내기':
                                now_boss_hp -= my_attack
                            ########################
                    elif boss_Ang2 == 0:
                        boss_Ang2 = boss_skills[boss_cast][1]
                        if boss_Ang2 == 'attack':
                            boss_Ang2_image = pygame.image.load('.\\resource\\공격코스트.png')
                            now_boss_hp -= my_attack
                            if my_buff[0] == '화내기':
                                now_boss_hp -= my_attack
                            if boss_buff[0] == '촉수':
                                if boss_debuff[0] != '실명':
                                    now_boss_hp += boss_attack
                                boss_buff[1] -= 1
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                                now_my_hp -= 0
                            else:
                                if my_buff != ['피의 결계', 1]:
                                    now_my_hp -= boss_attack
                                    if my_buff[0] == '화내기':
                                        now_my_hp -= boss_attack
                        elif boss_Ang2 == 'gard':
                            boss_Ang2_image = pygame.image.load('.\\resource\\방어코스트.png')
                            if my_attack - boss_defense >= 0:
                                now_boss_hp -= my_attack - boss_defense
                                if my_buff[0] == '화내기':
                                    now_boss_hp -= my_attack - boss_defense
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                        elif boss_Ang2 == 'concentration':
                            boss_Ang2_image = pygame.image.load('.\\resource\\집중코스트.png')
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            now_boss_hp -= my_attack
                            if my_buff[0] == '화내기':
                                now_boss_hp -= my_attack
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            #########################
                    elif boss_Ang3 == 0:
                        boss_Ang3 = boss_skills[boss_cast][2]
                        if boss_Ang3 == 'attack':
                            boss_Ang3_image = pygame.image.load('.\\resource\\공격코스트.png')
                            now_boss_hp -= my_attack
                            if my_buff[0] == '화내기':
                                now_boss_hp -= my_attack
                            if boss_buff[0] == '촉수':
                                if boss_debuff[0] != '실명':
                                    now_boss_hp += boss_attack
                                boss_buff[1] -= 1
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                                now_my_hp -= 0
                            else:
                                if my_buff != ['피의 결계', 1]:
                                    now_my_hp -= boss_attack
                                    if my_buff[0] == '화내기':
                                        now_my_hp -= boss_attack
                        elif boss_Ang3 == 'gard':
                            boss_Ang3_image = pygame.image.load('.\\resource\\방어코스트.png')
                            if my_attack - boss_defense >= 0:
                                now_boss_hp -= my_attack - boss_defense
                                if my_buff[0] == '화내기':
                                    now_boss_hp -= my_attack - boss_defense
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                        elif boss_Ang3 == 'concentration':
                            boss_Ang3_image = pygame.image.load('.\\resource\\집중코스트.png')
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            now_boss_hp -= my_attack
                            if my_buff[0] == '화내기':
                                now_boss_hp -= my_attack
                            if my_buff[0] == '신의 가호':
                                now_boss_hp -= 1
                                my_buff[1] -= 1
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                        for boss_skill in boss_skills:
                            if boss_skill == boss_cast:
                                if boss_debuff[0] == '화상':
                                    now_boss_hp -= boss_debuff[1]
                                    if my_skills['화염 방사'][1] <= boss_debuff[1]:
                                        now_boss_hp -= boss_debuff[1]
                                    if my_buff[0] == '신의 가호':
                                        now_boss_hp -= 1
                                        my_buff[1] -= 1
                                    boss_debuff[1] == 0
                                if my_debuff[0] == '식중독':
                                    if my_buff != ['피의 결계', 1]:
                                        now_my_hp -= 10 - my_skills['우마이'][1]
                                    my_debuff[1] -= 1
                                hp = skill_check(character, boss_cast, used_skill, now_my_hp, now_boss_hp, boss_debuff, boss_buff, my_debuff, my_buff, boss_attack, boss_defense, my_max_hp, boss_max_hp)
                                print(hp, type(hp))
                                now_boss_hp = hp[0]
                                now_my_hp = hp[1]
                                boss_debuff = hp[2]
                                boss_buff = hp[3]
                                my_debuff = hp[4]
                                my_buff = hp[5]
                                
                                break
                        boss_Ang1 = 0
                        boss_Ang2 = 0
                        boss_Ang3 = 0
                        boss_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                        boss_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                        boss_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')
                if gard_button_x_pos < pygame.mouse.get_pos()[0] < gard_button_x_pos + gard_button_width and gard_button_y_pos < pygame.mouse.get_pos()[1] < gard_button_y_pos + gard_button_height and my_debuff[0] != '기절':
                    my_Ang = [my_Ang1, my_Ang2, my_Ang3]
                    if my_debuff[0] == '도발' and my_debuff[1] != my_Ang.index(0) or my_debuff[0] != '도발':
                        pygame.mixer.Sound('.\\resource\\sound\\기본방어.wav').play()
                        if my_debuff[0] == ['감전']:
                            if my_buff != ['피의 결계', 1]:
                                now_my_hp -= my_debuff[1]
                                if my_buff[0] == '화내기':
                                    now_my_hp -= my_debuff[1]
                        if my_Ang1 == 0:
                            my_Ang1 = 'gard'
                            my_Ang1_image = pygame.image.load('.\\resource\\방어코스트.png')
                        elif my_Ang2 == 0:
                            my_Ang2 = 'gard'
                            my_Ang2_image = pygame.image.load('.\\resource\\방어코스트.png')
                        elif my_Ang3 == 0:
                            my_Ang3 = 'gard'
                            my_Ang3_image = pygame.image.load('.\\resource\\방어코스트.png')
                            used_skill = None
                            for my_skill in my_skills:
                                if my_skills[my_skill][0] == (my_Ang1, my_Ang2, my_Ang3):
                                    print('{} 스킬 시전'.format(my_skill))
                                    used_skill = my_skill
                            my_Ang1 = 0
                            my_Ang2 = 0
                            my_Ang3 = 0
                            my_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                            my_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                            my_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')

                        #보스 스킬 관련 (내 앙이 방어라고 가정)
                        if boss_Ang1 == 0:
                            boss_cast = random.choice(list(boss_skills.keys()))
                            if character == 'junhyeok':
                                if boss_buff[0] == None:
                                    boss_cast = list(boss_skills.keys())[0]
                                else:
                                    boss_cast = list(boss_skills.keys())[1]
                            boss_Ang1 = boss_skills[boss_cast][0]
                            if boss_Ang1 == 'attack':
                                boss_Ang1_image = pygame.image.load('.\\resource\\공격코스트.png')
                                if boss_buff[0] == '촉수':
                                    if boss_debuff[0] != '실명':
                                        if boss_attack - my_defence >= 0:
                                            now_boss_hp += boss_attack - my_defence
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                    now_my_hp -= 0
                                else:
                                    if my_buff != ['피의 결계', 1]:
                                        if boss_attack - my_defence >= 0:
                                            now_my_hp -= boss_attack - my_defence
                                            if my_buff[0] == '화내기':
                                                now_my_hp -= boss_attack - my_defence
                            elif boss_Ang1 == 'gard':
                                boss_Ang1_image = pygame.image.load('.\\resource\\방어코스트.png')
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            elif boss_Ang1 == 'concentration':
                                boss_Ang1_image = pygame.image.load('.\\resource\\집중코스트.png')
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                        elif boss_Ang2 == 0:
                            boss_Ang2 = boss_skills[boss_cast][1]
                            if boss_Ang2 == 'attack':
                                boss_Ang2_image = pygame.image.load('.\\resource\\공격코스트.png')
                                if boss_buff[0] == '촉수':
                                    if boss_debuff[0] != '실명':
                                        if boss_attack - my_defence >= 0:
                                            now_boss_hp += boss_attack
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                    now_my_hp -= 0
                                else:
                                    if my_buff != ['피의 결계', 1]:
                                        if boss_attack - my_defence >= 0:
                                            now_my_hp -= boss_attack - my_defence
                                            if my_buff[0] == '화내기':
                                                now_my_hp -= boss_attack - my_defence
                            elif boss_Ang2 == 'gard':
                                boss_Ang2_image = pygame.image.load('.\\resource\\방어코스트.png')
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            elif boss_Ang2 == 'concentration':
                                boss_Ang2_image = pygame.image.load('.\\resource\\집중코스트.png')
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                        elif boss_Ang3 == 0:
                            boss_Ang3 = boss_skills[boss_cast][2]
                            if boss_Ang3 == 'attack':
                                boss_Ang3_image = pygame.image.load('.\\resource\\공격코스트.png')
                                if boss_buff[0] == '촉수':
                                    if boss_debuff[0] != '실명':
                                        if boss_attack - my_defence >= 0:
                                            now_boss_hp += boss_attack
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                    now_my_hp -= 0
                                else:
                                    if my_buff != ['피의 결계', 1]:
                                        if boss_attack - my_defence >= 0:
                                            now_my_hp -= boss_attack - my_defence
                                            if my_buff[0] == '화내기':
                                                now_my_hp -= boss_attack - my_defence
                            elif boss_Ang3 == 'gard':
                                boss_Ang3_image = pygame.image.load('.\\resource\\방어코스트.png')
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            elif boss_Ang3 == 'concentration':
                                boss_Ang3_image = pygame.image.load('.\\resource\\집중코스트.png')
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            for boss_skill in boss_skills:
                                if boss_skill == boss_cast:
                                    if boss_debuff[0] == '화상':
                                        now_boss_hp -= boss_debuff[1]
                                        if my_skills['화염 방사'][1] <= boss_debuff[1]:
                                            now_boss_hp -= boss_debuff[1]
                                        if my_buff[0] == '신의 가호':
                                            now_boss_hp -= 1
                                            my_buff[1] -= 1
                                        boss_debuff[1] == 0
                                    if my_debuff[0] == '식중독':
                                        if my_buff != ['피의 결계', 1]:
                                            now_my_hp -= 10 - my_skills['우마이'][1]
                                        my_debuff[1] -= 1
                                    hp = skill_check(character, boss_cast, used_skill, now_my_hp, now_boss_hp, boss_debuff, boss_buff, my_debuff, my_buff, boss_attack, boss_defense, my_max_hp, boss_max_hp)
                                    print(hp, type(hp))
                                    now_boss_hp = hp[0]
                                    now_my_hp = hp[1]
                                    boss_debuff = hp[2]
                                    boss_buff = hp[3]
                                    my_debuff = hp[4]
                                    my_buff = hp[5]
                                    
                                    break

                            boss_Ang1 = 0
                            boss_Ang2 = 0
                            boss_Ang3 = 0
                            boss_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                            boss_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                            boss_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')
                if concentration_button_x_pos < pygame.mouse.get_pos()[0] < concentration_button_x_pos + concentration_button_width and concentration_button_y_pos < pygame.mouse.get_pos()[1] < concentration_button_y_pos + concentration_button_height and my_debuff[0] != '기절':
                    my_Ang = [my_Ang1, my_Ang2, my_Ang3]
                    if my_debuff[0] == '도발' and my_debuff[1] != my_Ang.index(0) or my_debuff[0] != '도발':
                        pygame.mixer.Sound('.\\resource\\sound\\집중.wav').play()
                        if my_debuff[0] == ['감전']:
                            if my_buff != ['피의 결계', 1]:
                                now_my_hp -= my_debuff[1]
                                if my_buff[0] == '화내기':
                                    now_my_hp -= my_debuff[1]
                        if my_Ang1 == 0: 
                            my_Ang1 = 'concentration'
                            my_Ang1_image = pygame.image.load('.\\resource\\집중코스트.png')
                        elif my_Ang2 == 0:
                            my_Ang2 = 'concentration'
                            my_Ang2_image = pygame.image.load('.\\resource\\집중코스트.png')
                        elif my_Ang3 == 0:
                            my_Ang3 = 'concentration'
                            my_Ang3_image = pygame.image.load('.\\resource\\집중코스트.png')
                            used_skill = None
                            for my_skill in my_skills:
                                if my_skills[my_skill][0] == (my_Ang1, my_Ang2, my_Ang3):
                                    print('{} 스킬 시전'.format(my_skill))
                                    used_skill = my_skill

                            my_Ang1 = 0
                            my_Ang2 = 0
                            my_Ang3 = 0
                            my_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                            my_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                            my_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')

                        #보스 스킬 관련 (내 앙이 집중이라고 가정)
                        if boss_Ang1 == 0:
                            boss_cast = random.choice(list(boss_skills.keys()))
                            if character == 'junhyeok':
                                if boss_buff[0] == None:
                                    boss_cast = list(boss_skills.keys())[0]
                                else:
                                    boss_cast = list(boss_skills.keys())[1]
                            boss_Ang1 = boss_skills[boss_cast][0]
                            if boss_Ang1 == 'attack':
                                boss_Ang1_image = pygame.image.load('.\\resource\\공격코스트.png')
                                if boss_buff[0] == '촉수':
                                    if boss_debuff[0] != '실명':
                                        now_boss_hp += boss_attack
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                    now_my_hp -= 0
                                else:
                                    if my_buff != ['피의 결계', 1]:
                                        now_my_hp -= boss_attack
                                        if my_buff[0] == '화내기':
                                            now_my_hp -= boss_attack
                            elif boss_Ang1 == 'gard':
                                boss_Ang1_image = pygame.image.load('.\\resource\\방어코스트.png')
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            elif boss_Ang1 == 'concentration':
                                boss_Ang1_image = pygame.image.load('.\\resource\\집중코스트.png')
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                        elif boss_Ang2 == 0:
                            boss_Ang2 = boss_skills[boss_cast][1]
                            if boss_Ang2 == 'attack':
                                boss_Ang2_image = pygame.image.load('.\\resource\\공격코스트.png')
                                if boss_buff[0] == '촉수':
                                    if boss_debuff[0] != '실명':
                                        now_boss_hp += boss_attack
                                    boss_buff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                    now_my_hp -= 0
                                else:
                                    if my_buff != ['피의 결계', 1]:
                                        now_my_hp -= boss_attack
                                        if my_buff[0] == '화내기':
                                            now_my_hp -= boss_attack
                            elif boss_Ang2 == 'gard':
                                boss_Ang2_image = pygame.image.load('.\\resource\\방어코스트.png')
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            elif boss_Ang2 == 'concentration':
                                boss_Ang2_image = pygame.image.load('.\\resource\\집중코스트.png')
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                        elif boss_Ang3 == 0:
                            boss_Ang3 = boss_skills[boss_cast][2]
                            if boss_Ang3 == 'attack':
                                boss_Ang3_image = pygame.image.load('.\\resource\\공격코스트.png')
                                if boss_buff[0] == '촉수':
                                    if boss_debuff[0] != '실명':
                                        now_boss_hp += boss_attack
                                    boss_buff[1] -= 1
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                    now_my_hp -= 0
                                else:
                                    if my_buff != ['피의 결계', 1]:
                                        now_my_hp -= boss_attack
                                        if my_buff[0] == '화내기':
                                            now_my_hp -= boss_attack
                            elif boss_Ang3 == 'gard':
                                boss_Ang3_image = pygame.image.load('.\\resource\\방어코스트.png')
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            elif boss_Ang3 == 'concentration':
                                boss_Ang3_image = pygame.image.load('.\\resource\\집중코스트.png')
                                if boss_buff[0] == '촉수':
                                    boss_buff[1] -= 1
                                if boss_debuff[0] == '실명':
                                    boss_debuff[1] -= 1
                                if boss_buff[0] == '흡혈중':
                                    boss_buff[1] -= 1
                                    if boss_max_hp >= now_boss_hp + boss_attack:
                                        now_boss_hp += boss_attack
                                    else:
                                        now_boss_hp = boss_max_hp
                            for boss_skill in boss_skills:
                                if boss_skill == boss_cast:
                                    if boss_debuff[0] == '화상':
                                        now_boss_hp -= boss_debuff[1]
                                        if my_skills['화염 방사'][1] <= boss_debuff[1]:
                                            now_boss_hp -= boss_debuff[1]
                                        if my_buff[0] == '신의 가호':
                                            now_boss_hp -= 1
                                            my_buff[1] -= 1
                                        boss_debuff[1] == 0
                                    if my_debuff[0] == '식중독':
                                        if my_buff != ['피의 결계', 1]:
                                            now_my_hp -= 10 - my_skills['우마이'][1]
                                        my_debuff[1] -= 1
                                    hp = skill_check(character, boss_cast, used_skill, now_my_hp, now_boss_hp, boss_debuff, boss_buff, my_debuff, my_buff, boss_attack, boss_defense, my_max_hp, boss_max_hp)
                                    print(hp, type(hp))
                                    now_boss_hp = hp[0]
                                    now_my_hp = hp[1]
                                    boss_debuff = hp[2]
                                    boss_buff = hp[3]
                                    my_debuff = hp[4]
                                    my_buff = hp[5]
                                    
                                    break

                            boss_Ang1 = 0
                            boss_Ang2 = 0
                            boss_Ang3 = 0
                            boss_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                            boss_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                            boss_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')
                if my_debuff[0] == '기절':
                    used_skill = None
                    for my_skill in my_skills:
                        if my_skills[my_skill][0] == (my_Ang1, my_Ang2, my_Ang3):
                            print('{} 스킬 시전'.format(my_skill))
                            used_skill = my_skill
                    my_Ang1 = 0
                    my_Ang2 = 0
                    my_Ang3 = 0
                    my_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                    my_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                    my_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')
                    if boss_Ang1 == 0:
                        boss_cast = random.choice(list(boss_skills.keys()))
                        
                        boss_Ang1 = boss_skills[boss_cast][0]
                        if boss_Ang1 == 'attack':
                            boss_Ang1_image = pygame.image.load('.\\resource\\공격코스트.png')
                            if boss_buff[0] == '촉수':
                                if boss_debuff[0] != '실명':
                                    now_boss_hp += boss_attack
                                boss_buff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                                now_my_hp -= 0
                            else:
                                if my_buff != ['피의 결계', 1]:
                                    now_my_hp -= boss_attack
                                    if my_buff[0] == '화내기':
                                        now_my_hp -= boss_attack
                        elif boss_Ang1 == 'gard':
                            boss_Ang1_image = pygame.image.load('.\\resource\\방어코스트.png')
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                        elif boss_Ang1 == 'concentration':
                            boss_Ang1_image = pygame.image.load('.\\resource\\집중코스트.png')
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                    elif boss_Ang2 == 0:
                        boss_Ang2 = boss_skills[boss_cast][1]
                        if boss_Ang2 == 'attack':
                            boss_Ang2_image = pygame.image.load('.\\resource\\공격코스트.png')
                            if boss_buff[0] == '촉수':
                                if boss_debuff[0] != '실명':
                                    now_boss_hp += boss_attack
                                boss_buff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                                now_my_hp -= 0
                            else:
                                if my_buff != ['피의 결계', 1]:
                                    now_my_hp -= boss_attack
                                    if my_buff[0] == '화내기':
                                        now_my_hp -= boss_attack
                        elif boss_Ang2 == 'gard':
                            boss_Ang2_image = pygame.image.load('.\\resource\\방어코스트.png')
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                        elif boss_Ang2 == 'concentration':
                            boss_Ang2_image = pygame.image.load('.\\resource\\집중코스트.png')
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                    elif boss_Ang3 == 0:
                        boss_Ang3 = boss_skills[boss_cast][2]
                        if boss_Ang3 == 'attack':
                            boss_Ang3_image = pygame.image.load('.\\resource\\공격코스트.png')
                            if boss_buff[0] == '촉수':
                                if boss_debuff[0] != '실명':
                                    now_boss_hp += boss_attack
                                boss_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                                now_my_hp -= 0
                            else:
                                if my_buff != ['피의 결계', 1]:
                                    now_my_hp -= boss_attack
                                    if my_buff[0] == '화내기':
                                        now_my_hp -= boss_attack
                        elif boss_Ang3 == 'gard':
                            boss_Ang3_image = pygame.image.load('.\\resource\\방어코스트.png')
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                        elif boss_Ang3 == 'concentration':
                            boss_Ang3_image = pygame.image.load('.\\resource\\집중코스트.png')
                            if boss_buff[0] == '촉수':
                                boss_buff[1] -= 1
                            if boss_debuff[0] == '실명':
                                boss_debuff[1] -= 1
                            if boss_buff[0] == '흡혈중':
                                boss_buff[1] -= 1
                                if boss_max_hp >= now_boss_hp + boss_attack:
                                    now_boss_hp += boss_attack
                                else:
                                    now_boss_hp = boss_max_hp
                        for boss_skill in boss_skills:
                            if boss_skill == boss_cast:
                                if boss_debuff[0] == '화상':
                                    now_boss_hp -= boss_debuff[1]
                                    if my_skills['화염 방사'][1] <= boss_debuff[1]:
                                        now_boss_hp -= boss_debuff[1]
                                    if my_buff[0] == '신의 가호':
                                        now_boss_hp -= 1
                                        my_buff[1] -= 1
                                    boss_debuff[1] == 0
                                if my_debuff[0] == '식중독':
                                    if my_buff != ['피의 결계', 1]:
                                        now_my_hp -= 10 - my_skills['우마이'][1]
                                    my_debuff[1] -= 1
                                hp = skill_check(character, boss_cast, used_skill, now_my_hp, now_boss_hp, boss_debuff, boss_buff, my_debuff, my_buff, boss_attack, boss_defense, my_max_hp, boss_max_hp)
                                print(hp, type(hp))
                                now_boss_hp = hp[0]
                                now_my_hp = hp[1]
                                boss_debuff = hp[2]
                                boss_buff = hp[3]
                                my_debuff = hp[4]
                                my_buff = hp[5]
                                
                                break
                        boss_Ang1 = 0
                        boss_Ang2 = 0
                        boss_Ang3 = 0
                        boss_Ang1_image = pygame.image.load('.\\resource\\코스트틀.png')
                        boss_Ang2_image = pygame.image.load('.\\resource\\코스트틀.png')
                        boss_Ang3_image = pygame.image.load('.\\resource\\코스트틀.png')
                



        #게임 캐릭터 위치 정의
        if used_skill == None:
            used_skill_font = font.render('', True, white)
        else:
            used_skill_font = font.render('사용 스킬 : {}'.format(used_skill), True, white)
        used_skill_font_x_pos = 570
        used_skill_font_y_pos = 640
        if boss_skill == None:
            boss_skill_font = font.render('', True, white)
        else:
            boss_skill_font = font.render('상대 스킬 : {}'.format(boss_skill), True, white)
        boss_skill_font_x_pos = 570
        boss_skill_font_y_pos = 660
        #충돌처리

        #화면에 그리기
        screen.fill(white)
        screen.blit(gameui, (gameui_x_pos, gameui_y_pos))
        screen.blit(background, (70, 70))
        pygame.draw.rect(screen, boss_hp_coler, pygame.Rect(boss_hp_frame_x_pos, boss_hp_frame_y_pos, boss_hp_frame_width * now_boss_hp / boss_max_hp, 30))
        pygame.draw.rect(screen, my_hp_coler, pygame.Rect(my_hp_frame_x_pos, my_hp_frame_y_pos, my_hp_frame_width * now_my_hp / my_max_hp, 30))
        screen.blit(boss_hp_frame, (boss_hp_frame_x_pos, boss_hp_frame_y_pos))
        screen.blit(my_hp_frame, (my_hp_frame_x_pos, my_hp_frame_y_pos))

        screen.blit(fight_log, (fight_log_x_pos, fight_log_y_pos))
        screen.blit(my_debuff_font, (my_debuff_font_x_pos, my_debuff_font_y_pos))
        screen.blit(my_buff_font, (my_buff_font_x_pos, my_buff_font_y_pos))
        screen.blit(boss_debuff_font, (boss_debuff_font_x_pos, boss_debuff_font_y_pos))
        screen.blit(boss_buff_font, (boss_buff_font_x_pos, boss_buff_font_y_pos))
        screen.blit(my_hp_font, (my_hp_font_x_pos, my_hp_font_y_pos))
        screen.blit(boss_hp_font, (boss_hp_font_x_pos, boss_hp_font_y_pos))
        screen.blit(used_skill_font, (used_skill_font_x_pos, used_skill_font_y_pos))
        screen.blit(boss_skill_font, (boss_skill_font_x_pos, boss_skill_font_y_pos))
        screen.blit(special_event, (special_event_x_pos, special_event_y_pos))


        screen.blit(attack_button, (attack_button_x_pos, attack_button_y_pos))
        screen.blit(gard_button, (gard_button_x_pos, gard_button_y_pos))
        screen.blit(concentration_button, (concentration_button_x_pos, concentration_button_y_pos))
        screen.blit(boss_Ang1_image, (boss_Ang1_x_pos, boss_Ang1_y_pos))
        screen.blit(boss_Ang2_image, (boss_Ang2_x_pos, boss_Ang2_y_pos))
        screen.blit(boss_Ang3_image, (boss_Ang3_x_pos, boss_Ang3_y_pos))
        screen.blit(my_Ang1_image, (my_Ang1_x_pos, my_Ang1_y_pos))
        screen.blit(my_Ang2_image, (my_Ang2_x_pos, my_Ang2_y_pos))
        screen.blit(my_Ang3_image, (my_Ang3_x_pos, my_Ang3_y_pos))
        screen.blit(items, (5, 100))
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

        pygame.display.update()


def skill_check(boss_name, boss_cast, used_skill, now_my_hp, now_boss_hp, boss_debuff, boss_buff, my_debuff, my_buff, boss_attack, boss_defense, my_max_hp, boss_max_hp):
    global my_attacking
    global my_defence
    global my_skills
    print('{} 시전'.format(boss_cast)) #if문으로 boss_cast 확인 후 데미지나 효과 처리
    if used_skill == None:
        my_attacking = 0
        my_garding = 0
    if used_skill == '삼연속베기':
        three_slashes = pygame.mixer.Sound('.\\resource\\sound\\3연속베기.wav')
        three_slashes.play()
        if (my_skills['삼연속베기'][1]) <= 5:
            additional_damage = (my_skills['삼연속베기'][1])
        else:
            additional_damage = 5
        my_attacking = (my_attack - 1) * 2 + my_attack + additional_damage
        my_garding = 0
    elif used_skill == '텟카이':
        짱짱쎈방어 = pygame.mixer.Sound('.\\resource\\sound\\스킬방어.wav')
        짱짱쎈방어.play()
        if (my_skills['텟카이'][1]) <= 5:
            additional_gard = (my_skills['텟카이'][1])
        else:
            additional_gard = 5
        my_garding = (my_defence - 1) * 2 + my_defence + additional_gard
        my_attacking = 0
    elif used_skill == '실명다트':
        if my_debuff[0] == '마법 봉인':
            마법봉인 = pygame.mixer.Sound('.\\resource\\sound\\마법봉인.wav')
            마법봉인.play()
            my_debuff[1] -= 1
            my_attacking = my_attack
            my_garding - 0
        else:
            실명다트 = pygame.mixer.Sound('.\\resource\\sound\\실명_다트.wav')
            실명다트.play()
            my_garding = 0
            my_attacking = my_attack + my_skills['실명다트'][1]
            boss_debuff = ['실명', 3]
    elif used_skill == '신의 가호':
        if my_debuff[0] == '마법 봉인':
            마법봉인 = pygame.mixer.Sound('.\\resource\\sound\\마법봉인.wav')
            마법봉인.play()
            my_debuff[1] -= 1
            my_attacking = 0
            my_garding = 0
        else:
            신의가호 = pygame.mixer.Sound('.\\resource\\sound\\신의가호.wav')
            신의가호.play()
            my_garding = 0
            my_attacking = 0
            my_buff = ['신의 가호', 5]
    elif used_skill == '화내기':
        화내기 = pygame.mixer.Sound('.\\resource\\sound\\화내기.wav')
        화내기.play()
        my_attacking = my_attack + my_skills['화내기'][1]
        my_garding = my_defence + my_skills['화내기'][1]
        my_buff = ['흥분',  my_skills['화내기'][1]]
    elif used_skill == '피의 결계':
        if my_buff[0] != '피의 결계':
            now_my_hp -= 16 - my_skills['피의 결계'][1]
            if my_debuff[0] == '마법 봉인':
                마법봉인 = pygame.mixer.Sound('.\\resource\\sound\\마법봉인.wav')
                마법봉인.play()
                my_attacking = 0
                my_garding = 0
            else:
                피의결계 = pygame.mixer.Sound('.\\resource\\sound\\피의결계.wav')
                피의결계.play()
                my_attacking = 0
                my_garding = 0
                my_buff = ['피의 결계', 2]
        my_attacking = 0
        my_garding = 0
    elif used_skill == '흡수':
        if my_debuff[0] == '마법 봉인':
            마법봉인 = pygame.mixer.Sound('.\\reosurce\\sound\\마법봉인.wav')
            마법봉인.play()
            my_attacking = 0
            my_garding = 0
        else:
            흡수 = pygame.mixer.Sound('.\\resource\\sound\\흡수.wav')
            흡수.play()
            now_boss_hp -= my_skills['흡수'][1]
            now_my_hp += my_skills['흡수'][1]
            if my_max_hp / 2 >= now_my_hp:
                now_my_hp += int(my_skills['흡수'][1] // 2)
            my_attacking = 0
            my_garding = 0


    if boss_name == 'jammin':
        if boss_cast == '마구 부수기':
            boss_attacking = boss_attack * 3
            boss_garding = 0
        elif boss_cast == '소음공해':
            if my_buff != ['피의 결계', 1]:
                now_my_hp -= boss_attack
            boss_attacking = 0
            boss_garding = 0
    elif boss_name == 'cockroach':
        if boss_cast == '질긴 생존력':
            boss_attacking = 0
            boss_garding = 9999
            now_boss_hp += my_attacking
        elif boss_cast == '민초 폭탄':
            boss_attacking = boss_attack * 2
            boss_garding = boss_defense
    elif boss_name == 'junhyeok':
        if boss_cast == '촉수 소환':
            boss_attacking = 0
            boss_garding = 0
            boss_buff = ['촉수', 6]
        if boss_cast == '촉수 강타':
            boss_attacking = boss_attack * 3
            boss_garding = 0
    elif boss_name == 'reddragon':
        if boss_cast == '화염브레스':
            boss_attacking = boss_attack * 2
            boss_garding = 0
            my_debuff = ['업화의 화염', 3]
        elif boss_cast == '앞발공격':
            boss_attacking = boss_attack * 2
            boss_garding = boss_defense * 2
        elif boss_cast == '마법 봉인':
            boss_attacking = 0
            boss_garding = boss_defense
            my_debuff = ['마법 봉인', 2]
    elif boss_name == 'sunghyun':
        if boss_cast == '총공격':
            boss_attacking = boss_attack * 4
            boss_garding = 0
        elif boss_cast == '완전분담':
            boss_attacking = boss_attack * 2
            boss_garding = boss_defense * 2
        elif boss_cast == '애니멀테라피':
            boss_attacking = 0
            boss_garding = boss_defense * 2
            now_boss_hp += boss_max_hp - now_boss_hp // 4
    elif boss_name == 'minyoung':
        if boss_cast == '보이지 않는 위협':
            boss_attacking = boss_attack
            boss_garding = boss_defense * 5
            my_debuff = ['공포', 2]
        elif boss_cast == '공포 음미':
            if my_debuff[0] == '공포':
                boss_attacking = boss_attack * 6
            else:
                boss_attacking = boss_attack * 4
            boss_garding = 0
        elif boss_cast == '공허의 가시':
            if my_debuff[0] == '공포':
                boss_attacking = boss_attack * 2
                boss_garding = boss_defense * 2
                now_boss_hp += 7
            else:
                boss_attacking = boss_attack
                boss_garding = boss_defense * 3
    elif boss_name == 'blackcow':
        if boss_cast == '몸통박치기':
            boss_attacking = now_boss_hp // 5
            boss_garding -= now_boss_hp // 10
        elif boss_cast == '도발의 춤':
            boss_attacking = 0
            boss_garding = boss_defense * 2
            my_debuff = ['도발', random.randint(1, 3)]
        boss_buff[1] += 1
    elif boss_name == 'ojimin':
        if boss_cast == '흡혈':
            boss_buff = ['흡혈중', 6]
            boss_attacking = boss_attack
            boss_garding = 0
        elif boss_cast == '뽀록':
            if random.randint(1, 25) == 1:
                boss_attacking = boss_attack * 10
            else:
                boss_attacking = boss_attack
            boss_garding = boss_defense
        elif boss_cast == '평행시간교차':
            my_debuff = ['기절예고', 2]
            boss_attacking = 0 
            boss_garding = 0
            
    
    if used_skill == '화염 방사':
        if my_debuff[0] == '마법 봉인':
            마법봉인 = pygame.mixer.Sound('.\\resource\\sound\\마법봉인.wav')
            마법봉인.play()
            my_debuff[1] -= 1
            my_attacking = my_attack
            my_garding = 0
        else:
            화염방사 = pygame.mixer.Sound('.\\resource\\sound\\화염방사.wav')
            화염방사.play()
            boss_debuff = ['화상', boss_garding]
            my_attacking = my_skills['화염 방사'][1]
            my_garding = 0
    elif used_skill == '우마이':
        if my_debuff[0] == '마법 봉인':
            마법봉인 = pygame.mixer.Sound('.\\resource\\sound\\마법봉인.wav')
            마법봉인.play()
            my_debuff[1] -= 1
            my_attacking = my_attack - 1
            my_garding = my_garding - 1
        else:
            우마이 = pygame.mixer.Sound('.\\resource\\sound\\우마이.wav')
            우마이.play()
            my_debuff = ['식중독', 1]
            my_attacking = my_attack - 1
            my_garding = my_defence - 1

    if my_attacking - boss_garding > 0:
        now_boss_hp -= my_attacking - boss_garding
        if my_buff[0] == '화내기':
            now_boss_hp -= my_attacking - boss_garding
    if boss_attacking - my_garding > 0:
        if my_buff != ['피의 결계', 1]:
            now_my_hp -= boss_attacking - my_garding
            if my_buff[0] == '화내기':
                now_my_hp -= boss_attacking - my_garding
            if my_buff[0] == '피의 결계':
                my_buff[1] -= 1
        else:
            my_buff[1] -= 1
    if my_debuff[0] == '공포':
        my_debuff[1] -= 1
    if my_debuff[0] == '기절예고':
        my_debuff[1] -= 1
    return([now_boss_hp, now_my_hp, boss_debuff, boss_buff, my_debuff, my_buff])

def item(cause=None):
    global screen_width
    global screen_height
    global items
    global item_list
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    a = 0 # 어떤 프레임에 담았는지 확인용

    background = pygame.image.load('.\\resource\\아이템창.png')
    background_size = background.get_rect().size
    background_width = background_size[0]
    background_height = background_size[1]
    background_x_pos = screen_width / 2 - background_width / 2
    background_y_pos = screen_height / 2 - background_height / 2

    close_button = pygame.image.load('.\\resource\\X버튼.png')
    close_button_size = close_button.get_rect().size
    close_button_width = close_button_size[0]
    close_button_height = close_button_size[1]
    close_button_x_pos = background_x_pos + background_width - close_button_width
    close_button_y_pos = background_y_pos

    item_frame1 = pygame.image.load('.\\resource\\아이템틀.png')
    item_frame2 = pygame.image.load('.\\resource\\아이템틀.png')
    item_frame3 = pygame.image.load('.\\resource\\아이템틀.png')
    item_frame4 = pygame.image.load('.\\resource\\아이템틀.png')
    item_frame5 = pygame.image.load('.\\resource\\아이템틀.png')
    item_frame6 = pygame.image.load('.\\resource\\아이템틀.png')
    item_frame_size = item_frame1.get_rect().size
    item_frame_width = item_frame_size[0]
    item_frame_height = item_frame_size[1]

    item_frame1_x_pos = background_x_pos + 50 + 5 #아이템 화면 + 5
    item_frame2_x_pos = item_frame1_x_pos + item_frame_width + 20
    item_frame3_x_pos = item_frame2_x_pos + item_frame_width + 20
    item_frame4_x_pos = item_frame3_x_pos + item_frame_width + 20
    item_frame5_x_pos = item_frame4_x_pos + item_frame_width + 20
    item_frame6_x_pos = item_frame5_x_pos + item_frame_width + 20
    item_frame_y_pos = 230

    stick_image = pygame.image.load('.\\resource\\나뭇가지.png')
    stick_x_pos = 720
    stick_y_pos = 720

    bone_image = pygame.image.load('.\\resource\\뼈.png')
    bone_x_pos = 720
    bone_y_pos = 720
    
    mintchoco_image = pygame.image.load('.\\resource\\민트초코.png')
    mintchoco_x_pos = 720
    mintchoco_y_pos = 720

    squid_leg_image = pygame.image.load('.\\resource\\오징어다리.png')
    squid_leg_x_pos = 720
    squid_leg_y_pos = 720

    dragon_head_image = pygame.image.load('.\\resource\\용의머리.png')
    dragon_head_x_pos = 720
    dragon_head_y_pos = 720

    bluescreen_image = pygame.image.load('.\\resource\\단조설계도아이템.png')
    bluescreen_x_pos = 720
    bluescreen_y_pos = 720

    scroll_image = pygame.image.load('.\\resource\\스크롤아이템.png')
    scroll_x_pos = 720
    scroll_y_pos = 720

    jeyookbokkem_image = pygame.image.load('.\\resource\\제육볶음아이템.png')
    jeyookbokkem_x_pos = 720
    jeyookbokkem_y_pos = 720

    eating_button = pygame.image.load('.\\resource\\먹기버튼.png')
    eating_button_x_pos = 720
    eating_button_y_pos = 720
    eating_button_size = eating_button.get_rect().size
    eating_button_width = eating_button_size[0]
    eating_button_height = eating_button_size[1]

    synthesis_button = pygame.image.load('.\\resource\\합성.png')
    synthesis_button_x_pos = 720
    synthesis_button_y_pos = 720
    synthesis_button_size = synthesis_button.get_rect().size
    synthesis_button_width = synthesis_button_size[0]
    synthesis_button_height = synthesis_button_size[1]

    itemframe1_item = ''
    itemframe2_item = ''
    itemframe3_item = ''
    itemframe4_item = ''
    itemframe5_item = ''
    itemframe6_item = ''

    itemframe1_explanation = ''
    itemframe2_explanation = ''
    itemframe3_explanation = ''
    itemframe4_explanation = ''
    itemframe5_explanation = ''
    itemframe6_explanation = ''

    itemframe1_explanation2 = ''
    itemframe2_explanation2 = ''
    itemframe3_explanation2 = ''
    itemframe4_explanation2 = ''
    itemframe5_explanation2 = ''
    itemframe6_explanation2 = ''

    itemframe1_count = ''
    itemframe2_count = ''
    itemframe3_count = ''
    itemframe4_count = ''
    itemframe5_count = ''
    itemframe6_count = ''


    item_name = ''
    explanation = ''
    explanation2 = ''
    item_count = ''

    item_name_font = font.render('', True, black)
    explanation_font = font.render('', True, black)
    explanation2_font = font.render('', True, black)
    item_count_font = font.render('', True, black)
    


    for i in item_list: #i는 아이템이름 중 하나를 꺼내온 값
        b = item_list.get(i)[0] #b는 아이템의 개수, 아이템 이름으로 아이템 개수를 꺼내옴
        if b != 0: #아이템이 하나라도 있다면
            a += 1 #a는 아이템을 표시할 프레임의 번호
            item_name = i
            explanation = item_list.get(i)[1]
            explanation2 = item_list.get(i)[2]
            item_count = b
            if i == '나뭇가지':
                if a == 1:
                    stick_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    stick_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    stick_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    stick_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    stick_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    stick_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                stick_y_pos = item_frame_y_pos
            if i == '뼈':
                if a == 1:
                    bone_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    bone_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    bone_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    bone_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    bone_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    bone_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                bone_y_pos = item_frame_y_pos
            if i == '민트초코':
                explanation2 = item_list.get(i)[2]
                if a == 1:
                    mintchoco_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    mintchoco_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    mintchoco_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    mintchoco_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    mintchoco_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    mintchoco_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                mintchoco_y_pos = item_frame_y_pos
            if i == '오징어다리':
                if a == 1:
                    squid_leg_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    squid_leg_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    squid_leg_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    squid_leg_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    squid_leg_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    squid_leg_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                squid_leg_y_pos = item_frame_y_pos
            if i == '용의 머리':
                if a == 1:
                    dragon_head_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    dragon_head_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    dragon_head_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    dragon_head_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    dragon_head_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    dragon_head_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                dragon_head_y_pos = item_frame_y_pos
            if i == '단조 설계도':
                if a == 1:
                    bluescreen_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    bluescreen_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    bluescreen_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    bluescreen_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    bluescreen_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    bluescreen_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                bluescreen_y_pos = item_frame_y_pos
            if i == '스크롤':
                if a == 1:
                    scroll_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    scroll_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    scroll_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    scroll_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    scroll_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    scroll_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                scroll_y_pos = item_frame_y_pos
            if i == '제육볶음':
                if a == 1:
                    jeyookbokkem_x_pos = item_frame1_x_pos + 2.5
                    itemframe1_item = item_name
                    itemframe1_explanation = explanation
                    itemframe1_explanation2 = explanation2
                    itemframe1_count = item_count
                if a == 2:
                    jeyookbokkem_x_pos = item_frame2_x_pos + 2.5
                    itemframe2_item = item_name
                    itemframe2_explanation = explanation
                    itemframe2_explanation2 = explanation2
                    itemframe2_count = item_count
                if a == 3:
                    jeyookbokkem_x_pos = item_frame3_x_pos + 2.5
                    itemframe3_item = item_name
                    itemframe3_explanation = explanation
                    itemframe3_explanation2 = explanation2
                    itemframe3_count = item_count
                if a == 4:
                    jeyookbokkem_x_pos = item_frame4_x_pos + 2.5
                    itemframe4_item = item_name
                    itemframe4_explanation = explanation
                    itemframe4_explanation2 = explanation2
                    itemframe4_count = item_count
                if a == 5:
                    jeyookbokkem_x_pos = item_frame5_x_pos + 2.5
                    itemframe5_item = item_name
                    itemframe5_explanation = explanation
                    itemframe5_explanation2 = explanation2
                    itemframe5_count = item_count
                if a == 6:
                    jeyookbokkem_x_pos = item_frame6_x_pos + 2.5
                    itemframe6_item = item_name
                    itemframe6_explanation = explanation
                    itemframe6_explanation2 = explanation2
                    itemframe6_count = item_count
                jeyookbokkem_y_pos = item_frame_y_pos

                    





    running = True

    while running:
        dt = clock.tick(60)

        #이벤트 처리
        for event in pygame.event.get(): #이벤트 수집
            if event.type == pygame.MOUSEBUTTONDOWN: #창이 닫히는 이벤트가 발생하였는가?
                if close_button_x_pos < pygame.mouse.get_pos()[0] < close_button_x_pos + close_button_width and close_button_y_pos < pygame.mouse.get_pos()[1] < close_button_y_pos + close_button_height:
                    pygame.mixer.Sound('.\\resource\\sound\\대화창다음으로.wav').play()
                    running = False #게임 실행 False
                if item_frame1_x_pos < pygame.mouse.get_pos()[0] < item_frame1_x_pos + item_frame_width and item_frame_y_pos < pygame.mouse.get_pos()[1] < item_frame_y_pos + item_frame_height:
                    item_name = itemframe1_item
                    item_name_font = font.render('{}'.format(item_name), True, black)
                    explanation_font = font.render('{}'.format(itemframe1_explanation), True, black)
                    explanation2_font = font.render('{}'.format(itemframe1_explanation2), True, black)
                    if itemframe1_item == '':
                        item_count_font = font.render('', True, black)
                    else:
                        if cause == 'synthesis':
                            synthesis_button_x_pos = 305
                            synthesis_button_y_pos = 475
                        item_count_font = font.render('{}개'.format(itemframe1_count), True, black)
                    if itemframe1_item == '민트초코' or itemframe1_item == '제육볶음' or itemframe1_item == '오징어다리':
                        if cause == 'battle':
                            eating_button_x_pos = 305
                            eating_button_y_pos = 475
                            eat_item_name = itemframe1_item
                    else:
                        eating_button_x_pos = 720
                        eating_button_y_pos = 720
                elif item_frame2_x_pos < pygame.mouse.get_pos()[0] < item_frame2_x_pos + item_frame_width and item_frame_y_pos < pygame.mouse.get_pos()[1] < item_frame_y_pos + item_frame_height:
                    item_name = itemframe2_item
                    item_name_font = font.render('{}'.format(item_name), True, black)
                    explanation_font = font.render('{}'.format(itemframe2_explanation), True, black)
                    explanation2_font = font.render('{}'.format(itemframe2_explanation2), True, black)
                    if itemframe2_item == '':
                        item_count_font = font.render('', True, black)
                        synthesis_button_x_pos = 720
                        synthesis_button_y_pos = 720
                    else:
                        if cause == 'synthesis':
                            synthesis_button_x_pos = 305
                            synthesis_button_y_pos = 475
                        else:
                            synthesis_button_x_pos = 720
                            synthesis_button_y_pos = 720
                        item_count_font = font.render('{}개'.format(itemframe2_count), True, black)
                    if itemframe2_item == '민트초코' or itemframe2_item == '제육볶음' or itemframe2_item == '오징어다리':
                        if cause == 'battle':
                            eating_button_x_pos = 305
                            eating_button_y_pos = 475
                            eat_item_name = itemframe2_item
                    else:
                        eating_button_x_pos = 720
                        eating_button_y_pos = 720
                elif item_frame3_x_pos < pygame.mouse.get_pos()[0] < item_frame3_x_pos + item_frame_width and item_frame_y_pos < pygame.mouse.get_pos()[1] < item_frame_y_pos + item_frame_height:
                    item_name = itemframe3_item
                    item_name_font = font.render('{}'.format(item_name), True, black)
                    explanation_font = font.render('{}'.format(itemframe3_explanation), True, black)
                    explanation2_font = font.render('{}'.format(itemframe3_explanation2), True, black)
                    if itemframe3_item == '':
                        item_count_font = font.render('', True, black)
                        synthesis_button_x_pos = 720
                        synthesis_button_y_pos = 720
                    else:
                        if cause == 'synthesis':
                            synthesis_button_x_pos = 305
                            synthesis_button_y_pos = 475
                        else:
                            synthesis_button_x_pos = 720
                            synthesis_button_y_pos = 720
                        item_count_font = font.render('{}개'.format(itemframe3_count), True, black)
                    if itemframe3_item == '민트초코' or itemframe3_item == '제육볶음' or itemframe3_item == '오징어다리':
                        if cause == 'battle':
                            eating_button_x_pos = 305
                            eating_button_y_pos = 475
                            eat_item_name = itemframe3_item
                    else:
                        eating_button_x_pos = 720
                        eating_button_y_pos = 720
                elif item_frame4_x_pos < pygame.mouse.get_pos()[0] < item_frame4_x_pos + item_frame_width and item_frame_y_pos < pygame.mouse.get_pos()[1] < item_frame_y_pos + item_frame_height:
                    item_name = itemframe4_item
                    item_name_font = font.render('{}'.format(item_name), True, black)
                    explanation_font = font.render('{}'.format(itemframe4_explanation), True, black)
                    explanation2_font = font.render('{}'.format(itemframe4_explanation2), True, black)
                    if itemframe4_item == '':
                        item_count_font = font.render('', True, black)
                        synthesis_button_x_pos = 720
                        synthesis_button_y_pos = 720
                    else:
                        if cause == 'synthesis':
                            synthesis_button_x_pos = 305
                            synthesis_button_y_pos = 475
                        else:
                            synthesis_button_x_pos = 720
                            synthesis_button_y_pos = 720
                        item_count_font = font.render('{}개'.format(itemframe4_count), True, black)
                    if itemframe4_item == '민트초코' or itemframe4_item == '제육볶음' or itemframe4_item == '오징어다리':
                        if cause == 'battle':
                            eating_button_x_pos = 305
                            eating_button_y_pos = 475
                            eat_item_name = itemframe4_item
                    else:
                        eating_button_x_pos = 720
                        eating_button_y_pos = 720
                elif item_frame5_x_pos < pygame.mouse.get_pos()[0] < item_frame5_x_pos + item_frame_width and item_frame_y_pos < pygame.mouse.get_pos()[1] < item_frame_y_pos + item_frame_height:
                    item_name = itemframe5_item
                    item_name_font = font.render('{}'.format(item_name), True, black)
                    explanation_font = font.render('{}'.format(itemframe5_explanation), True, black)
                    explanation2_font = font.render('{}'.format(itemframe5_explanation2), True, black)
                    if itemframe5_item == '':
                        item_count_font = font.render('', True, black)
                        synthesis_button_x_pos = 720
                        synthesis_button_y_pos = 720
                    else:
                        if cause == 'synthesis':
                            synthesis_button_x_pos = 305
                            synthesis_button_y_pos = 475
                        else:
                            synthesis_button_x_pos = 720
                            synthesis_button_y_pos = 720
                        item_count_font = font.render('{}개'.format(itemframe5_count), True, black)
                    if itemframe5_item == '민트초코' or itemframe5_item == '제육볶음' or itemframe5_item == '오징어다리':
                        if cause == 'battle':
                            eating_button_x_pos = 305
                            eating_button_y_pos = 475
                            eat_item_name = itemframe5_item
                    else:
                        eating_button_x_pos = 720
                        eating_button_y_pos = 720
                elif item_frame6_x_pos < pygame.mouse.get_pos()[0] < item_frame6_x_pos + item_frame_width and item_frame_y_pos < pygame.mouse.get_pos()[1] < item_frame_y_pos + item_frame_height:
                    item_name = itemframe6_item
                    item_name_font = font.render('{}'.format(item_name), True, black)
                    explanation_font = font.render('{}'.format(itemframe6_explanation), True, black)
                    explanation2_font = font.render('{}'.format(itemframe6_explanation2), True, black)
                    if itemframe6_item == '':
                        item_count_font = font.render('', True, black)
                        synthesis_button_x_pos = 720
                        synthesis_button_y_pos = 720
                    else:
                        if cause == 'synthesis':
                            synthesis_button_x_pos = 305
                            synthesis_button_y_pos = 475
                        else:
                            synthesis_button_x_pos = 720
                            synthesis_button_y_pos = 720
                        item_count_font = font.render('{}개'.format(itemframe6_count), True, black)
                    if itemframe6_item == '민트초코' or itemframe6_item == '제육볶음' or itemframe6_item == '오징어다리':
                        if cause == 'battle':
                            eating_button_x_pos = 305
                            eating_button_y_pos = 475
                            eat_item_name = itemframe6_item
                    else:
                        eating_button_x_pos = 720
                        eating_button_y_pos = 720
                elif eating_button_x_pos < pygame.mouse.get_pos()[0] < eating_button_x_pos + eating_button_width and eating_button_y_pos < pygame.mouse.get_pos()[1] < eating_button_y_pos + eating_button_height:
                    print('먹기')
                    if eat_item_name == '제육볶음':
                        item_list['제육볶음'][0] -= 1
                        return '제육볶음'
                    elif eat_item_name == '민트초코':
                        print('민초')
                        item_list['민트초코'][0] -= 1
                        return '민트초코'
                    elif eat_item_name == '오징어다리':
                        item_list['오징어다리'][0] -= 1
                        return '오징어다리'
                elif synthesis_button_x_pos < pygame.mouse.get_pos()[0] < synthesis_button_x_pos + synthesis_button_width and synthesis_button_y_pos < pygame.mouse.get_pos()[1] < synthesis_button_y_pos + synthesis_button_height:
                    if item_name == '나뭇가지':
                        return_image = stick_image
                    elif item_name == '뼈':
                        return_image = bone_image
                    elif item_name == '민트초코':
                        return_image = mintchoco_image
                    elif item_name == '오징어다리':
                        return_image = squid_leg_image
                    elif item_name == '용의 머리':
                        return_image = dragon_head_image
                    elif item_name == '단조 설계도':
                        return_image = bluescreen_image
                    elif item_name == '제육볶음':
                        return_image = jeyookbokkem_image
                    elif item_name == '스크롤':
                        return_image = scroll_image
                    return [return_image, item_name]
                else:
                    item_name_font = font.render('', True, black)
                    explanation_font = font.render('', True, black)
                    explanation2_font = font.render('', True, black)
                    item_count_font = font.render('', True, black)
                    eating_button_x_pos = 720
                    eating_button_y_pos = 720
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print(pygame.mouse.get_pos())
        #게임 캐릭터 위치 정의

        #충돌처리

        #화면에 그리기
        screen.blit(background, (background_x_pos, background_y_pos))
        screen.blit(item_frame1, (item_frame1_x_pos, item_frame_y_pos))
        screen.blit(item_frame2, (item_frame2_x_pos, item_frame_y_pos))
        screen.blit(item_frame3, (item_frame3_x_pos, item_frame_y_pos))
        screen.blit(item_frame4, (item_frame4_x_pos, item_frame_y_pos))
        screen.blit(item_frame5, (item_frame5_x_pos, item_frame_y_pos))
        screen.blit(item_frame6, (item_frame6_x_pos, item_frame_y_pos))
        screen.blit(close_button, (close_button_x_pos, close_button_y_pos))
        screen.blit(stick_image, (stick_x_pos, stick_y_pos))
        screen.blit(bone_image, (bone_x_pos, bone_y_pos))
        screen.blit(mintchoco_image, (mintchoco_x_pos, mintchoco_y_pos))
        screen.blit(squid_leg_image, (squid_leg_x_pos, squid_leg_y_pos))
        screen.blit(dragon_head_image, (dragon_head_x_pos, dragon_head_y_pos))
        screen.blit(bluescreen_image, (bluescreen_x_pos, bluescreen_y_pos))
        screen.blit(scroll_image, (scroll_x_pos, scroll_y_pos))
        screen.blit(jeyookbokkem_image, (jeyookbokkem_x_pos, jeyookbokkem_y_pos))
        screen.blit(explanation_font, (115, 360))
        screen.blit(explanation2_font, (115, 380))
        screen.blit(item_name_font, (115, 310))
        screen.blit(item_count_font, (570, 310))
        screen.blit(eating_button, (eating_button_x_pos, eating_button_y_pos))
        screen.blit(synthesis_button, (synthesis_button_x_pos, synthesis_button_y_pos))
        pygame.display.update()
    
    if cause == 'synthesis':
        return [pygame.image.load('.\\resource\\텅비어있음.png'), '']
    return

def shop():
    global item_list
    global gold
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    background = pygame.image.load('.\\resource\\장소8.png')
    
    shop_menu = pygame.image.load('.\\resource\\shop.png')
    shop_menu_size = shop_menu.get_rect().size
    shop_menu_width = shop_menu_size[0]
    shop_menu_height = shop_menu_size[1]
    shop_menu_x_pos = screen_width / 2 - shop_menu_width / 2
    shop_menu_y_pos = screen_height / 2 - shop_menu_height / 2

    close_button = pygame.image.load('.\\resource\\X버튼.png')
    close_button_size = close_button.get_rect().size
    close_button_width = close_button_size[0]
    close_button_height = close_button_size[1]
    close_button_x_pos = shop_menu_x_pos + shop_menu_width - close_button_width
    close_button_y_pos = shop_menu_y_pos

    buy_button = pygame.image.load('.\\resource\\buy.png')
    buy_button_size = buy_button.get_rect().size
    buy_button_width = buy_button_size[0]
    buy_button_height = buy_button_size[1]
    buy_menu_button_x_pos = shop_menu_x_pos + 50
    buy_menu_button_y_pos = shop_menu_y_pos + 50 + 10
    buy_button_x_pos = 430
    buy_button_y_pos = 540

    sell_button = pygame.image.load('.\\resource\\sell.png')
    sell_button_size = sell_button.get_rect().size
    sell_button_width = sell_button_size[0]
    sell_button_height = sell_button_size[1]
    sell_menu_button_x_pos = buy_menu_button_x_pos
    sell_menu_button_y_pos = buy_menu_button_y_pos + buy_button_height + 10
    sell_button_x_pos = 430
    sell_button_y_pos = 540

    blueprint = pygame.image.load('.\\resource\\단조설계도.png')
    blueprint_size = blueprint.get_rect().size
    blueprint_width = blueprint_size[0]
    blueprint_height = blueprint_size[1]
    blueprint_x_pos = shop_menu_x_pos + 60
    blueprint_y_pos = shop_menu_y_pos + 168

    blueprint_image = pygame.image.load('.\\resource\\buy_item\\단조설계도.png')
    blueprint_image_x_pos = shop_menu_x_pos + 350
    blueprint_image_y_pos = shop_menu_y_pos + 168

    scroll = pygame.image.load('.\\resource\\스크롤.png')
    scroll_size = scroll.get_rect().size
    scroll_width = scroll_size[0]
    scroll_height = scroll_size[1]
    scroll_x_pos = blueprint_x_pos
    scroll_y_pos = blueprint_y_pos + blueprint_height

    scroll_image = pygame.image.load('.\\resource\\buy_item\\스크롤.png')
    scroll_image_x_pos = blueprint_image_x_pos
    scroll_image_y_pos = blueprint_image_y_pos

    bone = pygame.image.load('.\\resource\\뼈판매.png')
    bone_size = bone.get_rect().size
    bone_width = bone_size[0]
    bone_height = bone_size[1]
    bone_x_pos = blueprint_x_pos
    bone_y_pos = blueprint_y_pos

    bone_image = pygame.image.load('.\\resource\\buy_item\\뼈.png')
    bone_image_x_pos = shop_menu_x_pos + 350
    bone_image_y_pos = shop_menu_y_pos + 168

    dragon_head = pygame.image.load('.\\resource\\용의머리판매.png')
    dragon_size = dragon_head.get_rect().size
    dragon_width = dragon_size[0]
    dragon_height = dragon_size[1]
    dragon_x_pos = bone_x_pos
    dragon_y_pos = bone_y_pos + bone_height

    dragon_head_image = pygame.image.load('.\\resource\\buy_item\\용의 머리.png')
    dragon_head_image_x_pos = shop_menu_x_pos + 350
    dragon_head_image_y_pos = shop_menu_y_pos + 168

    jeyookbokkem = pygame.image.load('.\\resource\\제육볶음.png')
    jeyookbokkem_size = jeyookbokkem.get_rect().size
    jeyookbokkem_width = jeyookbokkem_size[0]
    jeyookbokkem_height = jeyookbokkem_size[1]
    jeyookbokkem_x_pos = blueprint_x_pos
    jeyookbokkem_y_pos = scroll_y_pos + scroll_height

    jeyookbokkem_image = pygame.image.load('.\\resource\\buy_item\\제육볶음.png')
    jeyookbokkem_image_x_pos = shop_menu_x_pos + 350
    jeyookbokkem_image_y_pos = shop_menu_y_pos + 168

    squid_leg = pygame.image.load('.\\resource\\오징어다리판매.png')
    squid_leg_size = squid_leg.get_rect().size
    squid_leg_width = squid_leg_size[0]
    squid_leg_height = squid_leg_size[1]
    squid_leg_x_pos = blueprint_x_pos
    squid_leg_y_pos = jeyookbokkem_y_pos

    squid_leg_image = pygame.image.load('.\\resource\\buy_item\\오징어다리.png')
    squid_leg_image_x_pos = shop_menu_x_pos + 350
    squid_leg_image_y_pos = shop_menu_y_pos + 168

    junji = pygame.image.load('.\\resource\\준지.png')
    junji_x_pos = shop_menu_x_pos + shop_menu_width - 50
    junji_y_pos = shop_menu_y_pos + shop_menu_height - 236

    item_button = pygame.image.load('.\\resource\\아이템.png')
    item_button_x_pos = 110
    item_button_y_pos = 70
    item_button_size = item_button.get_rect().size
    item_button_width = item_button_size[0]
    item_button_height = item_button_size[1]

    buy_or_sell = 'buy'

    now_buy = 'blueprint'

    #이벤트 루프
    running = True #게임이 진행중인가?

    while running:
        dt = clock.tick(60)

        #이벤트 처리
        for event in pygame.event.get(): #이벤트 수집
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button_x_pos < pygame.mouse.get_pos()[0] < close_button_x_pos + close_button_width and close_button_y_pos < pygame.mouse.get_pos()[1] < close_button_y_pos + close_button_height:
                    running = False
                if buy_menu_button_x_pos < pygame.mouse.get_pos()[0] < buy_menu_button_x_pos + buy_button_width and buy_menu_button_y_pos < pygame.mouse.get_pos()[1] < buy_menu_button_y_pos + buy_button_height:
                    buy_or_sell = 'buy'
                    now_buy = 'blueprint'
                elif sell_menu_button_x_pos < pygame.mouse.get_pos()[0] < sell_menu_button_x_pos + sell_button_width and sell_menu_button_y_pos < pygame.mouse.get_pos()[1] < sell_menu_button_y_pos + sell_button_height:
                    buy_or_sell = 'sell'
                    now_buy = '뼈'
                if item_button_x_pos < pygame.mouse.get_pos()[0] < item_button_x_pos + item_button_width and item_button_y_pos < pygame.mouse.get_pos()[1] < item_button_y_pos + item_button_height:
                    item()
                if buy_or_sell == 'buy':
                    if blueprint_x_pos < pygame.mouse.get_pos()[0] < blueprint_x_pos + blueprint_width and blueprint_y_pos < pygame.mouse.get_pos()[1] < blueprint_y_pos + blueprint_height:
                        now_buy = 'blueprint'
                    elif scroll_x_pos < pygame.mouse.get_pos()[0] < scroll_x_pos + scroll_width and scroll_y_pos < pygame.mouse.get_pos()[1] < scroll_y_pos + scroll_height:
                        now_buy = 'scroll'
                    elif jeyookbokkem_x_pos < pygame.mouse.get_pos()[0] < jeyookbokkem_x_pos + jeyookbokkem_width and jeyookbokkem_y_pos < pygame.mouse.get_pos()[1] < jeyookbokkem_y_pos + jeyookbokkem_height:
                        now_buy = 'jeyookbokkem'
                if buy_or_sell == 'sell':
                    if dragon_x_pos < pygame.mouse.get_pos()[0] < dragon_x_pos + dragon_width and dragon_y_pos < pygame.mouse.get_pos()[1] < dragon_y_pos + dragon_height:
                        now_buy = '용의 머리'
                    elif bone_x_pos < pygame.mouse.get_pos()[0] < bone_x_pos + bone_width and bone_y_pos < pygame.mouse.get_pos()[1] < bone_y_pos + bone_height:
                        now_buy = '뼈'
                    elif squid_leg_x_pos < pygame.mouse.get_pos()[0] < squid_leg_x_pos + squid_leg_width and squid_leg_y_pos < pygame.mouse.get_pos()[1] < squid_leg_y_pos + squid_leg_height:
                        now_buy = '오징어다리'
                if buy_button_x_pos < pygame.mouse.get_pos()[0] < buy_button_x_pos + buy_button_width and buy_button_y_pos < pygame.mouse.get_pos()[1] < buy_button_y_pos + buy_button_height:
                    if buy_or_sell == 'buy':
                        if gold - item_value >= 0:
                            gold -= item_value
                            item_list[item_name][0] += 1
                            pygame.mixer.Sound('.\\resource\\sound\\아이템구매음.wav').play()
                    elif buy_or_sell == 'sell':
                        if item_list[now_buy][0] > 0:
                            item_list[now_buy][0] -= 1
                            gold += item_value
                            pygame.mixer.Sound('.\\resource\\sound\\아이템판매음.wav').play()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print(pygame.mouse.get_pos())
                

        #게임 캐릭터 위치 정의
        if now_buy == 'blueprint':
            item_name = '단조 설계도'
            item_explanation = font.render('장비를 강화할 때', True, black)
            item_explanation2 = font.render('사용할 수 있는 설계도', True, black)
            item_value = 5
            item_price = font.render('{} gold'.format(item_value), True, (255, 255, 0))
        elif now_buy == '뼈':
            item_name = '뼈'
            item_explanation = font.render('동물의 마지막 형태.', True, black)
            item_explanation2 = font.render('예상보다 쓸 일이 많다.', True, black)
            item_value = 1
            item_price = font.render('{} gold'.format(item_value), True, (255, 255, 0))
        elif now_buy == '용의 머리':
            item_name = '용의 머리'
            item_explanation = font.render('용을 처치하고 얻은 머리.', True, black)
            item_explanation2 = font.render('꽤나 비싸게 팔릴 것이다.', True, black)
            item_value = 5
            item_price = font.render('{} gold'.format(item_value), True, (255, 255, 0))
        elif now_buy == 'scroll':
            item_name = '스크롤'
            item_explanation = font.render('깨달음을 얻기위해', True, black)
            item_explanation2 = font.render('다른 재료와 합성할 수 있다.', True, black)
            item_value = 5
            item_price = font.render('{} gold'.format(item_value), True, (255, 255, 0))
        elif now_buy == 'jeyookbokkem':
            item_name = '제육볶음'
            item_explanation = font.render('입맛을 돋구는 요리', True, black)
            item_explanation2 = font.render('체력을 회복할 수 있다.', True, black)
            item_value = 5
            item_price = font.render('{} gold'.format(item_value), True, (255, 255, 0))
        elif now_buy == '오징어다리':
            item_name = '오징어다리'
            item_explanation = font.render('질겅질겅 씹는 맛!', True, black)
            item_explanation2 = font.render('최고의 간식거리다.', True, black)
            item_value = 5
            item_price = font.render('{} gold'.format(item_value), True, (255, 255, 0))
        
        item_explanation_width = item_explanation.get_rect().size[0]
        item_explanation_height = item_explanation.get_rect().size[1]
        item_explanation2_width = item_explanation2.get_rect().size[0]
        item_explanation2_height = item_explanation2.get_rect().size[1]
        item_price_width = item_price.get_rect().size[0]

        #충돌처리

        #화면에 그리기
        screen.fill(white)
        screen.blit(shop_menu, (shop_menu_x_pos, shop_menu_y_pos))
        screen.blit(close_button, (close_button_x_pos, close_button_y_pos))
        screen.blit(buy_button, (buy_menu_button_x_pos, buy_menu_button_y_pos))
        screen.blit(sell_button, (sell_menu_button_x_pos, sell_menu_button_y_pos))
        screen.blit(junji, (junji_x_pos, junji_y_pos))
        screen.blit(render('보유금 : {} gold'.format(gold), font), (500, 200))
        screen.blit(item_button, (item_button_x_pos, item_button_y_pos))
        if buy_or_sell == 'buy':
            screen.blit(buy_button, (buy_button_x_pos, buy_button_y_pos))
            screen.blit(blueprint, (blueprint_x_pos, blueprint_y_pos))
            screen.blit(scroll, (scroll_x_pos, scroll_y_pos))
            screen.blit(jeyookbokkem, (jeyookbokkem_x_pos, jeyookbokkem_y_pos))
            if now_buy == 'blueprint':
                screen.blit(blueprint_image, (blueprint_image_x_pos, blueprint_image_y_pos))
            elif now_buy == 'scroll':
                screen.blit(scroll_image, (scroll_image_x_pos, scroll_image_y_pos))
            elif now_buy == 'jeyookbokkem':
                screen.blit(jeyookbokkem_image, (jeyookbokkem_image_x_pos, jeyookbokkem_image_y_pos))
        elif buy_or_sell == 'sell':
            screen.blit(sell_button, (sell_button_x_pos, sell_button_y_pos))
            screen.blit(bone, (bone_x_pos, bone_y_pos))
            screen.blit(dragon_head, (dragon_x_pos, dragon_y_pos))
            screen.blit(squid_leg, (squid_leg_x_pos, squid_leg_y_pos))
            if now_buy == '뼈':
                screen.blit(bone_image, (bone_image_x_pos, bone_image_y_pos))
            elif now_buy == '용의 머리':
                screen.blit(dragon_head_image, (dragon_head_image_x_pos, dragon_head_image_y_pos))
            elif now_buy == '오징어다리':
                screen.blit(squid_leg_image, (squid_leg_image_x_pos, squid_leg_image_y_pos))
        screen.blit(item_explanation, (405 + (200 / 2) - item_explanation_width / 2, 430))
        screen.blit(item_explanation2, (405 + (200 / 2) - item_explanation2_width / 2, 430 + item_explanation_height))
        screen.blit(render('{} gold'.format(item_value), font), (405 + (200 / 2) - item_price_width / 2, 430 + item_explanation_height + item_explanation2_height))
        pygame.display.update()
    
    return 0
            
def skill_guide():
    global my_skills
    global my_attack
    global my_defence
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    background = pygame.image.load('.\\resource\\스킬창.png')
    background_size = background.get_rect().size
    background_width = background_size[0]
    background_height = background_size[1]
    background_x_pos = screen_width / 2 - background_width / 2
    background_y_pos = screen_height / 2 - background_height / 2

    close_button = pygame.image.load('.\\resource\\X버튼.png')
    close_button_size = close_button.get_rect().size
    close_button_width = close_button_size[0]
    close_button_height = close_button_size[1]
    close_button_x_pos = background_x_pos + background_width - close_button_width
    close_button_y_pos = background_y_pos

    before = pygame.image.load('.\\resource\\이전버튼.png')
    before_size = before.get_rect().size
    before_width = before_size[0]
    before_height = before_size[1]
    before_x_pos = background_x_pos + 50
    before_y_pos = background_y_pos + background_height / 2 - before_height / 2

    after = pygame.image.load('.\\resource\\다음버튼.png')
    after_size = after.get_rect().size
    after_width = after_size[0]
    after_height = after_size[1]
    after_x_pos = background_x_pos + background_width - after_width - 50
    after_y_pos = background_y_pos + background_height / 2 - after_height / 2


    skills_kind = list(my_skills.keys()) # ['삼연속베기', '아프니까 방어올인']
    now_skill_guide = 0

    use_skill1 = pygame.image.load('.\\resource\\텅비어있음.png')
    use_skill2 = pygame.image.load('.\\resource\\텅비어있음.png')
    use_skill3 = pygame.image.load('.\\resource\\텅비어있음.png')

    skill_explanation = font.render('', True, black)
    skill_explanation2 = font.render('', True, black)
    skill_explanation3 = font.render('', True, black)
    skill_explanation4 = font.render('', True, black)

    #이벤트 루프
    running = True #게임이 진행중인가?

    while running:
        dt = clock.tick(60)




        #이벤트 처리
        for event in pygame.event.get(): #이벤트 수집
            if event.type == pygame.MOUSEBUTTONDOWN: #창이 닫히는 이벤트가 발생하였는가?
                if close_button_x_pos < pygame.mouse.get_pos()[0] < close_button_x_pos + close_button_width and close_button_y_pos < pygame.mouse.get_pos()[1] < close_button_y_pos + close_button_height:
                    pygame.mixer.Sound('.\\resource\\sound\\대화창다음으로.wav').play()
                    running = False #게임 실행 False
                if before_x_pos < pygame.mouse.get_pos()[0] < before_x_pos + before_width and before_y_pos < pygame.mouse.get_pos()[1] < before_y_pos + before_height:
                    if now_skill_guide > 0:
                        now_skill_guide -= 1
                if after_x_pos < pygame.mouse.get_pos()[0] < after_x_pos + after_width and after_y_pos < pygame.mouse.get_pos()[1] < after_y_pos + after_height:
                    if now_skill_guide < len(skills_kind) - 1:
                        now_skill_guide += 1

                    

        #게임 캐릭터 위치 정의
        skill_name = skills_kind[now_skill_guide]
        skill_use_way = my_skills[skill_name][0]
        skill_name_font = font.render('{}.level {}'.format(skill_name, my_skills[skill_name][1]), True, black)
        skill_name_size = skill_name_font.get_rect().size
        skill_name_width = skill_name_size[0]
        skill_name_height = skill_name_size[1]

        #충돌처리

        if skill_name == '삼연속베기':
            skill_explanation = font.render('검을 세번 휘둘러 벤다.', True, black)
            skill_explanation2 = font.render('적에게 {} + 스킬 레벨 피해를 입힌다.'.format((my_attack - 1) * 2 + my_attack), True, black)
            skill_explanation3 = font.render('5레벨 이후로는 데미지가 늘어나지 않는다.', True, black)
            skill_explanation4 = font.render('', True, black)
        elif skill_name == '텟카이':
            skill_explanation = font.render('절대 뚫리지 않을 기세로 방어에만 집중한다.', True, black)
            skill_explanation2 = font.render('{} + 스킬 레벨만큼의 방어력을 얻는다.'.format((my_defence - 1) * 2 + my_defence), True, black)
            skill_explanation3 = font.render('5레벨 이후로는 방어력이 늘어나지 않는다.', True, black)
            skill_explanation4 = font.render('', True, black)
        elif skill_name == '실명다트':
            skill_explanation = font.render('적에게 실명 다트를 던져 {}데미지를 입히고'.format(my_attack + my_skills['실명다트'][1]), True, black)
            skill_explanation2 = font.render('다음 3턴동안 기본 공격 데미지를 받지 않는다.', True, black)
            skill_explanation3 = font.render('', True, black)
            skill_explanation4 = font.render('', True, black)
        elif skill_name == '신의 가호':
            skill_explanation = font.render('신의 가호를 받아 이단에게 심판을 내리는 힘을 받는다.', True, black)
            skill_explanation2 = font.render('또한, 공격 할 때마다 지속시간을 줄이고 1데미지를 입힌다.', True, black)
            skill_explanation3 = font.render('', True, black)
            skill_explanation4 = font.render('', True, black)
        elif skill_name == '화염 방사':
            skill_explanation = font.render('상대의 방어도만큼 화상효과를 부여한다. ', True, black)
            skill_explanation2 = font.render('화상 : 스킬사용시 지속시간만큼의 데미지를 입힌다.', True, black)
            skill_explanation3 = font.render('{} 이상의 지속시간을 가지면 두 배로 피해를 입힌다.'.format(6 - my_skills['화염 방사'][1]), True, black)
            skill_explanation4 = font.render('상대가 스킬을 사용하면 이 효과는 사라진다.', True, black)
        elif skill_name == '화내기':
            skill_explanation = font.render('흥분 상태를 얻는다. 이 버프는 다른 버프로', True, black)
            skill_explanation2 = font.render('덮어씨우지 않는 이상 전투 끝까지 지속된다.', True, black)
            skill_explanation3 = font.render('흥분 : 받는 피해 2배 증가, 주는 피해 2배 증가.', True, black)
            skill_explanation4 = font.render('단, 디버프로 인한 피해는 제외한다.', True, black)
        elif skill_name == '우마이':
            skill_explanation = font.render('체력을 10 회복하고 식중독 디버프를 1 얻는다.', True, black)
            skill_explanation2 = font.render('식중독 : 지속시간이 끝나면 체력을 {} 잃는다.'.format(10 - my_skills['우마이'][1]), True, black)
            skill_explanation3 = font.render('', True, black)
            skill_explanation4 = font.render('', True, black)
        elif skill_name == '피의 결계':
            skill_explanation = font.render('{}hp를 잃고 피의 결계 상태를 1 얻는다.'.format(16 - my_skills['피의 결계'][1]), True, black)
            skill_explanation2 = font.render('피의 결계 : 이번 턴동안 받는 모든 데미지를 무시한다.', True, black)
            skill_explanation3 = font.render('이 스킬은 연속해서 쓸 수 없다.', True, black)
            skill_explanation4 = font.render('', True, black)
        elif skill_name == '흡수':
            skill_explanation = font.render('{}만큼의 고정피해를 주고 그만큼 체력을 회복한다.'.format(my_skills['흡수'][1]), True, black)
            skill_explanation2 = font.render('체력이 절반 이하라면 추가로 {}% 더 회복한다.'.format(my_skills['흡수'][1] * 10), True, black)
            skill_explanation3 = font.render('', True, black)
            skill_explanation4 = font.render('', True, black)

        if skill_use_way[0] == 'attack':
            use_skill1 = pygame.image.load('.\\resource\\공격코스트.png')
        elif skill_use_way[0] == 'gard':
            use_skill1 = pygame.image.load('.\\resource\\방어코스트.png')
        elif skill_use_way[0] == 'concentration':
            use_skill1 = pygame.image.load('.\\resource\\집중코스트.png')

        if skill_use_way[1] == 'attack':
            use_skill2 = pygame.image.load('.\\resource\\공격코스트.png')
        elif skill_use_way[1] == 'gard':
            use_skill2 = pygame.image.load('.\\resource\\방어코스트.png')
        elif skill_use_way[1] == 'concentration':
            use_skill2 = pygame.image.load('.\\resource\\집중코스트.png')

        if skill_use_way[2] == 'attack':
            use_skill3 = pygame.image.load('.\\resource\\공격코스트.png')
        elif skill_use_way[2] == 'gard':
            use_skill3 = pygame.image.load('.\\resource\\방어코스트.png')
        elif skill_use_way[2] == 'concentration':
            use_skill3 = pygame.image.load('.\\resource\\집중코스트.png')
    
        skill_explanation_size = skill_explanation.get_rect().size
        skill_explanation_width = skill_explanation_size[0]
        skill_explanation_height = skill_explanation_size[1]
        skill_explanation2_size = skill_explanation2.get_rect().size
        skill_explanation2_width = skill_explanation2_size[0]
        skill_explanation2_height = skill_explanation2_size[1]
        skill_explanation_x_pos = background_x_pos + background_width / 2 - skill_explanation_width / 2
        skill_explanation_y_pos = 380
        skill_explanation2_x_pos = background_x_pos + background_width / 2 - skill_explanation2_width / 2
        skill_explanation2_y_pos = skill_explanation_y_pos + skill_explanation2_height
        skill_explanation3_size = skill_explanation3.get_rect().size
        skill_explanation3_width = skill_explanation3_size[0]
        skill_explanation3_height = skill_explanation3_size[1]
        skill_explanation4_size = skill_explanation4.get_rect().size
        skill_explanation4_width = skill_explanation4_size[0]
        skill_explanation4_height = skill_explanation4_size[1]
        skill_explanation3_x_pos = background_x_pos + background_width / 2 - skill_explanation3_width / 2
        skill_explanation3_y_pos = skill_explanation2_y_pos + skill_explanation3_height
        skill_explanation4_x_pos = background_x_pos + background_width / 2 - skill_explanation4_width / 2
        skill_explanation4_y_pos = skill_explanation3_y_pos + skill_explanation4_height
        


        #화면에 그리기
        screen.blit(background, (background_x_pos, background_y_pos))
        screen.blit(close_button, (close_button_x_pos, close_button_y_pos))
        screen.blit(before, (before_x_pos, before_y_pos))
        screen.blit(after, (after_x_pos , after_y_pos))
        screen.blit(skill_explanation, (skill_explanation_x_pos, skill_explanation_y_pos))
        screen.blit(skill_explanation2, (skill_explanation2_x_pos, skill_explanation2_y_pos))
        screen.blit(skill_explanation3, (skill_explanation3_x_pos, skill_explanation3_y_pos))
        screen.blit(skill_explanation4, (skill_explanation4_x_pos, skill_explanation4_y_pos))
        screen.blit(skill_name_font, (background_x_pos + background_width / 2 - skill_name_width / 2, background_y_pos + 220))
        screen.blit(use_skill1, (240, 530))
        screen.blit(use_skill2, (340, 530))
        screen.blit(use_skill3, (440, 530))
        pygame.display.update()
    
    return

def synthesis():
    global items
    global item_list
    global button_sound
    global my_skills
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    background = pygame.image.load('.\\resource\\현우.png')
    background_x_pos = 50
    background_y_pos = 50

    synthesis_menu = pygame.image.load('.\\resource\\합성창.png')
    synthesis_menu_size = synthesis_menu.get_rect().size
    synthesis_menu_width = synthesis_menu_size[0]
    synthesis_menu_height = synthesis_menu_size[1]
    synthesis_menu_x_pos = screen_width / 2 - synthesis_menu_width / 2
    synthesis_menu_y_pos = screen_height / 2 - synthesis_menu_height / 2

    synthesis_button = pygame.image.load('.\\resource\\합성.png')
    synthesis_button_x_pos = 350
    synthesis_button_y_pos = 500
    synthesis_button_size = synthesis_button.get_rect().size
    synthesis_button_width = synthesis_button_size[0]
    synthesis_button_height = synthesis_button_size[1]

    close_button = pygame.image.load('.\\resource\\X버튼.png')
    close_button_size = close_button.get_rect().size
    close_button_width = close_button_size[0]
    close_button_height = close_button_size[1]
    close_button_x_pos = synthesis_menu_x_pos + synthesis_menu_width - close_button_width
    close_button_y_pos = synthesis_menu_y_pos

    item_button = pygame.image.load('.\\resource\\아이템.png')
    item_button_x_pos = 110
    item_button_y_pos = 70
    item_button_size = item_button.get_rect().size
    item_button_width = item_button_size[0]
    item_button_height = item_button_size[1]

    ingredient = [pygame.image.load('.\\resource\\텅비어있음.png'), '']
    ingredient_x_pos = synthesis_menu_x_pos + 430
    ingredient_y_pos = synthesis_menu_y_pos + 229

    #이벤트 루프
    running = True #게임이 진행중인가?

    while running:
        dt = clock.tick(60)

        #이벤트 처리
        for event in pygame.event.get(): #이벤트 수집
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button_x_pos < pygame.mouse.get_pos()[0] < close_button_x_pos + close_button_width and close_button_y_pos < pygame.mouse.get_pos()[1] < close_button_y_pos + close_button_height:
                    pygame.mixer.Sound('.\\resource\\sound\\대화창다음으로.wav').play()
                    running = False #함수 실행 False
                elif item_button_x_pos < pygame.mouse.get_pos()[0] < item_button_x_pos + item_button_width and item_button_y_pos < pygame.mouse.get_pos()[1] < item_button_y_pos + item_button_height:
                    ingredient = item('synthesis') #ingredient는 리스트 형으로 0번은 사진 1번은 아이템 이름
                elif synthesis_button_x_pos < pygame.mouse.get_pos()[0] < synthesis_button_x_pos + synthesis_button_width and synthesis_button_y_pos < pygame.mouse.get_pos()[1] < synthesis_button_y_pos + synthesis_button_height:
                    if item_list[ingredient[1]][0] > 0 and item_list['스크롤'][0] > 0:
                        item_list[ingredient[1]][0] -= 1
                        item_list['스크롤'][0] -= 1
                        ingredient = [pygame.image.load('.\\resource\\텅비어있음.png'), '']
                        if ingredient[1] == '뼈':
                            if random.randint(1, 2) == 1: #특성뽑 성공
                                get_skill = random.choice(['삼연속베기', '텟카이'])
                                if get_skill in my_skills:
                                    my_skills[get_skill][1] += 1
                            else: #실패시 원래 있던 스킬중 하나를 레벨 업
                                get_skill = random.choice(my_skills)
                                my_skills[get_skill][1] += 1
                        elif ingredient[1] == '용의 머리':
                            if random.randint(1, 2) == 1:
                                get_skill = random.choice(['화염 방사'])
                                if get_skill in my_skills:
                                    my_skills[get_skill][1] += 1
                                elif get_skill == '화염 방사':
                                    my_skills[get_skill] = [('concentration', 'attack', 'concentration'), 1]
                            else:
                                get_skill = random.choice(my_skills)
                                my_skills[get_skill][1] += 1
                        elif ingredient[1] == '단조 설계도':
                            if random.randint(1, 2) == 1:
                                get_skill = random.choice(['화내기', '피의 결계'])
                                if get_skill in my_skills:
                                    my_skills[get_skill][1] += 1
                                elif get_skill == '화내기':
                                    my_skills[get_skill] = [('gard', 'gard', 'concentration'), 1]
                                elif get_skill == '피의 결계':
                                    my_skills[get_skill] = [('concentration', 'concentration', 'concentration'), 1]
                            else:
                                get_skill = random.choice(my_skills)
                                my_skills[get_skill][1] += 1
                        elif ingredient[1] == '민트초코' or ingredient[1] == '오징어다리' or ingredient[1] == '제육볶음':
                            if random.randint(1, 2) == 1:
                                get_skill = random.choice(['우마이', '흡수'])
                                if get_skill in my_skills:
                                    my_skills[get_skill][1] += 1
                                elif get_skill == '우마이':
                                    my_skills[get_skill] = [('attack', 'concentration', 'gard'), 1]
                                elif get_skill == '흡수':
                                    my_skills[get_skill] = [('gard', 'concentration', 'concentration'), 1]
                            else:
                                get_skill = random.choice(my_skills)
                                my_skills[get_skill][1] += 1 





        #게임 캐릭터 위치 정의

        #충돌처리

        #화면에 그리기
        screen.blit(background, (background_x_pos, background_y_pos))
        screen.blit(synthesis_menu, (synthesis_menu_x_pos, synthesis_menu_y_pos))
        screen.blit(close_button, (close_button_x_pos, close_button_y_pos))
        screen.blit(item_button, (item_button_x_pos, item_button_y_pos))
        screen.blit(synthesis_button, (synthesis_button_x_pos, synthesis_button_y_pos))
        screen.blit(ingredient[0], (ingredient_x_pos, ingredient_y_pos))
        pygame.display.update()



def game(save):
    global button_sound
    global items
    global conversation_check
    global item_list
    global my_skills
    global weapons
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    gameui = pygame.image.load('.\\resource\\게임UI.png')
    gameui_x_pos = 0
    gameui_y_pos = 0


    sun = pygame.image.load('.\\resource\\선이.png')
    sun_size = sun.get_rect().size
    sun_width = sun_size[0]
    sun_height = sun_size[1]
    now_sun_x_pos = 370
    now_sun_y_pos = 180
    to_x = 0
    to_y = 0

    jammin = pygame.image.load('.\\resource\\샌즈.png')
    jammin_x_pos = 120
    jammin_y_pos = 400

    house = pygame.image.load('.\\resource\\집.png')
    house_size = house.get_rect().size
    house_width =house_size[0]
    house_height = house_size[1]
    house_x_pos = 650 / 2 - house_width / 2 + 70
    house_y_pos = 70

    tree1 = pygame.image.load('.\\resource\\나무1.png')
    tree1_x_pos = 100
    tree1_y_pos = 600

    sign = pygame.image.load('.\\resource\\표지판.png')
    sign_size = sign.get_rect().size
    sign_width = sign_size[0]
    sign_height = sign_size[1]

    fairy = pygame.image.load('.\\resource\\지도용요정.png')
    fairy_size = fairy.get_rect().size
    fairy_width = fairy_size[0]
    fairy_height = fairy_size[1]
    fairy_x_pos = 145
    fairy_y_pos = 210

    cockroach = pygame.image.load('.\\resource\\바퀴.png')
    cockroach_size = cockroach.get_rect().size
    cockroach_width = cockroach_size[0]
    cockroach_height = cockroach_size[1]
    cockroach_x_pos = 380
    cockroach_y_pos = 530

    warning = pygame.image.load('.\\resource\\텅비어있음.png')
    warning_x_pos = 650
    warning_y_pos = 5

    church = pygame.image.load('.\\resource\\교회.png')
    church_x_pos = 190
    church_y_pos = -130

    smithy = pygame.image.load('.\\resource\\대장간.png')
    smithy_x_pos = 220
    smithy_y_pos = 180

    junhyeok = pygame.image.load('.\\resource\\지도용일라오이.png')
    junhyeok_x_pos = 370
    junhyeok_y_pos = 220

    reddragon = pygame.image.load('.\\resource\\지도용홍룡.png')
    reddragon_x_pos = 260
    reddragon_y_pos = 70

    junji = pygame.image.load('.\\resource\\준지.png')
    junji_x_pos = 220
    junji_y_pos = 180

    office = pygame.image.load('.\\resource\\사무실.png')
    office_x_pos = 450
    office_y_pos = 180

    tower = pygame.image.load('.\\resource\\마탑.png')
    tower_x_pos = 70 + 50
    tower_y_pos = 70 + 50

    door1 = pygame.image.load('.\\resource\\door.png')
    door1_size = door1.get_rect().size
    door1_width = door1_size[0]
    door1_height = door1_size[1]
    door1_x_pos = 70
    
    door2 = pygame.image.load('.\\resource\\door.png')
    door2_size = door2.get_rect().size
    door2_width = door2_size[0]
    door2_height = door2_size[1]
    door2_x_pos = 70 + 265
    
    door3 = pygame.image.load('.\\resource\\door.png')
    door3_size = door3.get_rect().size
    door3_width = door3_size[0]
    door3_height = door3_size[1]
    door3_x_pos = 70 + 530

    door_y_pos = 205 + 70

    interaction = font.render('', True, black)

    place1 = pygame.image.load('.\\resource\\장소1.png')
    place2 = pygame.image.load('.\\resource\\장소2(나무).png')
    place3 = pygame.image.load('.\\resource\\장소3.png')
    place4 = pygame.image.load('.\\resource\\장소4.png')
    place5 = pygame.image.load('.\\resource\\장소1.png')
    place6 = pygame.image.load('.\\resource\\장소6.png')
    place7 = pygame.image.load('.\\resource\\장소7.png')
    place8 = pygame.image.load('.\\resource\\장소1.png')
    place9 = pygame.image.load('.\\resource\\장소8.png')
    place10 = pygame.image.load('.\\resource\\탑1층.png')
    place11 = pygame.image.load('.\\resource\\탑2층.jpg')
    place12 = pygame.image.load('.\\resource\\탑3층.png')


    if save == 0:
        pass ##########세이브 된게 없을경우 설정할 기본 변수
        conversation('tutorial', 1)
        nowplace = place1
        item_list = {
    '나뭇가지' : [0, '나무에서 떨어진 나뭇가지.', '금방이라도 부러질 듯하여 무기로는 쓸 수 없다.'],
    '뼈' : [0, '잼민이와의 결투에서 승리하고 얻은 전리품.', '누구의 뼈인지는 알 수 없다.'],
    '민트초코' : [0, '왠지 모르겠지만 바퀴벌레가 들고있던 민트초코.', '어디서 얻은것인지는 알 수 없다.'],
    '오징어다리' : [0, '깨달음의 보상으로 얻어낸 아이템.', '씹으면 질겅질겅하다.'],
    '용의 머리' : [0, '용을 쓰러트리고 얻어낸 아이템.', '귀한 약재로 쓰여 매우 비싸다.'],
    '단조 설계도' : [0, '장비를 강화할 때 사용할 수 있는 설계도.','상점에서만 구할 수 있다.'],
    '제육볶음' : [0, '최고의 일식요리사 준스케가 만든 제육볶음.', '체력을 회복하는데 좋다.'],
    '스크롤' : [0, '깨달음을 얻기 위해 필요한 기초 재료', '사무실에서 사용할 수 있다.']
}
        conversation_check = {
            'teemo' : 0,
            'sign' : 0,
            'youknow' : 0,
            'winline' : 0,
            'hyunwoo' : 0,
            'sun' : 0
}
        weapons = {
            'sword' : common_sword,
            'shield' : common_shield,
            'healthy' : common_healthy
        }

        my_skills = {
            '삼연속베기' : [('attack', 'attack', 'attack'), 1],
            '텟카이' : [('gard', 'gard', 'gard'), 1]
        }
    elif save == 1:
        pass ##########세이브 된게 있을경우 설정할 기본 변수(파일 읽어오기)

    #이벤트 루프
    running = True #게임이 진행중인가?

    while running:
        dt = clock.tick(60)

        #이벤트 처리
        for event in pygame.event.get(): #이벤트 수집
            if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
                pygame.quit()
                sys.exit()


        #게임 캐릭터 위치 정의
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: #########################################개발 완료후 지울 코드
                    print('{}, {}'.format(now_sun_x_pos, now_sun_y_pos))
                
                if event.key == pygame.K_w:
                    to_y = -10
                if event.key == pygame.K_s:
                    to_y = 10
                if event.key == pygame.K_a:
                    to_x = -10
                if event.key == pygame.K_d:
                    to_x = 10
                if event.key == pygame.K_f:
                    if cause == '전투':
                        victory = battle(enemy)
                        if victory == 0:
                            return 'death'
                        if victory == 1:
                            if enemy == 'jammin':
                                item_list['뼈'][0] += 1
                            elif enemy == 'cockroach':
                                item_list['민트초코'][0] += 1
                            elif enemy == 'reddragon':
                                item_list['용의 머리'][0] += 1
                    elif cause == '채집':
                        pygame.mixer.Sound('.\\resource\\sound\\나무캐는소리.wav').play()
                        item_list['나뭇가지'][0] += 1
                    elif cause == '왼쪽 길로 이동':
                        if nowplace == place1:
                            nowplace = place2
                        elif nowplace == place3:
                            nowplace = place1
                        elif nowplace == place5:
                            nowplace = place3
                        elif nowplace == place6:
                            nowplace = place5
                        elif nowplace == place8:
                            nowplace = place6
                        elif nowplace == place9:
                            nowplace = place8
                        now_sun_x_pos = screen_width - sun_width
                    elif cause == '오른쪽 길로 이동':
                        if nowplace == place2:
                            nowplace = place1
                        elif nowplace == place1:
                            nowplace = place3
                        elif nowplace == place3:
                            nowplace = place5
                        elif nowplace == place5:
                            nowplace = place6
                        elif nowplace == place6:
                            nowplace = place8
                        elif nowplace == place8:
                            nowplace = place9
                        now_sun_x_pos = 70
                    elif cause == '위쪽 길로 이동':
                        if nowplace == place3:
                            nowplace = place4
                        if nowplace == place6:
                            nowplace = place7
                        now_sun_y_pos = 720
                    elif cause == '아래쪽 길로 이동':
                        if nowplace == place4:
                            nowplace = place3
                        if nowplace == place7:
                            nowplace = place6
                        now_sun_y_pos = 70
                    elif cause == '읽기':
                        conversation('sign', conversation_check['sign'])
                    elif cause == '대화':
                        if partner == 'teemo':
                            conversation_check['teemo'] += 1
                            conversation(partner, conversation_check['teemo'])
                        elif partner == 'winline':
                            conversation(partner, conversation_check['winline'])
                        elif partner == 'junhyeok':
                            conversation(partner, conversation_check['junhyeok'])
                            victory = battle(enemy)
                            if victory == 0:
                                return 'death'
                            if victory == 1:
                                if enemy == 'junhyeok':
                                    conversation(partner, 2)
                                    item_list['오징어다리'][0] += 1
                        elif partner == 'junji':
                            conversation(partner, conversation_check['junji'])
                    elif cause == '진입':
                        if partner == 'youknow':
                            conversation_check['youknow'] += 1
                            conversation('youknow', conversation_check['youknow'])
                        elif partner == 'hyunwoo':
                            conversation('hyunwoo', conversation_check['hyunwoo'])
                        elif partner == '독백':
                            conversation('독백', conversation_check['sun'])
                            nowplace = place10
                        elif partner == 'blackcow':
                            conversation('blackcow', 1)
                            victory = battle('blackcow')
                            if victory == 0:
                                return 'death'
                            else:
                                conversation('ending', 1)
                                return 'chainsaw'
                        elif partner == 'oji':
                            conversation('ojimin', 1)
                            victory = battle('ojimin')
                            if victory == 0:
                                return 'death'
                            else:
                                conversation('ending', 2)
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if items_x_pos < pygame.mouse.get_pos()[0] < items_x_pos + items_width and items_y_pos < pygame.mouse.get_pos()[1] < items_y_pos + items_height:
                    button_sound.play()
                    item()
                elif skills_x_pos < pygame.mouse.get_pos()[0] < skills_x_pos + skills_width and skills_y_pos < pygame.mouse.get_pos()[1] < skills_y_pos + skills_height:
                    button_sound.play()
                    skill_guide()
                        



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    to_y = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    to_x = 0

        now_sun_x_pos += to_x
        now_sun_y_pos += to_y
        if now_sun_y_pos < 70:
            now_sun_y_pos = 70
        elif now_sun_y_pos > screen_height - sun_height:
            now_sun_y_pos = screen_height - sun_height
        
        if now_sun_x_pos < 70:
            now_sun_x_pos = 70
        elif now_sun_x_pos > screen_width - sun_width:
            now_sun_x_pos = screen_width - sun_width



        sun_rect = sun.get_rect()
        sun_rect.left = now_sun_x_pos
        sun_rect.top = now_sun_y_pos
        jammin_rect = jammin.get_rect()
        jammin_rect.left = jammin_x_pos
        jammin_rect.top = jammin_y_pos
        tree1_rect = tree1.get_rect()
        tree1_rect.left = tree1_x_pos
        tree1_rect.top = tree1_y_pos
        sign_rect = sign.get_rect()
        sign_rect.left = 220
        sign_rect.top = 420
        fairy_rect = fairy.get_rect()
        fairy_rect.left = fairy_x_pos
        fairy_rect.top = fairy_y_pos
        cockroach_rect = cockroach.get_rect()
        cockroach_rect.left = cockroach_x_pos
        cockroach_rect.top = cockroach_y_pos
        church_rect = church.get_rect()
        church_rect.left = church_x_pos
        church_rect.top = church_y_pos
        smithy_rect = smithy.get_rect()
        smithy_rect.left = smithy_x_pos
        smithy_rect.top = smithy_y_pos
        junhyeok_rect = junhyeok.get_rect()
        junhyeok_rect.left = junhyeok_x_pos
        junhyeok_rect.top = junhyeok_y_pos
        reddragon_rect = reddragon.get_rect()
        reddragon_rect.left = reddragon_x_pos
        reddragon_rect.top = reddragon_y_pos
        junji_rect = junji.get_rect()
        junji_rect.left = junji_x_pos
        junji_rect.top = junji_y_pos
        office_rect = office.get_rect()
        office_rect.left = office_x_pos
        office_rect.top = office_y_pos
        tower_rect = tower.get_rect()
        tower_rect.left = tower_x_pos
        tower_rect.top = tower_y_pos
        door1_rect = door1.get_rect()
        door1_rect.left = door1_x_pos
        door1_rect.top = door_y_pos
        door2_rect = door2.get_rect()
        door2_rect.left = door2_x_pos
        door2_rect.top = door_y_pos
        door3_rect = door3.get_rect()
        door3_rect.left = door3_x_pos
        door3_rect.top = door_y_pos

        #충돌처리


        if nowplace == place1:
            if sun_rect.colliderect(jammin_rect): ######################################잼민이와 부딫힘
                warning = pygame.image.load('.\\resource\\주의.png')
                cause = '전투'
                enemy = 'jammin'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 70 and 450 <= now_sun_y_pos <= 560:
                cause = '왼쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 675 and 450 <= now_sun_y_pos <= 560:
                cause = '오른쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black) 
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
                conversation_check['sign'] = 0
        if nowplace == place2:
            if sun_rect.colliderect(tree1_rect):
                warning = pygame.image.load('.\\resource\\주의.png')
                cause = '채집'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif sun_rect.colliderect(fairy_rect):
                cause = '대화'
                partner = 'teemo'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 675 and 450 <= now_sun_y_pos <= 560:
                cause = '오른쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black) 
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
                conversation_check['sign'] = 0
        if nowplace == place3:
            if sun_rect.colliderect(sign_rect):
                cause = '읽기'
                conversation_check['sign'] = 1
                interaction = font.render('F|{}'.format(cause), True, black)
            elif sun_rect.colliderect(cockroach_rect):
                cause = '전투'
                enemy = 'cockroach'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 70 and 450 <= now_sun_y_pos <= 560:
                cause = '왼쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 675 and 450 <= now_sun_y_pos <= 560:
                cause = '오른쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_y_pos == 70 and 290 <= now_sun_x_pos <= 450:
                cause = '위쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
                conversation_check['sign'] = 0
        if nowplace == place4:
            if sun_rect.colliderect(church_rect):
                cause = '진입'
                partner = 'youknow'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_y_pos == 620 and 310 <= now_sun_x_pos <= 480:
                cause = '아래쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
                conversation_check['sign'] = 0
        if nowplace == place5:
            if sun_rect.colliderect(smithy_rect):
                cause = '대화'
                partner = 'winline'
                conversation_check['winline'] = 1
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 70 and 450 <= now_sun_y_pos <= 560:
                cause = '왼쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 675 and 450 <= now_sun_y_pos <= 560:
                cause = '오른쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black) 
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
                conversation_check['sign'] = 0
        if nowplace == place6:
            if sun_rect.colliderect(junhyeok_rect):
                cause = '대화'
                partner = 'junhyeok'
                enemy = 'junhyeok'
                conversation_check['junhyeok'] = 1
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 70 and 450 <= now_sun_y_pos <= 560:
                cause = '왼쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 675 and 450 <= now_sun_y_pos <= 560:
                cause = '오른쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_y_pos == 70 and 290 <= now_sun_x_pos <= 450:
                cause = '위쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
        if nowplace == place7:
            if sun_rect.colliderect(reddragon_rect):
                cause = '전투'
                enemy = 'reddragon'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_y_pos == 620 and 290 <= now_sun_x_pos <= 450:
                cause = '아래쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
        if nowplace == place8:
            if sun_rect.colliderect(junji_rect):
                cause = '대화'
                partner = 'junji'
                conversation_check['junji'] = 1
                interaction = font.render('F|{}'.format(cause), True, black)
            elif sun_rect.colliderect(office_rect):
                cause = '진입'
                partner = 'hyunwoo'
                conversation_check['hyunwoo'] = 1
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 70 and 450 <= now_sun_y_pos <= 560:
                cause = '왼쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 675 and 450 <= now_sun_y_pos <= 560:
                cause = '오른쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
        if nowplace == place9:
            if sun_rect.colliderect(tower_rect):
                cause = '진입'
                partner = '독백'
                conversation_check['sun'] = 1
                interaction = font.render('F|{}'.format(cause), True, black)
            elif now_sun_x_pos == 70 and 450 <= now_sun_y_pos <= 560:
                cause = '왼쪽 길로 이동'
                interaction = font.render('F|{}'.format(cause), True, black)
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
        if nowplace == place10:
            warning = pygame.image.load('.\\resource\\텅비어있음.png')
            cause = ''
            interaction = font.render('', True, black)
            conversation('독백', conversation_check['sun'] + 1)
            victory = battle('sunghyun')
            if victory == 0:
                return 'death'
            conversation_check['sun'] = 3
            conversation('독백', conversation_check['sun'])
            nowplace = place11
        if nowplace == place11:
            warning = pygame.image.load('.\\resource\\텅비어있음.png')
            cause = ''
            interaction = font.render('', True, black)
            conversation_check['sun'] = 3
            conversation('minyoung', 1)
            victory = battle('minyoung')
            if victory == 0:
                return 'death'
            nowplace = place12
        if nowplace == place12:
            if sun_rect.colliderect(door1_rect):
                cause = '진입'
                partner = 'blackcow'
            elif sun_rect.colliderect(door2_rect):
                cause = '진입'
                partner = 'shaco'
            elif sun_rect.colliderect(door3_rect):
                cause = '진입'
                partner = 'oji'
            else:
                warning = pygame.image.load('.\\resource\\텅비어있음.png')
                cause = ''
                interaction = font.render('', True, black)
        
        interaction_x_pos = now_sun_x_pos + 10
        interaction_y_pos = now_sun_y_pos - 15
        interaction_size = interaction.get_rect().size
        interaction_width = interaction_size[0]
        interaction_height = interaction_size[1]
        if interaction_x_pos + interaction_width > 720:
            interaction_x_pos = now_sun_x_pos - interaction_width + 10

        #화면에 그리기
        screen.fill(white)
        screen.blit(nowplace, (70, 70))
        if nowplace == place1:
            screen.blit(house, (house_x_pos, house_y_pos))
            screen.blit(jammin, (jammin_x_pos, jammin_y_pos))
        elif nowplace == place2:
            screen.blit(tree1, (tree1_x_pos, tree1_y_pos))
            screen.blit(fairy, (fairy_x_pos, fairy_y_pos))
        elif nowplace == place3:
            screen.blit(sign, (220, 420))
            screen.blit(cockroach, (cockroach_x_pos, cockroach_y_pos))
        elif nowplace == place4:
            screen.blit(church, (church_x_pos, church_y_pos))
        elif nowplace == place5:
            screen.blit(smithy, (smithy_x_pos, smithy_y_pos))
        elif nowplace == place6:
            screen.blit(junhyeok, (junhyeok_x_pos, junhyeok_y_pos))
        elif nowplace == place7:
            screen.blit(reddragon, (reddragon_x_pos, reddragon_y_pos))
        elif nowplace == place8:
            screen.blit(junji, (junji_x_pos, junji_y_pos))
            screen.blit(office, (office_x_pos, office_y_pos))
        elif nowplace == place9:
            screen.blit(tower, (tower_x_pos, tower_y_pos))
        elif nowplace == place12:
            screen.blit(door1, (door1_x_pos, door_y_pos))
            screen.blit(door2, (door2_x_pos, door_y_pos))
            screen.blit(door3, (door3_x_pos, door_y_pos))
        screen.blit(gameui, (gameui_x_pos, gameui_y_pos))
        screen.blit(items, (items_x_pos, items_y_pos))
        screen.blit(skills, (skills_x_pos , skills_y_pos))
        screen.blit(warning, (warning_x_pos , warning_y_pos))
        screen.blit(sun, (now_sun_x_pos, now_sun_y_pos))
        screen.blit(interaction, (interaction_x_pos, interaction_y_pos))

        pygame.display.update()

    return

#이벤트 루프
running = True #게임이 진행중인가?

while running:
    dt = clock.tick(60)

    #이벤트 처리
    for event in pygame.event.get(): #이벤트 수집
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running = False #게임 실행 False
        #클릭 관련 이벤트
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if new_game_x_pos < pygame.mouse.get_pos()[0] < new_game_x_pos + new_game_width and new_game_y_pos < pygame.mouse.get_pos()[1] < new_game_y_pos + new_game_height: #새 게임 버튼
                button_sound = pygame.mixer.Sound('.\\resource\\sound\\버튼.wav')
                button_sound.play()
                result = game(0)
                if result == 'death' or result == 'chainsaw':
                    button_sound.play()
                    if result == 'death':
                        pygame.mixer.Sound('.\\resource\\sound\\죽음.wav').play()
                        death_display = pygame.image.load('.\\resource\\death.png')
                    elif result == 'chainsaw':
                        pygame.mixer.Sound('.\\resource\\sound\\장지엔딩.wav').play()
                        end1_display = pygame.image.load('.\\resource\\chainsaw.png')
                    continue_button = pygame.image.load('.\\resource\\컨티뉴.png')
                    continue_button_x_pos = 500
                    continue_button_y_pos = 500
                    continue_button_size = continue_button.get_rect().size
                    continue_button_width = continue_button_size[0]
                    continue_button_height = continue_button_size[1]

                    running_2 = True
                    while running_2:
                        dt = clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if continue_button_x_pos < pygame.mouse.get_pos()[0] < continue_button_x_pos + continue_button_width and continue_button_y_pos < pygame.mouse.get_pos()[1] < continue_button_y_pos + continue_button_height:
                                    print('컨티뉴 눌림')
                                    button_sound.play()
                                    running_2 = False
                                
                                
                        screen.fill(white)
                        screen.blit(death_display, (70, 70))
                        screen.blit(continue_button, (continue_button_x_pos, continue_button_y_pos))
                        screen.blit(gameui, (gameui_x_pos, gameui_y_pos))
                        pygame.display.update()

            if exit_x_pos < pygame.mouse.get_pos()[0] < exit_x_pos + exit_width and exit_y_pos < pygame.mouse.get_pos()[1] < exit_y_pos + exit_height:
                pygame.quit()
                sys.exit()
    
    #게임 캐릭터 위치 정의

    #충돌처리

    #화면에 그리기
    screen.fill(green)
    screen.blit(new_game, (new_game_x_pos, new_game_y_pos))
    screen.blit(following, (following_x_pos, following_y_pos))
    screen.blit(exit, (exit_x_pos , exit_y_pos))
    screen.blit(titles, (titles_x_pos, titles_y_pos))
    pygame.display.update()




#게임 종료
pygame.quit()


# 2022/05/13 현재 각 스킬들의 데미지와 방어력을 측정하여 hp깎는것은 완성, 공격버튼과 방어버튼을 눌렀을 때 짤딜과 배틀엔딩 구현 필요
# 2022/05/18 짤딜과 배틀엔딩 구현 완료 첫 배틀 완성 승리후 대화함수 작동 !소리를 추가 해야함! 승리시 보상 시스템 추가 필요
# 2022/05/20 기본 스킬 2개와 기본 공격,방어,집중 소리 추가 함 승리시 보상 시스템 추가 필요 소리조절 버튼 필요 슬슬 다음 맵 만들어야 됨
# 2022/05/22 진짜 아 무 것 도 안함 item함수 하나 이름만 붙여놓음
# 2022/05/27 item함수 소리랑 형태만 대충 잡아둠 세부 아이템 설정은 어떻게 할지 생각좀 해봐야 할듯 소리조절 버튼이랑 나무 캐서 아이템 칸에 넣는거 만들어보자
# 2022/05/28 뭐 안함
# 2022/05/29 다음 화면 만들고 나무 추가함 이동하는 소리 추가와 나무 위치/다른 나무 추가 및 나무 캐는 모션 추가 필요
# 2022/06/03 영상 추가
# 2022/06/04 item_frame추가 아직 ypos 안정함
# 2022/06/05 나뭇가지를 주울 시 아이템창에 나오는 것 추가 아이템 위에 마우스를 올렸을시 설명 나오도록 추가 필요
# 2022/06/06 아이템 그림을 클릭하면 설명이 나오도록 추가
# 2022/06/10 장소3 추가, 장소 2에 민규 추가 필요, 장소 3에 간단한 적 추가(민이)
# 2022/06/11 요정 추가, 요정 퀘스트 관련 기능 추가 필요
# 2022/06/12 대화기능 몇번 만났는지 확인 할 수있도록 개편, 아이템기능 뼈와 나뭇가지를 동시에 먹었을 때 뼈만 나오는 문제 수정 필요, 아이템리스트를 전역변수로 만듬
# 2022/06/17 아이템문제 수정 완료, 티모가 나뭇가지 10개와 뼈 5개 이상 가지고 있을 때 가져가게 함 보상 추가 필요, 장소 3 간단한 적 추가 필요
# 2022/06/18 스킬 가이드 함수 추가 완료, 보상 필요, 스킬가이드 함수 스킬 확인과 출력 구현 필요
# 2022/06/19 스킬가이드 함수 스킬 이름 찾아 적기 구현, 보상 필요, 스킬 사용방법과 스킬 설명 적기 구현 필요
# 2022/06/24 스킬 사용방법과 스킬 설명 적기 구현 완료, 티모 실명 다트 기술 추가. 배틀 기능에서 성능 구현 필요 이제 부터 패치노트는 인스타로 올림
# 2022/09/06 먹을 수 있는 아이템 전투시에 먹기버튼 띄우기까지 구현 완료, 먹는 기능 추가 필요
# 2022/09/12 먹는 기능 추가 완료, 합성티켓 사용기능 추가 필요
# 2022/09/17 합성 함수 기본 틀 제작 완료, 합성 기능과 아이템 함수간의 연계 개발 필요
# 2022/09/18 합성 기능에 아이템함수 추가 완료, 합성버튼 누를 시 아이템 개수는 줄어드나 아직 기술을 얻지는 않음 개발 필요
# 2022/09/24 스킬 레벨 추가, 뼈 합성 추가 다른 합성재료와 스킬 추가 필요
# 2022/09/25 스킬 레벨 관련 함수 개선, 뼈 합성기능 개선, 오징어다리 상점 팔기기능 추가
# 2022/10/01 화내기, 화염방사 기술 추가
# 2022/10/08 흡수 기술 추가
# 2022/10/10 성현이와 마탑1층 구현완료
# 2022/10/14 성현이와 전투 기술 구현 완료