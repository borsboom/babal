import sys
from java.awt import Frame
from java.awt.event import WindowAdapter
from java.lang import Runnable
from JGLBabalCanvas import JGLBabalCanvas


class CloseListener(WindowAdapter):
    def windowClosing(self, e):
        sys.exit()


class JGLBabalRunnable(Runnable):

    def run(self):
        if len(sys.argv) > 1:
            map_file = open(sys.argv[1], 'r')
        else:
            map_file = None
        frame = Frame()
        frame.setTitle('Babal')
        canvas = JGLBabalCanvas(320, 240, map_file)
        frame.add(canvas)
	frame.addWindowListener(CloseListener())
        frame.pack()
        frame.setVisible(1)
        canvas.start()
