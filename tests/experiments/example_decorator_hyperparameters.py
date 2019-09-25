"""
This file shows an example on how to use PyPaDRE via decorators defining a single experiments.

Note: it is a proof of concept now rather than a test.
"""
import pprint

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

# Note that we want to include all decorator at once using package import
from pypadre import *
from pypadre.app import p_app
from pypadre.pod.importing.dataset.ds_import import load_sklearn_toys


@Workflow(exp_name="example hyperparameter eval with decorators",
          description="Test experiment with decorators",
          hyperparameters={
              "C": [0.1, 0.2],
              "kernel": ["rbf", "linear"]
          })
def create_test_pipeline(**hp):
    estimators = [('clf', SVC(probability=True, **hp))]
    return Pipeline(estimators)


@Dataset(exp_name="example hyperparameter eval with decorators")
def get_dataset():
    ds = [i for i in load_sklearn_toys()][2]
    return ds


if __name__ == '__main__':
    # call run without pypadre app backend
    from pypadre.pod.decorators import _experiments
    pprint.pprint(_experiments)
    ex = run("example hyperparameter eval with decorators")
    print("Runs retained in memory ")
    for e in ex:
        print(e.name)
        for r in e.runs:
            print("\t" + str(r))
    # call via pipadre backend
    ex = p_app.experiments.run(decorated=True)
    print("Runs stored on disk via padre app")
    for e in ex:
      for idx2, r in enumerate(p_app.experiments.list_runs(e.name)):
        print("\tRun: %s" % str(r))
