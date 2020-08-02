
class Connection:

	active = False

	target = None

	@staticmethod
	def reset():
		Connection.target = None

