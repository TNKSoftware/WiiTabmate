import time

class keydata:
	UP = 4
	DOWN = 0
	LEFT = 2
	RIGHT = 6
	UPLEFT = 3
	UPRIGHT = 5
	DOWNLEFT = 1
	DOWNRIGHT = 7
	Button1 = 8
	Button2 = 16

	def __init__(self, name, pos, repeat, *keys):
		self.name = name
		self.pos = pos
		self.repeat = repeat
		self.keys = keys
		self.key_first_repeat = False
		self.timer_last = 0
	
	def beginRepeat(self):
		self.key_first_repeat = True
		self.timer_last = time.time()

	def execRepeat(self):
		if not self.isKeyRepeat():
			return
		
		ctime = time.time()
		repi = 1.0 if self.key_first_repeat else self.repeat
		if ctime - self.timer_last > repi:
			self.keyPress()
			self.key_first_repeat = False
			self.timer_last = ctime

	def isKeyRepeat(self):
		return self.repeat > 0

	def keyDown(self):
		for key in self.keys:
			keyboard.setKeyDown(key)
			#diagnostics.debug("KeyDown:{}".format(k))

	def keyUp(self):
		for key in reversed(self.keys):
			keyboard.setKeyUp(key)
			#diagnostics.debug("KeyUp:{}".format(k))

	def keyPress(self):
		self.keyDown()
		self.keyUp()


def findKeyData(pos):
	global klist
	if pos < 0 or pos >= len(klist):
		return None
	else:
		return klist[pos]

def initKeys(jd):
	global klist

	UP = keydata.UP
	DOWN = keydata.DOWN
	LEFT = keydata.LEFT
	RIGHT = keydata.RIGHT
	UPLEFT = keydata.UPLEFT
	UPRIGHT = keydata.UPRIGHT
	DOWNLEFT = keydata.DOWNLEFT
	DOWNRIGHT = keydata.DOWNRIGHT
	Ctrl = Key.LeftControl
	Shift = Key.LeftShift
	B1 = keydata.Button1
	B2 = keydata.Button2

	# Clip Studioでのショートカット例
	# 名前, スティックの方向とボタンの組み合わせ, 
	#   繰り返し入力のタイミング(秒), キー1, キー2...
	_klist = [
		keydata("undo", LEFT, 0, Ctrl, Key.Z),
		keydata("redo", RIGHT, 0, Ctrl, Key.Y),
		keydata("brush+", UP, 0.2, Key.RightBracket),
		keydata("brush-", DOWN, 0.2, Key.Backslash),

		keydata("Hand", B2 + UP, 0, Key.Space),
		keydata("Zoom", B2 + LEFT, 0, Ctrl, Key.Space),
		keydata("Rotate", B2 + RIGHT, 0, Key.R),
		keydata("Reset", B2 + DOWN, 0, Ctrl, Key.LeftBracket),

		keydata("Pen", B1 + UP, 0, Key.P),
		keydata("Eraser", B1 + DOWN, 0, Key.E),
		keydata("Brush", B1 + UPLEFT, 0, Key.B),
		keydata("Fill", B1 + UPRIGHT, 0, Key.G),
		keydata("Select", B1 + LEFT, 0, Key.M),
		keydata("ClearSel", B1 + RIGHT, 0, Ctrl, Key.M),
		keydata("InvertSel", B1 + DOWNLEFT, 0, Ctrl, Shift, Key.I),
		keydata("SelAll", B1 + DOWNRIGHT, 0, Ctrl, Key.A)
	]

	''' Kritaでのショートカット例
	_klist = [
		keydata("undo", LEFT, 0, Ctrl, Key.Z),
		keydata("redo", RIGHT, 0, Ctrl, Shift, Key.Z),
		keydata("brush+", UP, 0.2, Key.RightBracket),
		keydata("brush-", DOWN, 0.2, Key.Backslash),

		keydata("Hand", B2 + UP, 0, Key.Space),
		keydata("Zoom", B2 + LEFT, 0, Ctrl, Key.Space),
		keydata("Rotate", B2 + RIGHT, 0, Shift, Key.Space),
		keydata("Reset", B2 + DOWN, 0, Key.D5),

		keydata("Pen", B1 + UP, 0, Key.P),
		keydata("Eraser", B1 + DOWN, 0, Key.E),
		keydata("Brush", B1 + UPLEFT, 0, Key.B),
		keydata("Fill", B1 + UPRIGHT, 0, Key.G),
		keydata("Select", B1 + LEFT, 0, Key.R),
		keydata("ClearSel", B1 + RIGHT, 0, Ctrl, Shift, Key.A),
		keydata("InvertSel", B1 + DOWNLEFT, 0, Ctrl, Shift, Key.I),
		keydata("SelAll", B1 + DOWNRIGHT, 0, Ctrl, Key.A)
	]
	'''

	for k in _klist:
		klist[k.pos] = k


def update():
	global n, lastpos, klist

	# スティックの遊び(20%)
	DISTANCE = 0.2
	# スティックの認識角度(前後15°)
	ANGLEIDLE = 15

	sx = n.stick.x
	sy = n.stick.y

	# ヌンチャクスティックの範囲は0~100なのでここで調整
	# ゲームパッドによってはこの値は1000にする
	DISTANCE *= 100

	dist = math.sqrt(sx * sx + sy * sy)
	
	pos = -1
	if dist > DISTANCE:
		angle = math.atan2(sx, sy) * 180 / math.pi + 180

		for i in range(9):
			if abs(angle - i * 45) < ANGLEIDLE:
				pos = i % 8
				if n.buttons.button_down(NunchuckButtons.C):
					pos += 8				
				if n.buttons.button_down(NunchuckButtons.Z):
					pos += 16

	if pos == lastpos:
		return

	if lastpos != pos:
		k = findKeyData(lastpos)
		if k is not None:
			k.keyUp()
	
	k = findKeyData(pos)
	if k is not None:
		if k.isKeyRepeat():
			k.beginRepeat()
			k.keyPress()
		else:
			k.keyDown()

	lastpos = pos

if starting:
	klist = [None] * 32
	initKeys(klist)

	lastpos = -1

	n = wiimote[0].nunchuck
	n.update += update

	diagnostics.debug("Hello!")

k = findKeyData(lastpos)
if k is not None:
	k.execRepeat()
