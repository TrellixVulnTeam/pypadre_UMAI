# import os
#
# from pypadre.pod.backend.local.file.project.experiment.execution.run.split.split_file_backend import \
#     SplitFileRepository
#
#
# class PadreSplitHttpRepository(SplitFileRepository):
#
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.root_dir = os.path.join(self._parent.root_dir, "splits")
#
#     @property
#     def result(self):
#         return self._result
#
#     @property
#     def metric(self):
#         return self._metric
#
#     def put_progress(self, obj):pass
#
#     def list(self, search, offset=0, size=100):
#         pass
#
#     def get(self, uid):
#         pass
#
#     def put(self, obj, *args, merge=False, **kwargs):
#         pass
#
#     def delete(self, uid):
#         pass