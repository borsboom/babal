import time
import math
from MotionPhysics import MotionPhysics

_BALL_X_ACCEL = 4.0
_BALL_X_BRAKE_FACTOR = 5.0
_BALL_Z_ACCEL = 1.0
_BALL_Z_BRAKE_FACTOR = 7.0
_BALL_JUMP_VELOC = 2.0
_BALL_JUMP_GRAVITY = -2.0

_BALL_RADIUS = 0.2
_BALL_ROTATE_FACTOR = 360.0 / (2 * math.pi * _BALL_RADIUS)

class Game:
    
    def __init__(self, map_file=None):
        self._load_map(map_file)
        
        self._cur_time = 0.0
        self.ball_radius = _BALL_RADIUS
        self._paused = 0

        self._left_pressed = 0
        self._right_pressed = 0        
        self._ball_x_motion = MotionPhysics(self._cur_time)
        def x_v_zero_cb(self=self, xm=self._ball_x_motion):
            if self._right_pressed:
                xm.a = _BALL_X_ACCEL
            elif self._left_pressed:
                xm.a = -_BALL_X_ACCEL
            else:
                xm.a = 0.0
            xm.recalc()
        self._ball_x_motion.set_veloc_zero_callback(x_v_zero_cb)
        self._ball_x_motion.d = self._find_initial_row_ball_x_z(0)[0]
        self._ball_x_motion.recalc()
        self.ball_x = self._ball_x_motion.d

        self._jump_pressed = 0
        self._ball_y_motion = MotionPhysics(self._cur_time)        
        def y_d_zero_cb(ym=self._ball_y_motion):
            ym.a = 0.0
            ym.v = 0.0
            ym.d = 0.0
            ym.recalc()
        self._ball_y_motion.set_dist_zero_callback(y_d_zero_cb)
        self.ball_y = 0.0

        self._accel_pressed = 0
        self._decel_pressed = 0
        self._ball_z_motion = MotionPhysics(self._cur_time)
        def z_v_zero_cb(self=self, zm=self._ball_z_motion):
            if self._accel_pressed:
                zm.a = _BALL_Z_ACCEL
            elif self._decel_pressed:
                zm.a = -_BALL_Z_ACCEL
            else:
                zm.a = 0.0
            zm.v = 0.0
            zm.recalc()
        self._ball_z_motion.set_veloc_zero_callback(z_v_zero_cb)
        self.ball_z = 0.0
        self.ball_x_rotate = 0.0

        self._frame_count = 0
        self._frame_count_time = 0.0

        def status_callback(status):
            print status
        self.status_callback = status_callback

        self.reset_timer()        

    def reset_timer(self):
        self._prev_update_real_time = time.time()

    def _load_map(self, f=None):
        if not f:
            f = open('data/default.map')
        f.read(18)
        map = []
        b = f.read(1)
        i = 0
        while len(b) > 0: # and i < 10:
            x = ord(b)
            r = []
            for j in range(0, 8):
                r.append((x & (1 << j)) >> j)
            map.append(r)
            b = f.read(1)
            i += 1
        f.close()
        self.map_width = 8
        self.map = map

    def _move_ball(self):       
        self._ball_x_motion.update(self._cur_time)
        self.ball_x = self._ball_x_motion.d
        
        self._ball_y_motion.update(self._cur_time)
        self.ball_y = self._ball_y_motion.d

        old_z = self.ball_z
        self._ball_z_motion.update(self._cur_time)
        self.ball_z = self._ball_z_motion.d
        self.ball_x_rotate = ( self.ball_x_rotate + (self.ball_z - old_z) * _BALL_ROTATE_FACTOR ) % 360.0

    def _get_ball_col_idx(self):
        return int(math.floor(self.ball_x + 0.5 + math.floor((self.map_width-1) / 2.0)))

    def _get_ball_row_idx(self):
        return int(math.floor(self.ball_z + 0.5))

    def _col_idx_to_ball_x(self, col_idx):
        return col_idx - math.floor((self.map_width-1) / 2.0) - 0.5

    def _row_idx_to_ball_z(self, row_idx):
        return float(row_idx)

    def _detect_crash(self):
        if self.ball_y > 0.0:
            return 0
        col_i = self._get_ball_col_idx()
        row_i = self._get_ball_row_idx()
        crash = 0
        if row_i >= len(self.map):
            return 0
        if row_i < 0:
            return 1
        col = self.map[row_i]
        if col_i < 0 or col_i >= len(col):
            return 1
        return not col[col_i]

    def _find_initial_row_ball_x_z(self, row_idx):
        while row_idx < len(self.map):
            row = self.map[row_idx]
            i = 0
            found_start = 0
            for c in row:
                if not found_start:
                    if c:
                        start = self._col_idx_to_ball_x(i)
                        found_start = 1
                else:
                    if not c:
                        end = self._col_idx_to_ball_x(i)
                        return ((start + end) / 2.0,
                                self._row_idx_to_ball_z(row_idx))
                i += 1
            row_idx += 1
        return 0.0, self._row_idx_to_ball_z(row_idx)

    def _handle_crash(self):
        row_idx = self._get_ball_row_idx() - 64
        if row_idx < 0:
            row_idx = 0
        self._ball_x_motion.d, self._ball_z_motion.d = (
            self._find_initial_row_ball_x_z(row_idx))

        self._ball_z_motion.v = 0.0
        self._ball_z_motion.a = 0.0
        self._ball_z_motion.recalc()
        self.ball_z = self._ball_z_motion.d

        self._ball_x_motion.v = 0.0
        self._ball_x_motion.a = 0.0
        self._ball_x_motion.recalc()
        self.ball_x = self._ball_x_motion.d

    def update(self):
        real_time = time.time()
        elapsed_time = real_time - self._prev_update_real_time
        self._prev_update_real_time = real_time

        self._frame_count_time += elapsed_time
        self._frame_count += 1
        while self._frame_count_time >= 1.0:
            self.status_callback('FPS: ' + str(self._frame_count))
            self._frame_count = 0
            self._frame_count_time -= 1.0

        if self._paused:
            return

        self._cur_time += elapsed_time

        self._move_ball()
        if self._detect_crash():
            self._handle_crash()

    def begin_accel(self):
        if self._accel_pressed:
            return
        self._accel_pressed = 1
        self._decel_pressed = 0
        if self._ball_z_motion.v < 0.0:
            self._ball_z_motion.a = _BALL_Z_ACCEL * _BALL_Z_BRAKE_FACTOR
        else:
            self._ball_z_motion.a = _BALL_Z_ACCEL
        self._ball_z_motion.recalc()

    def end_accel(self):
        if not self._accel_pressed:
            return
        self._accel_pressed = 0
        self._ball_z_motion.a = 0.0
        self._ball_z_motion.recalc()

    def begin_decel(self):
        if self._decel_pressed:
            return
        self._decel_pressed = 1
        self._accel_pressed = 0
        if self._ball_z_motion.v > 0.0:
            self._ball_z_motion.a = -_BALL_Z_ACCEL * _BALL_Z_BRAKE_FACTOR
        else:
            self._ball_z_motion.a = -_BALL_Z_ACCEL
        self._ball_z_motion.recalc()

    def end_decel(self):
        if not self._decel_pressed:
            return
        self._decel_pressed = 0
        self._ball_z_motion.a = 0.0
        self._ball_z_motion.recalc()
        
    def begin_left(self):
        if self._left_pressed:
            return
        self._left_pressed = 1
        self._right_pressed = 0
        if self._ball_x_motion.v > 0.0:
            self._ball_x_motion.a = -_BALL_X_ACCEL * _BALL_X_BRAKE_FACTOR
        else:
            self._ball_x_motion.a = -_BALL_X_ACCEL
        self._ball_x_motion.recalc()

    def end_left(self):
        if not self._left_pressed:
            return
        self._left_pressed = 0
        if self._ball_x_motion.v < 0.0:
            self._ball_x_motion.a = _BALL_X_ACCEL
            self._ball_x_motion.recalc()

    def begin_right(self):
        if self._right_pressed:
            return
        self._right_pressed = 1
        self._left_pressed = 0
        if self._ball_x_motion.v < 0.0:
            self._ball_x_motion.a = _BALL_X_ACCEL * _BALL_X_BRAKE_FACTOR
        else:
            self._ball_x_motion.a = _BALL_X_ACCEL
        self._ball_x_motion.recalc()

    def end_right(self):
        if not self._right_pressed:
            return
        self._right_pressed = 0
        if self._ball_x_motion.v > 0.0:
            self._ball_x_motion.a = -_BALL_X_ACCEL
            self._ball_x_motion.recalc()

    def begin_jump(self):
        if self._jump_pressed:
            return
        self._jump_pressed = 1
        if self._ball_y_motion.d <= 0.0:
            self._ball_y_motion.v = _BALL_JUMP_VELOC
            self._ball_y_motion.a = _BALL_JUMP_GRAVITY
            self._ball_y_motion.recalc()

    def end_jump(self):
        self._jump_pressed = 0

    def toggle_pause(self):
        self._paused = not self._paused
