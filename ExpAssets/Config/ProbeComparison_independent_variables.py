from klibs.KLIndependentVariable import IndependentVariableSet


# Initialize object containing project's factor set

ProbeComparison_ind_vars = IndependentVariableSet()


# Define project variables and variable types

## Factors ##
# 'is_target': whether the trial is a n-back target trial or not

ProbeComparison_ind_vars.add_variable('is_target', bool, [True, (False, 5)])
