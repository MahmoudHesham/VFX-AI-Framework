import importlib
import sys
import os

class MLSolutions:
	'''
		this object will contain all the machine-learning solutions being automatically 
		imported from solutions directory. could also handle different type of solutions
		that is not machine-learning related but a new object has to be defined and initialized.
	'''

	def __init__(self):

		modules = self.get_modules()
		self.register(modules)

	def get_modules(self):
		
		modules_dir = os.path.dirname(__file__)
		sys.path.append(modules_dir)

		ignored_modules = ["__init__.py"]
		modules = [x[:-3] for x in os.listdir(modules_dir) if x.endswith(".py") and x not in ignored_modules]
		
		return modules

	def register(self, modules:list):

		for module in modules:

			print(f"[Importing Module] -> {module}")
			self.__dict__[module] = importlib.import_module(module)