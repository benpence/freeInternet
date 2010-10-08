def extract(self, keywords, kwargs):
	"""
	extract(self, # Reference to object
			keywords, # dictioary of parameter names : default parameter values
			kwargs, # Keyword arguments passd to objet's __init__ method

		allows the developer to use keyword arguments for child __init__ as well as **kwargs for parent __init__
	"""

	for keyword in keywords:
		# Use passed keyword value
		if keyword in kwargs:
			exec "self.%s = kwargs.get('%s')" % (keyword, keyword)
			kwargs.pop(keyword)
		# Use default keyword value
		else:
			exec "self.%s = %s" % (keyword, keywords[keyword])
