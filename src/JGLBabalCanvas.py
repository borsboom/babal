import time
from java.lang import Thread, Runnable
from java.awt import Canvas, Dimension
from java.awt.event import KeyListener, KeyEvent, ComponentListener
from java.awt.image import MemoryImageSource
from synchronize import make_synchronized
import jgl.GL
import jgl.GLU
import jgl.GLUT

from Game import Game
import gl_draw


class JGLBabalCanvas(Canvas, Runnable, KeyListener, ComponentListener):

    def __init__(self, w, h, map_file=None):
        self.initSize = Dimension(w, h)
        self.GL = jgl.GL()
        self.GLU = jgl.GLU(self.GL)
        self.GL.glXMakeCurrent(self, 0, 0)
        self.game = Game(map_file)
        self._resized = 0
        self._image = None
        self._image_source = None
        self.addKeyListener(self)
        self.addComponentListener(self)
        gl_draw.init(self.GL, self.GLU, self.game)

    def start(self):
        self.game.reset_timer()
        self.thread = Thread(self)
        self.thread.start()

    def stop(self):
        self.thread = None

    def preferredSize(self):
        return self.initSize

    def minimumSize(self):
        return self.initSize

    def update(self, g):
        self.paint(g)

    def paint(self, g):
        #print 'START paint'
        if self._image:
            g.drawImage(self._image, 0, 0, self)
        #print 'END paint'
    paint = make_synchronized(paint)

    def _draw(self):
        #print 'START draw'
        self.game.update()
        gl_draw.draw()
        if self._resized:
            self._image_source = self.GL.glXGetImageSource()
            self._image_source.setAnimated(1)
            self._image = self.createImage(self._image_source)
            self._resized = 0
            self.repaint()
        elif self._image_source:
            self._image_source.newPixels()                
        #print 'END draw'
    _draw = make_synchronized(_draw)            

    def run(self):
  	me = Thread.currentThread( );
	me.setPriority(Thread.MIN_PRIORITY);
        while self.thread == Thread.currentThread():
            try:
                Thread.sleep(1)
            except InterruptedException:
                return
            self._draw()

    def keyPressed(self, e):
        code = e.getKeyCode()
        if code == KeyEvent.VK_LEFT:
            self.game.begin_left()
        elif code == KeyEvent.VK_RIGHT:
            self.game.begin_right()
        elif code == KeyEvent.VK_UP:
            self.game.begin_accel()
        elif code == KeyEvent.VK_DOWN:
            self.game.begin_decel()
        elif code == KeyEvent.VK_SPACE:
            self.game.begin_jump()
    keyPressed = make_synchronized(keyPressed)

    def keyReleased(self, e):
        code = e.getKeyCode()
        if code == KeyEvent.VK_LEFT:
            self.game.end_left()
        elif code == KeyEvent.VK_RIGHT:
            self.game.end_right()
        elif code == KeyEvent.VK_UP:
            self.game.end_accel()
        elif code == KeyEvent.VK_DOWN:
            self.game.end_decel()
        elif code == KeyEvent.VK_SPACE:
            self.game.end_jump()
    keyReleased = make_synchronized(keyReleased)

    def keyTyped(self, e):
        if e.getKeyChar() == 'p' or e.getKeyChar() == 'P':
            self.game.toggle_pause()
    keyTyped = make_synchronized(keyTyped)

    def componentResized(self, e):
        size = self.getSize()
        gl_draw.reshape(size.width, size.height)
        self._resized = 1
    componentResized = make_synchronized(componentResized)

    def componentMoved(self, e):
        pass # required for ComponentListener interface

    def componentHidden(self, e):
        pass # required for ComponentListener interface

    def componentShown(self, e):
        pass # required for ComponentListener interface

