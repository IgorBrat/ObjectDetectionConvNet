import csv

HEADERS = ['class', 'confidence', 'x_left', 'y_top', 'x_right', 'y_bottom', 'depth']


def init_results(
        file,
):
    with open(file, "w") as fcsv:
        writer = csv.DictWriter(fcsv, fieldnames=HEADERS)
        writer.writeheader()


# Should check dictionary format - won`t parse box to xyxy
def write_results(
        file,
        predictions,
):
    if not predictions:
        return
    with open(file, "a") as fcsv:
        writer = csv.DictWriter(fcsv, fieldnames=HEADERS)
        for pred in predictions:
            writer.writerow(pred)
