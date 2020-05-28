import random

def contour(feats):

    temp = []
    temp_temp = []
    sorted(feats, key=lambda k: [k[1], k[0]])

    for x in range(1, len(feats)):
        if feats[x][1] == feats[x-1][1]:
            temp_temp.append(feats[x-1])
        else:
            temp_temp.append(feats[x-1])
            temp.append(temp_temp[0])
            temp.append(temp_temp[len(temp_temp)- 1])
            temp_temp = []
            temp_temp.append

    return temp

def contour_random(feats):
    for x in range(100):
        feats.remove(random.choice(feats))

    return feats

