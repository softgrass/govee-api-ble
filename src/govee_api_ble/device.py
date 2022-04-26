import subprocess
import typing

scenes = {
	'sunrise': '3305040000000000000000000000000000000032',
	'sunset': '3305040100000000000000000000000000000033',
	'movie': '3305040400000000000000000000000000000036',
	'dating': '3305040500000000000000000000000000000037',
	'romantic': '3305040700000000000000000000000000000035',
	'blinking': '330504080000000000000000000000000000003a',
	'candlelight': '330504090000000000000000000000000000003b',
	'snowflake': '3305040f0000000000000000000000000000003d',
}
music = {
	'energic': '3305010000000000000000000000000000000037',
	'spectrum': '3305010100RRGGBB0000000000000000000000c9',
	'rolling': '3305010200RRGGBB0000000000000000000000ca',
	'rhythm': '3305010300000000000000000000000000000034',
}

class GoveeDevice:
	def __init__(self, mac):
		"""
		Initialize a device
		mac - the bluetooth MAC address for your light strip
		"""
		self.mac = mac
	
	def setPower(self, status):
		"""
		Turn lights on or off
		Only takes boolean (True/False) as argument
		Usage - my_device.setPower(true)
		"""
		if status == True:
			output = subprocess.check_output("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n 3301010000000000000000000000000000000033".format(self.mac), shell=True)
			return (output == b'Characteristic value was written successfully\n'), status, output
		if status == False:
			output = subprocess.check_output("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n 3301000000000000000000000000000000000032".format(self.mac), shell=True)
			return (output == b'Characteristic value was written successfully\n'), status, output
		return False, status
	
	def setColor(self, c: typing.List[int], segment: typing.List[int] = None):
		"""
		Sets the color of the entire light strip
		c - List of three integers representing RGB values
		segment - optional - List of the segments that should be changed [0-14] (15 segments)
		Usage - my_device.setColor([255,0,0])
		"""
		if segment is None:
			mode = "0x02"
			l, r = 0x00, 0xFF
		else:
			mode = "0x0b"
			l, r = 0, 0
			for i in segment:
				if not isinstance(i, int):
					raise TypeError
				elif i >= 15:
					raise ValueError # there are only 15 Segments (0-14)
				elif i >= 8:
					r ^= 2**(i-8)
				else:
					l ^= 2**i
		if len(c) is not 3:
			raise IndexError
		for v in c:
			if not isinstance(v, int):
				raise TypeError
			if not (v >= 0 and v <= 255):
				raise ValueError
		hex_c = [hex(v) if len(hex(v)) is 4 else hex(v)[0:2]+"0"+hex(v)[2:] for v in c]
		l = hex(l) if len(hex(l)) is 4 else hex(l)[0:2]+"0"+hex(l)[2:]
		r = hex(r) if len(hex(r)) is 4 else hex(r)[0:2]+"0"+hex(r)[2:]
		#packet = '0x33 0x05 0x02 {0} {1} {2} 0x00 0xFF 0xAE 0x54 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00'.format(*hex_c)
		packet = f"0x33 0x05 {mode} {hex_c[0]} {hex_c[1]} {hex_c[2]} {l} {r} 0xAE 0x54 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00"
		packet_l = [chr(int(x, 16)) for x in packet.split(' ')]
		checksum = 0
		for el in packet_l:
			checksum ^= ord(el)
		cs_p = packet.replace("0x","")
		cs_p = cs_p.replace(" ","") + hex(checksum).replace("0x","")
		cs_p = cs_p.upper()
		output = subprocess.check_output("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n {}".format(self.mac,cs_p), shell=True)
		return (output == b'Characteristic value was written successfully\n'), c, output
	
	def setBrightness(self,level: int):
		"""
		Sets the brightness of the light strip
		level - Level of brightness for strip, must be 0<= and >=100
		Usage - my_device.setBrightness(50)
		"""
		if not isinstance(level, int):
			raise TypeError
		if not (level >= 0 and level <= 100):
			raise ValueError
		level_u = round((level/100)*255)
		level_h = hex(level_u)
		level_xor = int("0x33",16)^int("0x04",16)^level_u
		level_xor_h = hex(level_xor)
		packet = '0x33 0x04 {} 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00'.format(level_h)
		cs_p = packet.replace("0x","")
		cs_p = cs_p.replace(" ","") + level_xor_h.replace("0x","")
		cs_p = cs_p.upper()
		output = subprocess.check_output("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n {}".format(self.mac,cs_p), shell=True)
		return (output == b'Characteristic value was written successfully\n'), level, output
	
	def setScene(self,setting):
		"""
		Sets the different scenes for the lights
		The looks of them can be found in the Govee app
		setting - Takes a string, type which mode you want (can be found in app or inside the 'scenes' list at the top of the code
		Usage - my_device.setScene("setting")
		"""
		output = subprocess.check_output("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n {}".format(self.mac,scenes[setting.lower()]), shell=True)
		return (output == b'Characteristic value was written successfully\n'), setting, output
	
	def setColorMusic(self,setting,c=[255,0,0]):
		"""
		Sets the music mode for the lights
		The settings for this can be found in the Govee app or in the 'music' list at the top of the code
		Spectrum mode accepts a list of RGB values after the setting
		setting - Takes a string, type which mode you want
		c - Only used for Spectrum or Rolling setting, accepts 3 int values as RGB values
		Usage - my_device.setColorMusic("setting")
				my_device.setColorMusic("spectrum",[R,G,B])
		"""
		if not isinstance(c, list) or len(c) is not 3:
			raise TypeError
		for v in c:
			if not isinstance(v,int):
				raise TypeError
			if not (v >= 0 and v <= 255):
				raise ValueError
		hex_c = [hex(v) if len(hex(v)) is 4 else hex(v)[0:2]+"0"+hex(v)[2:] for v in c]
		hex_x = [v.replace("0x","") for v in hex_c]
		rgb_c = ''.join(hex_x)
		pre_setting = music[setting.lower()]
		cur_setting = (pre_setting[:10] + rgb_c + pre_setting[16:]) if("RR" in pre_setting) else pre_setting
		output = subprocess.check_output("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n {}".format(self.mac,cur_setting), shell=True)
		return (output == b'Characteristic value was written successfully\n'), setting, c, output
