import io
import math

class Packet():

	def __init__(self):

		#to be installed by the factory
		#Should I make 2 subclasses 1 with each type of thing? who cares?
		self.subpackets = None
		self.value = None
		self.version = None
		self.typeID = None
		self.length = None


	def sum_versions(self):

		total_version = self.version

		if self.subpackets is None:
			return total_version

		for subpacket in self.subpackets:

			total_version += subpacket.sum_versions()

		return total_version


	def do_calculation(self):

		#base case
		if self.value is not None:
			return self.value

		subpacket_values = []

		for subpacket in self.subpackets:

			subpacket_values.append(subpacket.do_calculation())

		if self.typeID == 0:
			return sum(subpacket_values)

		elif self.typeID == 1:
			return math.prod(subpacket_values)

		elif self.typeID == 2:
			return min(subpacket_values)

		elif self.typeID == 3:
			return max(subpacket_values)

		elif self.typeID == 5:
			return subpacket_values[0] > subpacket_values[1]

		elif self.typeID == 6:
			return subpacket_values[0] < subpacket_values[1]

		elif self.typeID == 7:
			return subpacket_values[0] == subpacket_values[1]


	@classmethod
	def PacketFactory(cls, bininput):

		packet = Packet()	

		packet.version = Packet._GetVersion(bininput)	
		packet.typeID = Packet._GetTypeID(bininput)


		#base case
		if packet.typeID == 4:		
			
			packet.value, number_bits_value = Packet._GetValue(bininput)
			packet.length = 6 + number_bits_value #6 for version and type ID
			
			return packet


		#recursion cases
		packet.subpackets = []

		lengthTypeID = Packet._GetLengthTypeID(bininput)

		number_bits_subpacket = 0
		number_subpackets = 0

		#case where subpackets have an exact number of bits
		if lengthTypeID == '0':
			number_bits_subpacket = Packet._GetSubPacketBits(bininput)
			packet.length = 22 #22 for version and type ID and length type id +bits length of subpackets
		else:
			number_subpackets = Packet._GetSubPacketNumber(bininput)
			packet.length = 18 #18 for version and type ID and length type id +bits number of subpackets

		#generate subpackets until we run out of bits to check or have generated the correct number of packets		
		while (number_bits_subpacket > 0) or (number_subpackets > 0):

			subpacket = Packet.PacketFactory(bininput[packet.length:])
			
			packet.subpackets.append(subpacket)
			packet.length += subpacket.length

			number_bits_subpacket -= subpacket.length
			number_subpackets -= 1
			

		return packet


	@classmethod
	def _GetVersion(cls, bininput):

		bin_version = bininput[0:3]
		version = int(bin_version,2)

		return version


	@classmethod
	def _GetTypeID(cls, bininput):

		bin_typeID = bininput[3:6]
		typeID = int(bin_typeID,2)
		
		return typeID


	@classmethod
	def _GetLengthTypeID(cls, bininput):

		return bininput[6]


	@classmethod
	def _GetValue(cls, bininput):

		packet_bin_value = bininput[6:]

		bin_value = ''
		number_bits_value = 0
		read_more = True

		while read_more:	
			read_more = packet_bin_value[0] == '1' #keep reading if we are not at the last value
			bin_value += packet_bin_value[1:5] #get bits
			packet_bin_value = packet_bin_value[5:]
			number_bits_value += 5

		value = int(bin_value,2)

		return value, number_bits_value


	@classmethod 
	def _GetSubPacketBits(cls, bininput):

		bin_number_subpacket_bits = bininput[7:22]
		number_subpacket_bits = int(bin_number_subpacket_bits, 2)

		return number_subpacket_bits


	@classmethod
	def _GetSubPacketNumber(cls, bininput):

		bin_number_subpackets = bininput[7:18]
		number_subpackets = int(bin_number_subpackets, 2)

		return number_subpackets


def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		hexstring = input_stream.readline().strip()

		binstring = bin(int(hexstring, 16))[2:]
		while len(binstring) % 4 != 0:
			binstring = '0' + binstring

	return binstring
		
	
fname = "input16.txt"
binstring = load_stuff(fname)
packet_root = Packet.PacketFactory(binstring)
sum_all_versions = packet_root.sum_versions()
print(sum_all_versions)
answer = packet_root.do_calculation()
print(answer)
