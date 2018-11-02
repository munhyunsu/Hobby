import copy
import time
import random

import matplotlib.pyplot as plt

import my_sort


def main():
    list01 = ['z', 'y', 'x', 'w', 'v',
              'u', 't', 's', 'r', 'q',
              'p', 'o', 'n', 'm', 'l',
              'k', 'j', 'i', 'h', 'g',
              'f', 'e', 'd', 'c', 'b',
              'a']
    list02 = ['harm', 'winter', 'flow', 'flock', 'pump',
              'stop', 'dear', 'cluttered', 'ignorant', 'delicious',
              'tan', 'downtown', 'grieving', 'mass', 'smile',
              'lively', 'messy', 'peace', 'soup', 'person',
              'impulse', 'null', 'box', 'secretive', 'pickle',
              'creepy', 'horse', 'resonant', 'thread', 'bed',
              'skirt', 'suit', 'camp', 'living', 'natural',
              'profit', 'education', 'drain', 'boast', 'grouchy',
              'plants', 'tank', 'smoke', 'condition', 'glossy',
              'puzzled', 'station', 'start', 'perpetual', 'brake',
              'cracker', 'insect', 'ski', 'camp', 'check',
              'theory', 'open', 'historical', 'reflect', 'name',
              'obsolete', 'billowy', 'baseball', 'precious', 'recess',
              'play', 'understood', 'drain', 'sleet', 'fancy',
              'accessible', 'good', 'minister', 'watch', 'picture',
              'woman', 'raise', 'maid', 'clip', 'aspiring',
              'giant', 'thankful', 'beginner', 'hose', 'tap',
              'vivacious', 'direction', 'view', 'various', 'puny',
              'massive', 'rod', 'whisper', 'books', 'memorise',
              'little', 'giddy', 'soak', 'pass', 'sack',
              'close', 'current', 'wacky', 'abashed', 'disturbed',
              'elfin', 'long', 'squeak', 'thirsty', 'limping',
              'brother', 'feeling', 'year', 'offer', 'upbeat',
              'black-and-white', 'quicksand', 'film', 'flippant', 'ripe',
              'assorted', 'time', 'parsimonious', 'invention', 'shade',
              'bomb', 'seal', 'teaching', 'ambitious', 'sand',
              'airplane', 'digestion', 'abaft', 'daily', 'honorable',
              'clear', 'dad', 'tidy', 'calendar', 'command',
              'three', 'milky', 'economic', 'representative', 'sad',
              'lunch', 'callous', 'cable', 'magenta', 'prefer',
              'trite', 'perform', 'zebra', 'saw', 'lace',
              'lush', 'store', 'likeable', 'recondite', 'cobweb',
              'carpenter', 'spade', 'box', 'locket', 'jealous',
              'unequal', 'bear', 'shiny', 'burn', 'nosy',
              'jaded', 'suck', 'untidy', 'sordid', 'one',
              'deafening', 'nasty', 'merciful', 'impress', 'ugly',
              'space', 'lock', 'thaw', 'canvas', 'loose',
              'whip', 'diligent', 'old-fashioned', 'kindly', 'old',
              'redundant', 'zealous', 'naughty', 'dam', 'dare',
              'loaf', 'crook', 'earth', 'fly', 'discover',
              'hall', 'extra-large', 'ban', 'tedious', 'funny',
              'beneficial', 'aback', 'house', 'rotten', 'pull',
              'pollution', 'wing', 'measure', 'nebulous', 'boat',
              'tomatoes', 'bow', 'clean', 'even', 'guard',
              'lovely', 'true', 'chickens', 'signal', 'neat',
              'judge', 'slim', 'blushing', 'fresh', 'respect',
              'matter', 'rule', 'exchange', 'early', 'labored',
              'flagrant', 'celery', 'righteous', 'talk', 'chin',
              'touch', 'club', 'pricey', 'moldy', 'overwrought',
              'weak', 'self', 'breakable', 'skate', 'poor',
              'small', 'approval', 'terrible', 'abusive', 'zephyr',
              'finger', 'equal', 'left', 'grip', 'battle',
              'value', 'poised', 'prepare', 'erect', 'detail',
              'flesh', 'ludicrous', 'thought', 'ceaseless', 'bird',
              'watery', 'well-to-do', 'spot', 'cake', 'blue-eyed',
              'eight', 'amuse', 'spotty', 'exclusive', 'shiver',
              'load', 'puzzling', 'amuck', 'holiday', 'muddled',
              'drown', 'dangerous', 'next', 'taste', 'huge',
              'move', 'tired', 'feigned', 'faint', 'unsuitable',
              'knowing', 'abrupt', 'guarded', 'waves', 'moaning',
              'shelter', 'wretched', 'suit', 'charge', 'toad',
              'clever', 'flash', 'sparkle', 'crack', 'ritzy',
              'building', 'school', 'thank', 'potato', 'force',
              'enchanting', 'sweater', 'extend', 'idea', 'spell',
              'friendly', 'satisfy', 'rub', 'depressed', 'spot',
              'morning', 'hang', 'remarkable', 'twig', 'crown',
              'explode', 'gratis', 'deserted', 'helpful', 'place',
              'pizzas', 'deep', 'point', 'hard', 'hurt',
              'adjoining', 'glistening', 'alarm', 'zesty', 'knowledge',
              'trees', 'impartial', 'incredible', 'reject', 'bustling',
              'resolute', 'slope', 'train', 'pear', 'wave',
              'fireman', 'trousers', 'mine', 'wash', 'face',
              'ashamed', 'arch', 'yielding', 'second-hand', 'leg',
              'lip', 'use', 'sail', 'base', 'rainy',
              'spark', 'increase', 'lean', 'open', 'fish',
              'uttermost', 'laborer', 'disagreeable', 'plot', 'creature',
              'sudden', 'possessive', 'elated', 'cows', 'vein',
              'trip', 'worm', 'quiet', 'decorate', 'lyrical',
              'selfish', 'ruddy', 'afternoon', 'crayon', 'pinch',
              'proud', 'statement', 'church', 'notebook', 'equable',
              'coil', 'gate', 'dolls', 'risk', 'transport',
              'cough', 'vengeful', 'grade', 'scientific', 'choke',
              'boundary', 'attend', 'doubtful', 'volatile', 'unwieldy',
              'zippy', 'loss', 'tightfisted', 'comfortable', 'godly',
              'top', 'rejoice', 'change', 'glass', 'secretary',
              'correct', 'parallel', 'chilly', 'jump', 'acceptable',
              'blow', 'peck', 'gentle', 'thick', 'drawer',
              'striped', 'determined', 'playground', 'itch', 'van',
              'letter', 'jail', 'turn', 'legal', 'cream',
              'vacation', 'phobic', 'sugar', 'rare', 'expand',
              'partner', 'evanescent', 'account', 'thrill', 'lacking',
              'murder', 'quixotic', 'plant', 'request', 'heartbreaking',
              'tall', 'rinse', 'art', 'flap', 'muddle',
              'chivalrous', 'extra-small', 'ticket', 'shirt', 'ear',
              'silent', 'hole', 'overjoyed', 'expensive', 'homely',
              'stitch', 'hanging', 'claim', 'plough', 'produce',
              'yoke', 'meeting', 'fearful', 'suggestion', 'tumble',
              'daffy', 'bang', 'wry', 'invent', 'learn',
              'omniscient', 'imperfect', 'butter', 'tearful', 'boorish',
              'tame', 'yam', 'call', 'summer', 'descriptive',
              'clean', 'mellow', 'children', 'cheap',
              'encouraging', 'admire', 'happen', 'science', 'company',
              'roasted', 'dysfunctional', 'seemly', 'belief', 'borrow',
              'dime', 'angle', 'scattered', 'lonely', 'silent',
              'jeans', 'relation', 'stomach', 'abrasive', 'nippy',
              'mother', 'long', 'army', 'curl', 'development',
              'title', 'guide', 'pedal', 'road', 'dust',
              'painful', 'cannon', 'mourn', 'line', 'womanly',
              'detailed', 'zip', 'receipt', 'mom', 'oven',
              'upset', 'foregoing', 'hug', 'car', 'gusty',
              'bubble', 'form', 'nail', 'cause', 'caring',
              'afford', 'whirl', 'switch', 'eye', 'man',
              'rude', 'smell', 'frightening', 'half', 'flaky',
              'regret', 'question', 'answer', 'cross', 'periodic',
              'talk', 'governor', 'shrug', 'offend', 'doubt',
              'abundant', 'system', 'silky', 'lumber', 'outgoing',
              'vagabond', 'noiseless', 'flashy', 'type', 'cloistered',
              'verdant', 'thirsty', 'mundane', 'observation', 'angry',
              'soggy', 'smoke', 'girls', 'comparison', 'heat',
              'clap', 'jail', 'rock', 'design', 'tow',
              'handle', 'finger', 'scintillating', 'courageous', 'nervous',
              'owe', 'acoustics', 'clover', 'grape', 'turkey',
              'wealthy', 'sign', 'window', 'stir', 'consist',
              'unhealthy', 'tire', 'crooked', 'x-ray', 'full',
              'arrest', 'stage', 'scratch', 'immense', 'rail',
              'husky', 'suffer', 'disgusted', 'painstaking', 'glove',
              'effect', 'aloof', 'story', 'possess', 'death',
              'secret', 'cheerful', 'utopian', 'leather', 'smiling',
              'adjustment', 'spoon', 'balance', 'tense', 'glamorous',
              'graceful', 'rescue', 'street', 'twist', 'efficient',
              'acrid', 'rampant', 'complete', 'false', 'fork',
              'welcome', 'sweet', 'growth', 'exist', 'frequent',
              'truthful', 'holistic', 'average', 'dark', 'replace',
              'hover', 'steel', 'damaged', 'ready', 'throne',
              'group', 'dull', 'sloppy', 'damage', 'crabby',
              'like', 'vigorous', 'trail', 'coil', 'chubby',
              'petite', 'habitual', 'illegal', 'nonchalant', 'expansion',
              'aboard', 'strange', 'pin', 'injure', 'knock',
              'zoom', 'crowded', 'skin', 'price', 'elastic',
              'coherent', 'beef', 'eyes', 'sock', 'agree',
              'willing', 'prick', 'suggest', 'complete', 'agreement',
              'pot', 'fact', 'boot', 'enter', 'soft',
              'stone', 'record', 'lick', 'heat', 'ignore',
              'dress', 'defective', 'adventurous', 'illustrious', 'file',
              'practise', 'gifted', 'permit', 'decide', 'snatch',
              'mind', 'ruin', 'clear', 'obtain', 'plant',
              'wink', 'honey', 'tiresome', 'pink', 'mailbox',
              'sleepy', 'knot', 'save', 'surprise', 'tangy',
              'pastoral', 'juvenile', 'broken', 'bikes', 'hunt',
              'orange', 'join', 'card', 'ad hoc', 'lighten',
              'cure', 'bath', 'surprise', 'pies', 'animal',
              'action', 'ubiquitous', 'synonymous', 'mark', 'fang',
              'stain', 'tour', 'parcel', 'mixed', 'quirky',
              'spiders', 'stew', 'necessary', 'jam', 'field',
              'channel', 'front', 'sprout', 'psychedelic', 'shoe',
              'embarrass', 'work', 'describe', 'wish', 'test',
              'return', 'ill', 'lavish', 'past', 'trace',
              'bore', 'romantic', 'nauseating', 'excited', 'pause',
              'vase', 'fold', 'somber', 'spring', 'giraffe',
              'mute', 'blue', 'macabre', 'hospital', 'rapid',
              'meal', 'try', 'basin', 'unit', 'wind',
              'concentrate', 'hand', 'follow', 'intelligent', 'fuzzy',
              'annoy', 'range', 'queen', 'thinkable', 'sheet',
              'brush', 'highfalutin', 'squalid', 'trust', 'skinny',
              'contain', 'dead', 'jewel', 'found', 'weary',
              'rough', 'teeny-tiny', 'wrench', 'lewd', 'metal',
              'dislike', 'shame', 'motionless', 'grease', 'dirt',
              'rebel', 'jar', 'frame', 'pump', 'grandmother',
              'distance', 'greasy', 'wander', 'dry', 'nest',
              'grab', 'root', 'scare', 'scale', 'share',
              'snore', 'produce', 'flight', 'condemned', 'ethereal',
              'abnormal', 'unable', 'spectacular', 'truck', 'baby',
              'invincible', 'yard', 'cool', 'retire', 'brown',
              'overflow', 'seashore', 'float', 'tasteless', 'hapless',
              'slave', 'lucky', 'guide', 'earthy', 'income',
              'square', 'miscreant', 'regular', 'attack', 'writing',
              'thing', 'heady', 'aftermath', 'aware', 'amusing',
              'friction', 'peel', 'longing', 'tease', 'sore',
              'camera', 'frantic', 'twist', 'thundering', 'numerous',
              'advise', 'erratic', 'place', 'ocean', 'kneel',
              'rock', 'tick', 'guitar', 'grate', 'acidic',
              'tax', 'rhetorical', 'therapeutic', 'grateful', 'apparatus',
              'jumpy', 'outstanding', 'mice', 'reaction', 'stale',
              'excuse', 'wide-eyed', 'basket', 'deserve', 'grandfather',
              'furtive', 'bucket', 'discreet', 'expect', 'disgusting',
              'third', 'country', 'abandoned', 'fetch', 'bolt',
              'tip', 'step', 'grass', 'agreeable', 'spurious',
              'color', 'separate', 'picayune', 'pack', 'pat',
              'credit', 'internal', 'compare', 'vessel', 'whine',
              'instinctive', 'squash', 'draconian', 'abounding', 'substantial',
              'hum', 'black', 'alcoholic', 'magic', 'shape',
              'stem', 'quarter', 'absent', 'lively', 'quilt',
              'land', 'point', 'harsh', 'songs', 'side',
              'real', 'sisters', 'edge', 'receptive', 'overrated',
              'knot', 'cast', 'thoughtful', 'live', 'anxious',
              'support', 'show', 'soothe', 'meek', 'cushion',
              'plantation', 'responsible', 'pig', 'puffy', 'drag',
              'ants', 'ancient', 'pleasant', 'ajar', 'actor',
              'political', 'groovy', 'unaccountable', 'empty', 'hook',
              'want', 'tame', 'record', 'plug', 'stimulating',
              'violent']

    time_bubble = list()
    time_selection = list()
    time_insertion = list()
    time_merge = list()
    time_quick = list()
    time_heap = list()
    time_lib = list()

    x_axis = [100, 200, 300, 400, 500,
              600, 700, 800, 900, 1000]

    for index in x_axis:
        index = index + 1
        random.shuffle(list02)
        target = copy.deepcopy(list02[:index])
        start_time = time.process_time()
        my_sort.bubble_sort(target)
        end_time = time.process_time()
        time_bubble.append(end_time - start_time)

        target = copy.deepcopy(list02[:index])
        start_time = time.process_time()
        my_sort.selection_sort(target)
        end_time = time.process_time()
        time_selection.append(end_time - start_time)

        target = copy.deepcopy(list02[:index])
        start_time = time.process_time()
        my_sort.insertion_sort(target)
        end_time = time.process_time()
        time_insertion.append(end_time - start_time)

        target = copy.deepcopy(list02[:index])
        start_time = time.process_time()
        my_sort.merge_sort(target)
        end_time = time.process_time()
        time_merge.append(end_time - start_time)

        target = copy.deepcopy(list02[:index])
        start_time = time.process_time()
        my_sort.quick_sort(target)
        end_time = time.process_time()
        time_quick.append(end_time - start_time)

        target = copy.deepcopy(list02[:index])
        start_time = time.process_time()
        my_sort.heap_sort(target)
        end_time = time.process_time()
        time_heap.append(end_time - start_time)

        target = copy.deepcopy(list02[:index])
        start_time = time.process_time()
        target.sort()
        end_time = time.process_time()
        time_lib.append(end_time - start_time)

    print(time_bubble)
    print(time_selection)
    print(time_insertion)
    print(time_merge)
    print(time_quick)
    print(time_heap)
    print(time_lib)

    plt.plot(x_axis, time_bubble, 'r.-', label='Bubble')
    plt.plot(x_axis, time_selection, 'g.-', label='Selection')
    plt.plot(x_axis, time_insertion, 'b.-', label='Insertion')
    plt.plot(x_axis, time_merge, 'm.-', label='Merge')
    plt.plot(x_axis, time_quick, 'y.-', label='Quick')
    plt.plot(x_axis, time_quick, 'c.-', label='Heap')
    plt.plot(x_axis, time_lib, 'k.-', label='Library')
    plt.legend(bbox_to_anchor=(0.05, 0.95), loc=2, borderaxespad=0.0)
    plt.title('compare execution time between sorting algorithm')
    plt.ylabel('Execution time')
    plt.xlabel('The number of words')
    plt.savefig('output.png', bbox_inches='tight')
    plt.show()
    plt.close()


if __name__ == '__main__':
    main()
