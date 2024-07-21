import csv
import json

example = [
    ["Tom", "Smith", 80, True],
    ["Alice", "Johnson", 92, False],
    ["Bob", "Williams", 75, True],
    ["Emma", "Brown", 88, False],
    ["David", "Jones", 107, True]
]


def writecsv():
    filename = 'people.csv'
    with open(filename, mode='w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['First name', 'Last name','Weight', 'is male'])
        writer.writerows(example)

def writejson():
    filename = 'people.json'
    data = [
        {'first_name': first_name, 'last_name': last_name, 'weight': weight, 'is_male': is_male}
        for first_name, last_name, weight, is_male in example
    ]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)



if __name__ == "__main__":
    # writecsv()
    writejson()
