The simulation is intended to model cross-situational learning of language. Agents consist of a signalling matrix. During a learning episode, an agent is exposed to an utterance (a signal paired with both a target meaning and a number of additional meanings), and updates its signalling matrix weights according to the learning bias given.

Usage example:
xsl_gen(gen=100, le=100, mc=500, report=10, meanings=5, signals=5, filename='test.txt', acquisition=False, type='optimal', restrict=None, context=1, noise=0.)

gen (int) - number of generations the simulation will run for, default 100
le (int) - number of learning episodes for each generations, default 100
mc (int) - number of Monte Carlo sampled trials to determine communicative accuracy, default 500
report (int) - number of learning episodes between trial rounds, default 10
meanings (int) - number of possible meanings, default 5
signals (int) - number of possible signals, default 5
filename (str) - name for the file the results are written to, default 'test.txt'
acquisition (bool) - whether to run the acquisition simulation or not, default False.
optimal (bool) - only relevant if acquisition = False, initialises population either with an optimal language or zero connection weights in their signalling matrix, default True.
restrict - removes agents that don't belong in the specified category (either 'learners', 'maintainers' or 'constructors'), default None. Useful for cutting down simulation runtime.
context (int) - how many additional meanings are present during each learning episode, default 1
noise (float) - the chance that in any given learning episode, the signal is wrong, default 0.