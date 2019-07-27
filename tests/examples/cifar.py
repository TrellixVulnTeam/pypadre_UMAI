from pypadre.ds_import import load_numpy_array_multidimensional
import numpy as np
from sklearn.pipeline import Pipeline
from pypa_pytorch import Wrapper
from pypadre.core.experiment import Experiment
from pypadre.app import p_app

def custom_split(idx):
    np.random.seed(0)
    idx = np.random.permutation(idx)
    return idx[:55000], idx[55000:], None


def main():

    features = np.load('../../features.npy')
    labels = np.load('../../labels.npy')
    #mean_img = np.load('../../mean_file.npy')
    #x = np.ones(shape=(1, 1, 32, 32))
    #mean = np.concatenate((x*0.4914, x*0.4822, x*.4465), axis=1)
    #std = np.concatenate((x*0.2023, x*0.1994, x*.2010), axis=1)
    #features = (features/255 - mean)/std
    ds = load_numpy_array_multidimensional(features=features, targets=labels, columns=['images', 'labels'],
                                           target_features=['labels'])

    print(ds)

    import json
    with open('vgg16.json') as json_data:
        params = json.load(json_data)



        # params['steps'] = 100000

        #params['epochs'] = 10
        """
        grid_params = dict()
        seed = list(range(0,100))
        p = {'seed': seed}
        grid_params['pytorch'] = p
        """
        for i in range(0, 100):
            obj = Wrapper(params=params)
            estimators = [('pytorch', obj)]
            workflow = Pipeline(estimators)
            # workflow.fit(np.asarray(x), np.reshape(y, newshape=(150,1)))
            ex = Experiment(name="Cifar-VGG16",
                            description="Testing Torch via SKLearn Pipeline",
                            dataset=ds,
                            workflow=workflow, keep_splits=True, strategy='function', function=custom_split
                            )
            #ex.execute(parameters=grid_params)
            ex.execute()
            print(ex.metrics)


def main1():
    print('Executing main1')
    features = np.load('../../features.npy')
    labels = np.load('../../labels.npy')
    ds = load_numpy_array_multidimensional(features=features, targets=labels, columns=['images', 'labels'],
                                           target_features=['labels'])
    import json
    with open('vgg16.json') as json_data:
        params = json.load(json_data)
    obj = Wrapper(params=params)
    estimators = [('pytorch', obj)]
    workflow = Pipeline(estimators)
    ex = Experiment(name="Cifar-VGG16",
                    description="Testing Torch via SKLearn Pipeline",
                    dataset=ds,
                    workflow=workflow, keep_splits=True, strategy='function', function=custom_split
                    )
    ex.execute()

if __name__ == '__main__':
    main()
