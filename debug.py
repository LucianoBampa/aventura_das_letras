class Debug:
	def __init__(self, debug=False):
		self.debug = debug

	def enable(self):
		self.debug = True
		print("DEBUG ON")
	
	def disable(self):
		self.debug = False
		print("DEBUG OFF")

	def print_debug(self, s, arquivo = ""):
		#chamada padrao = debug.print_debug(info, __name__)
		if self.debug:
			print(f"[{arquivo}] -- {s}")
	

debug = Debug() #objeto a ser exportado entre os arquivos
	

