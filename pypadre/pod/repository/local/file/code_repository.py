import errno
import glob
import os
import re
import shutil

from pypadre.core.model.code.code_file import CodeFile
from pypadre.core.model.code.function import Function
from pypadre.core.model.code.icode import ICode
from pypadre.pod.backend.i_padre_backend import IPadreBackend
from pypadre.pod.repository.i_repository import ICodeRepository
from pypadre.pod.repository.local.file.generic.i_file_repository import File
from pypadre.pod.repository.local.file.generic.i_git_repository import IGitRepository
from pypadre.pod.repository.serializer.serialiser import JSonSerializer, DillSerializer


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


NAME = "code"

META_FILE = File("metadata.json", JSonSerializer)
CODE_FILE = File("code.bin", DillSerializer)


class CodeFileRepository(IGitRepository, ICodeRepository):

    @staticmethod
    def placeholder():
        return '{CODE_ID}'

    def __init__(self, backend: IPadreBackend):
        super().__init__(root_dir=os.path.join(backend.root_dir, NAME), backend=backend)

    def get_by_dir(self, directory):
        path = glob.glob(os.path.join(self._replace_placeholders_with_wildcard(self.root_dir), directory))[0]

        metadata = self.get_file(path, META_FILE)

        # TODO what about inherited classes
        if metadata.get(ICode.CODE_CLASS) == str(Function):
            fn = self.get_file(path, CODE_FILE)
            code = Function(fn=fn, metadata=metadata)

        elif metadata.get(ICode.CODE_CLASS) == str(CodeFile):
            code = CodeFile(path=metadata.path, cmd=metadata.cmd, file=metadata.get("file", None))

        else:
            raise NotImplementedError()

        return code

    def to_folder_name(self, code):
        # TODO only name for folder okay? (maybe a uuid, a digest of a config or similar?)
        return code.name

    def get_by_name(self, name):
        """
        Shortcut because we know name is the folder name. We don't have to search in metadata.json
        :param name: Name of the dataset
        :return:
        """
        return self.list({'folder': re.escape(name)})

    def _put(self, obj, *args, directory: str, store_code=False, **kwargs):
        code = obj
        self.write_file(directory, META_FILE, code.metadata)

        if store_code:
            if isinstance(code, Function):
                self.write_file(directory, CODE_FILE, code.fn, mode="wb")

            if isinstance(code, CodeFile):
                code_dir = os.path.join(directory, "code")
                if code.file is not None:
                    if not os.path.exists(code_dir):
                        os.mkdir(code_dir)
                    copy(os.path.join(code.path, code.file), os.path.join(directory, "code", code.file))
                else:
                    copy(code.path, code_dir)
