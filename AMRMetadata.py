__author__ = 'arenduchintala'
import re
import os
from AMRGraph import AMRGraph


class AMRMetadata():
    def __init__(self, s, parse=False):
        self.attributes = {}
        self.graph_string = None
        self.attributes, self.graph_string = self.divide_text(s)
        self.graph = AMRGraph()
        if parse:
            self.parse_graph()

    def parse_graph(self):
        self.graph.parse_string(self.graph_string)

    def divide_text(self, s):
        '''
        parsing this weird format for AMR and its associated attributes
        :param s:
        :return:
        '''
        meta = ''
        graph_lines = []
        for line in s.split(os.linesep):
            if line.startswith('#'):
                meta += line[1:]
            else:
                graph_lines.append(line)
        graph = '\n'.join(graph_lines)
        meta_items = re.split('(\::[a-zA-Z-_]+\s)', meta)
        attributes = {}
        for idx, mi in enumerate(meta_items):
            if mi.startswith('::'):
                attr_name = mi[2:].strip()
                attr_val = meta_items[idx + 1].strip()
                attributes[attr_name] = attr_val
        return attributes, graph

    def add_attribute(self, k, val):
        self.attributes[k] = val

    def remove_attribute(self, k):
        self.attributes.pop(k, None)

    def __str__(self):
        s = ''
        for k, v in self.attributes.items():
            s += '# ::' + k + ' ' + str(v) + '\n'
        s += self.graph_string.strip() + '\n\n'
        return s


