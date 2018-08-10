import xml.etree.ElementTree as ET

def main():
    tree = ET.parse('sample1.xml')
    root = tree.getroot()

    print(root[0].text, root[1].text, root[2].text)
    print(root[3][1].text)
    print(root[4][1].text)

    tree = ET.parse('sample2.xml')
    root = tree.getroot()

    print(root.attrib['firstName'], root.attrib['lastName'], root.attrib['age'])
    print(root[0].attrib['city'])
    print(root[1].attrib['number'])



if __name__ == '__main__':
    main()