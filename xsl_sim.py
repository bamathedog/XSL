import random
import time

def reception_weights(system, signal):
    weights = []
    for row in system:
        weights.append(row[signal])
    return weights

def production_weights(system, meaning):
    return system[meaning]

def wta(items):
    maxweight = max(items)
    candidates = []
    for i in range(len(items)):
        if items[i] == maxweight:
            candidates.append(i)
    return random.choice(candidates)


def communicate(speaker_system, hearer_system, meaning):
    speaker_signal = wta(production_weights(speaker_system,meaning))
    hearer_meaning = wta(reception_weights(hearer_system,speaker_signal))
    if meaning == hearer_meaning: 
        return 1
    else: 
        return 0

def ca_monte(speaker_system, hearer_system, trials):
    total = 0.
    for n in range(trials):
        total += communicate(speaker_system, hearer_system,
                             random.randrange(len(speaker_system)))
    return total / trials

def ca_monte_pop(population, trials):
    total = 0.
    for n in range(trials):
        speaker = random.choice(population)
        hearer = random.choice(population)
        total += communicate(speaker, hearer, random.randrange(len(speaker)))
    return total / trials

# add random context to target meaning m
def add_context(meanings, m, context):
    m_list = range(meanings)
    if m in m_list:
        m_list.remove(m)
    random.shuffle(m_list) # randomizes list of non-target meanings
    context = m_list[ : context] # take first however many
    context.append(m) # add back in target meaning
    return context
    
def add_noise(s, signals, noise):
    s_list = range(signals)
    if s in s_list:
        s_list.remove(s)
    random.choice(s_list)

# produce a single data item from speaker_system
def produce_data(speaker_system, context, noise):
    meaning = random.randrange(len(speaker_system))
    signal = wta(production_weights(speaker_system,meaning))
    c = add_context(len(speaker_system), meaning, context)
    if random.random < noise:
        add_noise(s, len(speaker_system[0, noise]))
    return [c,signal]


# learn a signal paired with multiple meanings
def multiple_meaning_learn(system,meaning_list,signal,rule):
    for m in range(len(system)):
        for s in range(len(system[m])):
            if m in meaning_list and s == signal: system[m][s] += rule[0]
            if m in meaning_list and s != signal: system[m][s] += rule[1]
            if m not in meaning_list and s == signal: system[m][s] += rule[2]
            if m not in meaning_list and s != signal: system[m][s] += rule[3]
			
def pop_learn(population, data, no_learning_episodes, rule):
    for n in range(no_learning_episodes):
        ms_pair = random.choice(data)
        multiple_meaning_learn(random.choice(population), ms_pair[0], ms_pair[1], rule)

def new_agent(type, meanings, signals):
    system = []
    for i in range(meanings):
        row = []
        for j in range(signals):
            if type == 'optimal':
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            elif type == 'random':
                row.append(0)
        system.append(row)
    return system

def new_population(type, meanings, signals):
    population = []
    for i in range(100):
        population.append(new_agent(type, meanings, signals))
    return population	
    
def bias_perm():
    values = [1,0,-1]
    all = [[[a,b,c,d]] for a in values for b in values for c in values for d in values]
    for x in all:
        if x[0][0]+x[0][3] > x[0][1]+x[0][2]:
            x+=['+learner']	#for reporting
            if x[0][0] > x[0][1]:
                if x[0][3] >= x[0][2]:
                    x+=['+maintainer']
                    if x[0][3] > x[0][2]:
                        x+=['+constructor']
                    else:
                        x+=['-constructor']
                else:
                    x+='-maintainer','-constructor'
            else:
                x+='-maintainer','-constructor'
        else:
            x+='-learner','-maintainer','-constructor'
    return all
    
def xsl_simulation(adult, learner, learning_episodes, trials, report, rule, context, noise):
    data_accumulator = []
    for i in range(learning_episodes):
        utterance = produce_data(adult, context, noise)
        u = utterance[0]
        signal = utterance[1]
        multiple_meaning_learn(learner, u, signal, rule)
        if (i % report == 0):
            data_accumulator.append(ca_monte(adult, learner, trials))
    return [learner,data_accumulator]

def xsl_pop(population, le, trials, report, rule, context, noise):
    for i in range(le):
        a = random.choice(population)
        utterance = produce_data(a, context, noise)
        pop_learn(population, utterance, le, rule)
        if (i % report == 0):
            data_accumulator.append(ca_monte_pop(population, trials))
    return [learner,data_accumulator]

def xsl_gen(gen=100, le=100, mc=500, report=10, meanings=5, signals=5, filename='test.txt', acquisition=False, optimal=True, restrict=None, context=1, noise=0.):
    biases = bias_perm()
    if restrict == 'learners':
        biases2 = [b for b in biases if '+learner' in b]
        biases = biases2
    elif restrict == 'maintainers':
        biases2 = [b for b in biases if '+maintainer' in b]
        biases = biases2
    elif restrict == 'constructors':
        biases2 = [b for b in biases if '+constructor' in b]
        biases = biases2
    if optimal:
        type = 'optimal'
    else:
        type = 'random'
    population = new_population(type, meanings, signals)
    f = open(filename, 'w')
    f.write("Learner?\tMaintainer?\tConstructor?\tBias")
    for i in range(gen):
        q = i+1
        f.write("\t%d" % q)
    f.write("\n")
    if acquisition:
        adult = new_agent('optimal', meanings, signals)
        learner = new_agent('random', meanings, signals)
        for b in biases:
            for j in range(gen):
                f.write("%s\t%s\t%s\t%s" % (b[1], b[2], b[3],str(b[0])))
                b_res = xsl_simulation(adult,learner, le, mc, report, b[0], context, noise)
                for res in b_res[1]:
                    f.write("\t%f" % res)
                f.write("\n")
    else:
        for b in biases:
            f.write("%s\t%s\t%s\t%s" % (b[1], b[2], b[3],str(b[0])))
            for i in range(gen):
                b_res = xsl_pop(population, le, mc, report, b[0], context, noise)
                f.write("\t%s" % (b_res[1][-1]))
                adults = [x for x in b_res[0]]
                learner = new_agent('random', meanings, signals)
                adults.append(learner)
            f.write("\n")
    f.write("\n\n\tCross-situational Learning\n")
    f.write("\tGenerations:\t%d\n" % gen)
    f.write("\tReported every %d generations\n" % report)
    f.write("\tLearning episodes:\t%d\n" % le)
    f.write("\tMonte Carlo trials:\t%d\n" % mc)
    f.write("\tMeanings:\t%d\n" % meanings)
    f.write("\tSignals:\t%d\n" % signals)
    f.write("\tContext:\t%d\n" % context)
    f.write("\tNoise:\t%f\n" % noise)
    f.close()
