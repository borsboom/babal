BABAL
Copyright (C) 2003 Emanuel Borsboom (http://www.nuel.ca/)
Based on Babal for HP48 (http://www.ufoot.org/babal/) by U-Foot.
Map data by U-Foot (http://www.ufoot.org/) and Makoto Miyamoto.

Goal:
    
    Don't fall into the holes!

Keys:
    
    Space - Jump    
    Up    - Speed up    
    Down  - Slow down    
    Left  - Move left    
    Right - Move right
    P     - Pause

About:

    I just made this to learn a bit about OpenGL and to experiment with writing
    a game using a scripting language (Python).  As a side benefit, since I
    could use Jython to run the Python code under Java and jGL for OpenGL, I
    made a Java applet version.  I thought folks might like to try it, so here
    it is.

    Babal was my favorite game for the HP48 calculator that I got in grade 11,
    and there doesn't seem to be anything like it for other platforms so I
    thought it would be a perfect game to remake for my project.

    This is totally un-optimized, so it runs much more slowly than it should,
    especially the Java version (jGL does not appear to have been made for
    real-time, and Jython isn't exactly fast either).  My PIII 800 only runs
    the Java version a little bit faster than the HP48 version ran!

    The game isn't complete yet.  There is no score keeping, and you can't
    actually win (once you reach the end of the level, you just keep going
    forever).  Most of the original game is there, though, and it's just as
    addictive.

    I have a number of ideas for expansions on the concept that I may be
    implementing in the future, in addition to speed and graphics improvements.

Running the Windows executable:

    Requirements:

        - OpenGL.  Any recent version of Windows should include this.

    Unzip 'babal-win32.zip' and run 'babal.exe'.  To play a different map,
    specify the filename on the command-line.

    I have tested this with the following configurations:
    
        - Windows 2000, nVidia gForce 3
        - Windows ME, Matrox G400
        - Windows 98, NeoMagic 128XD

Running it using Python:

    Requirements:

        - Python (http://www.python.org/).  Tested with version 2.2 under Linux
          and Win32.  The 'python' executable must be in your path.
        - PyOpenGL (http://pyopengl.sourceforge.net/).  Tested with version
          2.0.0.44.

    Run it from the base folder using the following command-line: 

        python src/babal.py

    To play a different map, specify the filename on the command-line.

    I have tested this with the following configurations:

        - Linux Mandrake 9.0, Matrox G400
        - Windows 2000, nVidia gForce 3
        - Windows ME, Matrox G400.
        - Windows 98, no video acceleration

Running it using Jython (Java):

    Requirements:

        - Java (http://java.sun.com/).  Tested with J2SE 1.4.1 and JDK 1.1.8.
        - Jython (http://www.jython.org/).  Tested with version 2.1.
        - jGL (http://www.cmlab.csie.ntu.edu.tw/~robin/JavaGL/).  Tested with
          version 2.4.
        - You must modify jGL's jgl/GL.java class and add this method:

            public MemoryImageSource glXGetImageSource() {
                return new MemoryImageSource(Context.Viewport.Width,
                                             Context.Viewport.Height,
                                             Context.ColorBuffer.Buffer, 0,
                                             Context.Viewport.Width);
            }

          Then, recompile jGL.
        - The 'jython' executable must be in your path.
        - The jGL classes must be in your CLASSPATH.

    Run it from the base folder using the following command-line: 

        jython src/babal.py

Building and running the Java Applet:

    Requirements:

        - Same requirements as above.
        - If you want the applet to run in as many web browsers as possible,
          use JDK 1.1.

    To create the Applet JAR, run 'scripts/build_applet.sh'.

    To view the Applet, load 'babal_applet.html' into your web browser or
    appletviewer.

    The 'map' Applet parameter specifies the map to load.

    I have tested the applet with the following configurations:
    
        - Windows 2000/Linux, Mozilla 1.2, J2SE 1.4.1
        - Windows 2000, Internet Explorer 6.0, J2SE 1.4.1
        - Windows ME, Internet Explorer 5.5, JRE 1.4.1
        - Windows 98, Internet Explorer 6.0, JRE 1.4.0
        - Windows 98, Internet Explorer 6.0, Microsoft JVM 98 (some graphics
          glitches, but playable)
        - Windows ME, Internet Explorer 5.5, Microsoft JVM 2000

    In theory, the applet should run in any browser that supports Java 1.1 or
    above.

Building the Windows executable:

    Requirements:

        - Same as for running the Python version
        - py2exe (http://starship.python.net/crew/theller/py2exe/index.html).
          Tested with version 0.3.3.
        - Info-zip zip (http://www.info-zip.org/)

    First, edit 'scripts/build_exe.bat' and set the variables at the top
    appropriately.

    Run 'scripts/build_exe.bat', which creates 'babal-win32.zip'.

License:
    
    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation; either version 2 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
