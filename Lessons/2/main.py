import xml.etree.ElementTree as ET
import json


def parsexml_1():
    result =[]
    tree = ET.parse("cats.xml")
    root = tree.getroot()

    for child in root:
        for child2 in child:
            if child2.tag == "fact":
                result.append(child2.text)

    with open('cat_result.txt', "w") as f:
        f.write("\n".join(result))


def parsexml_2():
    result = []
    tree = ET.parse("cats.xml")
    root = tree.getroot()
    for info in root.findall("info"):
        fact = info.find('fact').text
        result.append(fact)
    with open('cat_result_2.txt', "w") as f:
        f.write("\n".join(result))


def parsejson():
    with open('cat.json') as file:
        data = json.load(file)

    print (data.get('fact'))

def parsexml_2_to_json():
    result = {}
    tree = ET.parse("cats.xml")
    root = tree.getroot()
    for number, info in enumerate(root.findall("info")):
        fact = info.find('fact').text
        result[number] = fact

    print(result, type(result))

    with open('cat_result.json', 'w') as file:
        json.dump(result,file)



if __name__ == "__main__":
    # parsexml_1()
    # parsexml_2()
    # parsejson()
    parsexml_2_to_json()