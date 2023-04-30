from pyqubo import Binary
import neal
import igraph
from igraph import Graph, EdgeSeq



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

