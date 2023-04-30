from pyqubo import Binary
import neal



# H = 0
# sensor_readings = [0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,1]

#P = [[], [1, 2, 6], [1, 2, 7], [1, 2, 8], [1, 2, 9], [1, 3, 10], [1, 3, 11], [1, 3, 12], [1, 3, 13], [1, 4, 14], [1, 4, 15],
#      [1, 4, 16], [1, 4, 17], [1, 5, 18], [1, 5, 19], [1, 5, 20], [1, 5, 21]]


# for l in sensor_readings:
#     for y in range(1, 17):
#         if l == 1:
#             H+= lambdaPath * Binary('y'+str(y)) * len(P[y])
#             for x in P[y]:
#                 H+= -lambdaPath * Binary('y'+str(y)) * Binary('x'+str(x))
#         else:
#             H+= lambdaPath*Binary('y'+str(y))*((1-len(P[y]))**2)
#             for x in P[y]:
#                 H+= lambdaPath*Binary('y'+str(y))*(Binary('x'+str(x))**2) + 2*lambdaPath*Binary('y'+str(y))*(1-len(P[y]))*Binary('x'+str(x))
#                 for j in P[y]:
#                     if x<j:
#                         H+= 2*lambdaPath*Binary('y'+str(y))*Binary('x'+str(x))*Binary('x'+str(j))


# for y in range(1, 17):
#     H+= 1-Binary('y'+str(y))

# for x in range(1, 22):
#     H+= 1-Binary('x'+str(x))


# model = H.compile()
# bqm = model.to_bqm()

# import neal
# sa = neal.SimulatedAnnealingSampler()
# sampleset = sa.sample(bqm, num_reads=10)
# decoded_samples = model.decode_sampleset(sampleset)
# best_sample = min(decoded_samples, key=lambda x: x.energy)

# print(best_sample.sample)


def read_input():
    sensor_file = open("sensor_readings.txt", "r")
    sensor_readings = []
    sensor_readings.append(1)
    sensor_readings.extend([int(x) for x in next(sensor_file).split(',')])

    paths_file = open("paths.txt", "r")
    number_of_nodes = int(next(paths_file))
    paths = [[]]
    for line in paths_file:
        paths.append([int(x) for x in line.split(',')])

    return sensor_readings, paths, number_of_nodes


def create_optimization_function(sensor_readings, paths, number_of_nodes):
    H = 0
    number_of_sensors = len(sensor_readings) - 1
    lambdaPath = 3
    # Add H consistent
    for y in range(1, number_of_sensors+1):
        l = sensor_readings[y]
        # for y in range(1, number_of_sensors+1):
        if l == 1:
            H+= (lambdaPath * Binary('y'+str(y)) * len(paths[y]))
            for x in paths[y]:
                H+= (-lambdaPath * Binary('y'+str(y)) * Binary('x'+str(x)))
        else:
            H+= (lambdaPath*Binary('y'+str(y))*((1-len(paths[y]))**2))
            for x in paths[y]:
                H+= (lambdaPath*Binary('y'+str(y))*(Binary('x'+str(x))**2) + 2*lambdaPath*Binary('y'+str(y))*(1-len(paths[y]))*Binary('x'+str(x)))
                for j in paths[y]:
                    if x<j:
                        H+= (2*lambdaPath*Binary('y'+str(y))*Binary('x'+str(x))*Binary('x'+str(j)))

    # Add H numFaults
    for y in range(1, number_of_sensors+1):
        H+= (1-Binary('y'+str(y)))

    for x in range(1, number_of_nodes+1):
        H+= (1-Binary('x'+str(x)))

    return H


def print_variables(best_sample):
    Nodes = {}
    Sensors = {}
    for key in best_sample:
        if "*" in key:
            if best_sample[key] == 0:
                pass
            key1, key2 = [x for x in key.split(" * ")]
            if "x" in key1:
                Nodes[key1] = best_sample[key]
            else:
                Sensors[key1] = best_sample[key]
            if "x" in key2:
                Nodes[key2] = best_sample[key]
            else:
                Sensors[key2] = best_sample[key]
        else:
            if "x" in key:
                Nodes[key] = best_sample[key]
            else:
                Sensors[key] = best_sample[key]
    
    print("Node Values:")
    for key in Nodes:
        print(key, ": ", Nodes[key])
    
    print("Sensor Values:")
    for key in Sensors:
        print(key, ": ", Sensors[key])


if __name__ == '__main__':
    # Read the input
    sensor_readings, paths, number_of_nodes = read_input()

    # Create optimization function
    H = create_optimization_function(sensor_readings, paths, number_of_nodes)

    # Create model
    model = H.compile()
    bqm = model.to_bqm()

    # Get the best samples
    sa = neal.SimulatedAnnealingSampler()
    sampleset = sa.sample(bqm, num_reads=10)
    decoded_samples = model.decode_sampleset(sampleset)
    best_sample = min(decoded_samples, key=lambda x: x.energy)

    # Print the binary variables values
    # print(best_sample.sample)
    print_variables(best_sample.sample)

