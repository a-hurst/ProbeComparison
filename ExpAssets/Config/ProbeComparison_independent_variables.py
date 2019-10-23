from klibs.KLIndependentVariable import IndependentVariableSet


# Initialize object containing project's factor set

ProbeComparison_ind_vars = IndependentVariableSet()


# Define project variables and variable types

ProbeComparison_ind_vars.add_variable('number', int, [1, 2, 3, 4, 5, 6, 7, 8, 9])
