"""
Extract icons from SVG file.

Author: Sergey Vartanov (me@enzet.ru).
"""

import re
import xml.dom.minidom

class IconExtractor:
    def __init__(self, svg_file_name):
        self.icons = {}

        input_file = open(svg_file_name)
        content = xml.dom.minidom.parse(input_file)
        for element in content.childNodes:
            if element.nodeName == 'svg':
                for node in element.childNodes:
                    if node.nodeName in ['g', 'path']:
                        self.parse(node)

    def parse(self, node):
        if node.nodeName == 'path':
            if 'id' in node.attributes.keys() and \
                    'd' in node.attributes.keys() and \
                    node.attributes['id'].value != '':
                path = node.attributes['d'].value
                m = re.match('[Mm] ([0-9.e-]*)[, ]([0-9.e-]*)', path)
                if not m:
                    print 'Error path: ' + path
                else:
                    x = float(m.group(1))
                    y = float(m.group(2))
                    x = int(x / 16)
                    y = int(y / 16)
                    self.icons[node.attributes['id'].value] = \
                        (node.attributes['d'].value, x, y)
        else:
            for subnode in node.childNodes:
                self.parse(subnode)

    def get_path(self, id):
        if id in self.icons:
            return self.icons[id]
        else:
            return None, 0, 0
