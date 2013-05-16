Collaborators: 
	Tanner Missler
	Dwight Hohnstein
	Jessica Junk

Project:
	Clean up documentation for all modules under sage/logic and add it to the reference manual. 
	This includes mostly to changing the adhoc documentation to the required Sphinx format.
	Related ticket numbers are as follows:
	#8790 - 
		Missing documentation:
			 * combine(self, statement1, statement2):
			 * simplify(self, table):
			 * prove(self, statement):


		Missing doctests:
			 * get_bit(x, c):
			 * eval(toks):
			 * eval_ltor_toks(lrtoks):
			 * reduce_bins(lrtoks):
			 * reduce_monos(lrtoks):
			 * eval_mon_op(args):
			 * eval_bin_op(args):
			 * eval_and_op(lval, rval):
			 * eval_or_op(lval, rval):
			 * eval_ifthen_op(lval, rval):
			 * eval_iff_op(lval, rval):
			 * tokenize(s, toks):
	#8793 - 
		Clean up documentation for logic/boolformula.py
	#8794 -
		Clean up documentation for logic/logicparser.py
	#8795 - 
		Clean up documentation for logic/logictable.py