gen - number of generations the simulation will run for, default 100
le - number of learning episodes for each generations, default 100
mc - number of Monte Carlo sampled trials to determine communicative accuracy, default 500
report - number of learning episodes between trial rounds, default 10
meanings - number of possible meanings, default 5
signals - number of possible signals, default 5
filename - name for the file the results are written to, default 'test.txt'
acquisition - whether to run the acquisition simulation or not, default False
type - only relevant if acquisition = False, initialises population either with an optimal language ('optimal') or no language ('random'), default 'optimal'
restrict - removes agents that don't belong in the specified category (either 'learners', 'maintainers' or 'constructors'), default None
context - how many additional meanings are present during each learning episode, default 1
noise - the chance that in any given learning episode, the signal is wrong