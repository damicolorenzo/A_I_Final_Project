class Displayable(object):
	max_display_level = 4 

	def display(self,level,*args,**nargs):
		if level <= self.max_display_level:
			print(*args, **nargs) 

def visualize(func):
	return func



