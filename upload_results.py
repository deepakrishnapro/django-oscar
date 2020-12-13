#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def main():
    try:
        print('Calling a function upload tests ')
        tree = ET.parse('/home/travis/build/deepakrishnapro/django-oscar/unit_report.xml')
        print(tree.getroot())
        root = tree.getroot()
        print("tag=%s, attrib=%s" % (root.tag, root.attrib))

    except Exception as exception:
        print("Exception occurred during running upload results  for pipeline-id - Exception details : {}".format(str(exception)))
        pass

if __name__ == "__main__":
    main()
