#!/usr/bin/env python3

import os
import sys
import random
import itertools
import importlib
import importlib.machinery
import operator
import copy

SRCPATH = './src/'

def start_fight():
    part_src = list()
    with os.scandir(SRCPATH) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                part_src.append((entry.name, entry.path))

    # 풀매치 시작
    input('지금부터 선수 {}명의 풀매치를 시작합니다.'.format(
            len(part_src)))
    print('경기 진행중...')
    full_result = get_full_match(part_src)
    for index in range(0, len(full_result)):
        print('{:03d}위 {:<39s} {}'.format(index+1, 
                                          str(full_result[index][1]),
                                          full_result[index][0][0]))
    input('풀매치 결과 확인하셨나요?')
    print('')

    # 강 시작
    rest = 16
    # 강 선수에 맞춰서 엔트리 조정
    entry = list()
    for index in range(0, rest):
        entry.append(full_result[index][0])
    # 강 경기 진행
    while rest > 1:
        input('지금부터 {}강을 시작합니다.'.format(rest))
        input('{}강 대진표를 확인합니다.'.format(rest))
        # 대진표
        for index in range(0, len(entry)):
            entry_name = entry[index][0].split('.')[0]
            print('{:2d}번선수: {}'.format(index+1, entry_name))
            if index % 2 == 1:
                print('')
        # 경기 진행
        input('{}강 경기 시작합니다.'.format(rest))
        players = list()
        pround = 1
        ahead = list()
        for index in range(0, len(entry)):
            players.append(entry[index])
            if len(players) == 2:
                p1_name = players[0][0].split('.')[0]
                p2_name = players[1][0].split('.')[0]
                input('{}강 {}번 경기: {} 대 {}'.format(rest,
                                                        pround,
                                                        p1_name,
                                                        p2_name))
                result = get_result(players[0], players[1])
                print('경기결과: \n{} 대 \n{}'.format(result[0],
                                                  result[1]))
                if get_score(result[0]) > get_score(result[1]):
                    input('{} 승리!'.format(p1_name))
                    ahead.append(players[0])
                elif get_score(result[0]) < get_score(result[1]):
                    input('{} 승리!'.format(p2_name))
                    ahead.append(players[1])
                else:
                    lotto = random.choice(players)
                    lotto_name = lotto[0].split('.')[0]
                    input('{} 무승부로 추첨 승리!'.format(lotto_name))
                    ahead.append(lotto)
                print('')
                players.clear()
                pround = pround + 1
        entry = copy.deepcopy(ahead)
        rest = rest // 2

    input('우승! {}'.format(entry[0][0].split('.')[0]))
    input('감사합니다. 종료하시려면 엔터를 3번 눌러야합니다.')
    input('충남대학교 데이터네트워크연구실 문현수가 만들었습니다.')
    input('안녕!')


def get_full_match(part_src):
    all_score = dict()
    for node in itertools.combinations(part_src, 2):
        if not node[0] in all_score:
            all_score[node[0]] = {'win': 0, 'lose': 0, 'draw': 0}
        if not node[1] in all_score:
            all_score[node[1]] = {'win': 0, 'lose': 0, 'draw': 0}
        result = get_result(node[0], node[1])
        if get_score(result[0]) > get_score(result[1]):
            all_score[node[0]]['win'] = \
                    all_score[node[0]]['win'] + 1
            all_score[node[1]]['lose'] = \
                    all_score[node[1]]['lose'] + 1
        elif get_score(result[0]) < get_score(result[1]):
            all_score[node[0]]['lose'] = \
                    all_score[node[0]]['lose'] + 1
            all_score[node[1]]['win'] = \
                    all_score[node[1]]['win'] + 1
        else:
            all_score[node[0]]['draw'] = \
                    all_score[node[0]]['draw'] + 1
            all_score[node[1]]['draw'] = \
                    all_score[node[1]]['draw'] + 1
    rank = list()
    for node in all_score:
        rank.append( (node, all_score[node], get_score(all_score[node])) )
    random.shuffle(rank)
    rank.sort(key = operator.itemgetter(2), reverse = True)

    return rank
        
        
def get_score(player):
    player_total = (player['win'] * 2
                  + player['lose'] * -1 
                  + player['draw'] * 1)
    return player_total
    

def get_result(p1, p2):
    p1_score = {'win': 0, 'lose': 0, 'draw': 0}
    p2_score = {'win': 0, 'lose': 0, 'draw': 0}
    p1m = importlib.machinery.SourceFileLoader('*', p1[1]).load_module()
    p2m = importlib.machinery.SourceFileLoader('*', p2[1]).load_module()
    p1_last = None
    p2_last = None
    for node in range(0, 10000):
        p1_hand = p1m.get_hand(p1_last)
        p2_hand = p2m.get_hand(p2_last)
        if p1_hand == 'kawi' and p2_hand == 'kawi':
            p1_result = 'draw'
            p2_result = 'draw'
        elif p1_hand == 'kawi' and p2_hand == 'bawi':
            p1_result = 'lose'
            p2_result = 'win'
        elif p1_hand == 'kawi' and p2_hand == 'bo':
            p1_result = 'win'
            p2_result = 'lose'
        elif p1_hand == 'bawi' and p2_hand == 'kawi':
            p1_result = 'win'
            p2_result = 'lose'
        elif p1_hand == 'bawi' and p2_hand == 'bawi':
            p1_result = 'draw'
            p2_result = 'draw'
        elif p1_hand == 'bawi' and p2_hand == 'bo':
            p1_result = 'lose'
            p2_result = 'win'
        elif p1_hand == 'bo' and p2_hand == 'kawi':
            p1_result = 'lose'
            p2_result = 'win'
        elif p1_hand == 'bo' and p2_hand == 'bawi':
            p1_result = 'win'
            p2_result = 'lose'
        elif p1_hand == 'bo' and p2_hand == 'bo':
            p1_result = 'draw'
            p2_result = 'draw'
        p1_last = (p1_hand, p1_result)
        p2_last = (p2_hand, p2_result)
        p1_score[p1_result] = p1_score[p1_result] + 1
        p2_score[p2_result] = p2_score[p2_result] + 1
    return (p1_score, p2_score)


def main(argv):
    start_fight()



if __name__ == '__main__':
    sys.exit(main(sys.argv))
