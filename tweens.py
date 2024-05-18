def ease_in_out(x):
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - pow(-2 * x + 2, 3) / 2

# A tween that does nothing but wait
class WaitTween:
    def __init__(self, time):
        self.time = time
        self.t = 0

    def update(self, dt):
        self.t += dt / self.time
        return self.t >= 1

# A tween that move the obj from the current position to target
class PosTween:
    def __init__(self, obj, target, time):
        self.obj = obj
        self.target = target
        self.time = time
        self.t = 0

    def update(self, dt):
        # Cache the start position in the first update
        if self.t == 0:
            self.start = self.obj.position
        
        self.t += dt / self.time
        if self.t >= 1:
            self.t = 1
        r = ease_in_out(self.t)
        px = self.start[0] + r * (self.target[0] - self.start[0])
        py = self.start[1] + r * (self.target[1] - self.start[1])
        self.obj.position = px, py
        return self.t >= 1

# A tween that rotate the obj from the current angle to target
class RotTween:
    def __init__(self, obj, target, time):
        self.obj = obj
        self.target = target
        self.time = time
        self.t = 0

    def update(self, dt):
        # Cache the start angle in the first update
        if self.t == 0:
            self.start = self.obj.rotation
            delta_angle = (self.target - self.start) % 360
            if delta_angle > 180:
                delta_angle -= 360
            self.target = self.start + delta_angle
        
        self.t += dt / self.time
        if self.t >= 1:
            self.t = 1
        r = ease_in_out(self.t)
        self.obj.rotation = self.start + r * (self.target - self.start)
        return self.t >= 1

# A tween that print stuff
class PrintTween:
    def __init__(self, string):
        self.string = string

    def update(self, _):
        print(self.string)
        return True