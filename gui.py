#!/usr/bin/python

import pygtk
import gtk
import gtk.gdk as gdk
import gtk.glade
from read_nsd import NsdReader
from random import random

class Plot:
    def __init__(self):
        self.glade_file = "gui.glade"
        self.wTree = gtk.glade.XML(self.glade_file)
        self.window = self.wTree.get_widget("mainWindow")
        self.wTree.signal_autoconnect(self)
        self.reader = NsdReader( )
        self.data = []
        for i in range(50):
            self.data += self.reader.parse(self.reader.get_data( ).next( ))
        self.colors = [(random( ), random( ), random( )) for i in range(10)]

    def on_mainWindow_destroy(self, window):
        gtk.main_quit( )

    def update_data(self):
        self.data.pop(0)
        self.data += self.reader.parse(self.reader.get_data( ).next( ))

    def on_plotArea_expose_event(self, widget, event):
        cr = widget.window.cairo_create( )

        width = event.area.width
        height = event.area.height

        number_of_channels = len(self.data[0]["samples"])
        channel_data = [[] for channel in range(number_of_channels)]

        for i in range(number_of_channels):
            for row in self.data:
                try:
                    channel_data[i].append(row["samples"][i])
                except:
                    pass

        maximum = float(max(map(lambda x: max(x), channel_data)))
        minimum = float(min(map(lambda x: min(x), channel_data)))

        self.wTree.get_widget("label1").set_text("maximum: %s" % maximum)
        self.wTree.get_widget("label2").set_text("minimum: %s" % minimum)

        cr.set_line_width(3)

        for channel_index, channel in enumerate(channel_data):
            scale = lambda x: 0.4*height*(float(x) - minimum)/abs(maximum - minimum) + 0.5 * height
            scaled_data = map(scale, channel)
            cr.set_source_rgb(self.colors[channel_index][0], 
                    self.colors[channel_index][1], self.colors[channel_index][2]) 
            for index, row in enumerate(scaled_data):
                cr.arc(width*index*1.0/len(scaled_data), row, 5, 0, 2*3.14)
                cr.line_to(width*index*1.0/len(scaled_data), row)
            cr.stroke( )

        self.update_data( )

        widget.window.invalidate_rect(gdk.Rectangle(0, 0, width, height), True)
        return False



def main( ):
    Plot( )
    gtk.main( )

if __name__ == "__main__": main( )
