

def percent_error(feats_original, feats_test):
    original_x = feats_original[0]
    original_y = feats_original[1]

    test_x = feats_test[0]
    test_y = feats_test[1]

    temp_x = abs(test_x - original_x)/original_x
    temp_y = abs(test_y - original_y)/original_y

    return (temp_x + temp_y)*100

def check_accuracy(feats_test, feats_original, accuracy_range):

    diff = []
    
    feats_original.sort()
    feats_test.sort()

    if len(feats_test) > len(feats_original):
        for x in range(len(feats_original) - 1):
            if abs(feats_original[x][0][0] - feats_test[x][0][0]) < accuracy_range and abs(feats_original[x][0][1] - feats_test[x][0][1]) < accuracy_range: 
                diff.append(percent_error(feats_original[x][0], feats_test[x][0]))

                
    else:
        for x in range(len(feats_test) - 1):
            if abs(feats_original[x][0][0] - feats_test[x][0][0]) < accuracy_range and abs(feats_original[x][0][1] - feats_test[x][0][1]) < accuracy_range: 
                diff.append(percent_error(feats_original[x][0], feats_test[x][0]))

    return diff

