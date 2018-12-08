class Item:
	def __init__(self, use_function=None, targeting=None, targeting_message=None, **kwargs):
		self.use_function = use_function
		self.function_kwargs = kwargs
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.owner = None