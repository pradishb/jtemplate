#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
from simplestyle import *
import inkex
import sys
import pystache
import string
import json
import re
import copy
from lxml.etree import tostring, dump, fromstring
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
# The simplestyle module provides functions for style parsing.


class JTemplateEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-j', '--json', action='store',
                                     type='string', dest='json', default='examples/invoice.json',
                                     help='Json file to template')

    def effect(self):
        json_path = self.options.json
        json_file = open(json_path, "r")
        json_data = json.loads(json_file.read())

        svg = self.document.getroot()

        textElements = svg.xpath(
            '//svg:text', namespaces=inkex.NSS)

        for e in textElements:
            e_text = tostring(e)
            e_text = re.sub(r'<tspan [^>]*>({{[#/][^}}]*}})<\/tspan>',
                            r'\1', e_text)
            new_text = pystache.render(e_text, json_data)
            elem = fromstring(new_text)
            e.getparent().replace(e, elem)


effect = JTemplateEffect()
effect.affect()
