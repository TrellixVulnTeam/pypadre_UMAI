import unittest

# noinspection PyMethodMayBeStatic
import numpy as np

from pypadre.binding.model.sklearn_binding import SKLearnPipeline
from pypadre.core.model.experiment import Experiment
from pypadre.pod.importing.dataset.dataset_import import SKLearnLoader

test_numpy_array = np.array([[1.0, "A", 2],
                             [2.0, "B", 2],
                             [3.0, "A", 3],
                             [3.0, "C", 4]])


def create_test_pipeline(self):
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC
    estimators = [('SVC', SVC(probability=True))]
    return Pipeline(estimators)


class TestSKLearnPipeline(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSKLearnPipeline, self).__init__(*args, **kwargs)

    def test_default_sklearn_pipeline(self):

        # TODO clean up experiment creator
        pipeline = SKLearnPipeline(pipeline=create_test_pipeline(['SVC']))

        loader = SKLearnLoader()
        iris = loader.load("sklearn", utility="load_iris")
        experiment = Experiment(dataset=iris, pipeline=pipeline)

        experiment.execute()
        # TODO asserts and stuff


if __name__ == '__main__':
    unittest.main()
