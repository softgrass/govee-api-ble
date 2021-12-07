import os

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
			os.system("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n 3301010000000000000000000000000000000033".format(self.mac))
			return True, status
		if status == False:
			os.system("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n 3301000000000000000000000000000000000032".format(self.mac))
			return True, status
		return False, status

	def setColor(self, c: list):
		"""
		Sets the color of the entire light strip
		c - List of three integers representing RGB values
		Usage - my_device.setColor([255,0,0])
		"""
		if not isinstance(c, list) or len(c) is not 3:
			raise TypeError
		for v in c:
			if not isinstance(v,int):
				raise TypeError
			if not (v >= 0 and v <= 255):
				raise ValueError
		hex_c = [hex(v) if len(hex(v)) is 4 else hex(v)[0:2]+"0"+hex(v)[2:] for v in c]
		packet = '0x33 0x05 0x02 {0} {1} {2} 0x00 0xFF 0xAE 0x54 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00'.format(*hex_c)
		packet_l = [chr(int(x, 16)) for x in packet.split(' ')]
		checksum = 0
		for el in packet_l:
			checksum ^= ord(el)
		cs_p = packet.replace("0x","")
		cs_p = cs_p.replace(" ","") + hex(checksum).replace("0x","")
		cs_p = cs_p.upper()
		os.system("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n {}".format(self.mac,cs_p))
		return True, c

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
		os.system("gatttool -i hci0 -b {} --char-write-req -a 0x0015 -n {}".format(self.mac,cs_p))
