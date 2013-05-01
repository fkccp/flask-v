import time
from datetime import datetime

class J:
	@staticmethod
	def fromNow(ctime):
		delta = datetime.utcnow() - ctime
		delta = delta.seconds
		return ('%ds before' % delta)

	@staticmethod
	def floorSign(index):
		return ('Floor : %d' % index)