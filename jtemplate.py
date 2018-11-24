#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
from simplestyle import *
import inkex
import sys
import pystache
import string
import json
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
# The simplestyle module provides functions for style parsing.


class JTemplateEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-j', '--json', action='store',
                                     type='string', dest='json', default='default.json',
                                     help='Json file to template')

    def effect(self):
        json_path = self.options.json
        json_file = open(json_path, "r")
        json_data = json.loads(json_file.read())

        svg = self.document.getroot()
        textElements = svg.xpath(
            '//svg:text', namespaces=inkex.NSS)

        for e in textElements:
            style = e.get('style')
            line_height = inkex.unittouu(parseStyle(style)["line-height"])
            font_size = inkex.unittouu(parseStyle(style)["font-size"])
            font_spacing = font_size * line_height
            x = e.get('x')
            y = inkex.unittouu(e.get('y'))

            old_text = string.join(e.xpath(".//text()"), "\n")
            for tspan in e.getchildren():
                e.remove(tspan)

            new_text = pystache.render(old_text, json_data)

            lines = new_text.split("\n")

            for line in lines:
                tspan = inkex.etree.Element(inkex.addNS('tspan', 'svg'), attrib={
                    inkex.addNS('role', 'sodipodi'): 'line',
                    'x': x,
                    'y': str(y)})
                tspan.text = line + "\n"
                e.append(tspan)
                y += font_spacing


effect = JTemplateEffect()
effect.affect()
