def get_box_depth(frame, box):
    # print(box)
    temp = [
        frame.get_distance((box[0] + box[2]) // 2, (box[1] + box[3]) // 2),
        frame.get_distance((box[0] + box[2]) // 2, (2 * box[1] + box[3]) // 3),
        frame.get_distance((box[0] + box[2]) // 2, (box[1] + 2 * box[3]) // 3),
        frame.get_distance((2 * box[0] + box[2]) // 3, (box[1] + box[3]) // 2),
        frame.get_distance((2 * box[0] + box[2]) // 3, (2 * box[1] + box[3]) // 3),
        frame.get_distance((2 * box[0] + box[2]) // 3, (box[1] + 2 * box[3]) // 3),
        frame.get_distance((box[0] + 2 * box[2]) // 3, (box[1] + box[3]) // 2),
        frame.get_distance((box[0] + 2 * box[2]) // 3, (2 * box[1] + box[3]) // 3),
        frame.get_distance((box[0] + 2 * box[2]) // 3, (box[1] + 2 * box[3]) // 3),
    ]

    res = sum(temp)
    counter = 0
    # print(f"TEMP: {temp}")
    for el in temp:
        if el:
            counter += 1
    return round(res / counter, 3) if counter else -1


def set_predictions_depth(frame, predictions):
    for pred in predictions:
        pred['depth'] = get_box_depth(frame, pred['box'])
        print(pred)
