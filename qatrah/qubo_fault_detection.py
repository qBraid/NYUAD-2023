from pyqubo import Binary

lambdaPath = 5

H = 0
L = [0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,1]

P = [[], [1, 2, 6], [1, 2, 7], [1, 2, 8], [1, 2, 9], [1, 3, 10], [1, 3, 11], [1, 3, 12], [1, 3, 13], [1, 4, 14], [1, 4, 15],
     [1, 4, 16], [1, 4, 17], [1, 5, 18], [1, 5, 19], [1, 5, 20], [1, 5, 21]]


for l in L:
    for y in range(1, 17):
        if l == 1:
            H+= lambdaPath * Binary('y'+str(y)) * len(P[y])
            for x in P[y]:
                H+= -lambdaPath * Binary('y'+str(y)) * Binary('x'+str(x))
        else:
            H+= lambdaPath*Binary('y'+str(y))*((1-len(P[y]))**2)
            for x in P[y]:
                H+= lambdaPath*Binary('y'+str(y))*(Binary('x'+str(x))**2) + 2*lambdaPath*Binary('y'+str(y))*(1-len(P[y]))*Binary('x'+str(x))
                for j in P[y]:
                    if x<j:
                        H+= 2*lambdaPath*Binary('y'+str(y))*Binary('x'+str(x))*Binary('x'+str(j))


for y in range(1, 17):
    H+= 1-Binary('y'+str(y))

for x in range(1, 22):
    H+= 1-Binary('x'+str(x))


model = H.compile()
bqm = model.to_bqm()

import neal
sa = neal.SimulatedAnnealingSampler()
sampleset = sa.sample(bqm, num_reads=10)
decoded_samples = model.decode_sampleset(sampleset)
best_sample = min(decoded_samples, key=lambda x: x.energy)

print(best_sample.sample)
