COPYRIGHT='''Babal 2003.02.19
Copyright (C) 2003 Emanuel Borsboom (http://www.nuel.ca/)
Based on Babal for HP48 (http://www.ufoot.org/babal/) by U-Foot.
Map data by U-Foot (http://www.ufoot.org/) and Makoto Miyamoto

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
'''

print COPYRIGHT

try:
    from OpenGL import GL
    import pyopengl_main
    pyopengl_main.main()
except ImportError:
    from JGLBabalRunnable import JGLBabalRunnable
    JGLBabalRunnable().run()
