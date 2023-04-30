from TDA import get_topology_gudhi
import numpy as np
from scipy.sparse import coo_matrix
import os

class TopologyTransformer:
    def __init__(self):
        pass

    def fit_transform(self, adj_mats):
        results = []
        x = 0
        last_check = 0
        for adj_mat in adj_mats:
            results.append(get_topology_gudhi(adj_mat))
            x += 1
            if x - last_check> 100:
                print(str(x) + " iterations passed")
                last_check = x

                           
        print(results)

        return results
    
def process_features(in_A_file, in_X_file, out_X_file):
    As = np.load(in_A_file, allow_pickle = True)
    Xs = np.load(in_X_file, allow_pickle = True)

    new_features_list = np.array(TopologyTransformer().fit_transform(As))
    #new_features_list = new_features_list.T

    results = []
    for X, new_features in zip(Xs, new_features_list):
        #print(X, new_features)
        results.append(np.hstack((X, new_features)))

    results = np.array(results)
    np.save(out_X_file, results, allow_pickle = True)



def check_shape(file):
    x = np.load(file)
    print(x.shape)
    print(x[0])



def remake_input(case_number, train_or_test):
    DATA_PATH = '/data/experiment1/case' + case_number + '/graph_structured/'
    DATA_PATH = os.path.dirname(__file__)[:-5] + DATA_PATH

    A_train = DATA_PATH + 'A_' + train_or_test + '.npy'
    X_train = DATA_PATH + 'X_' + train_or_test + '.npy'
    out_file = DATA_PATH + 'X_' + train_or_test + '_new.npy'

    process_features(A_train, X_train, out_file)

    check_shape(DATA_PATH + 'X_' + train_or_test + '_new.npy')



def test_simple():
    row  = np.array([0, 1, 2, 1, 3, 2, 0, 3, 4, 1])
    col  = np.array([1, 0, 1, 2, 2, 3, 3, 0, 1, 4])
    data = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    K4 = coo_matrix((data, (row, col)), shape=(5, 5))

    np.save('testing_transformer_A.npy', [K4, K4, K4])
    np.save('testing_transformer_X.npy', [np.ones((5,2)), np.ones((5,2)), np.ones((5,2))])

    process_features('testing_transformer_A.npy', 'testing_transformer_X.npy', 'testing_transformer_output.npy')
    check_shape('testing_transformer_output.npy')


if __name__ == '__main__':
    for case_number in ['30', '118', '300']:
        for train_or_test in ['test', 'train', 'val']:
            print('updating parameters for case' + case_number + ' and on the ' + train_or_test + ' set')
            remake_input(case_number, train_or_test)

    print("all done!")



