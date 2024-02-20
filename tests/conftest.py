import pytest
import os


@pytest.fixture
def read_testdata_file():
    def _read_file(filename):
        # Assume que os arquivos estão na pasta "testdata"
        testdata_dir = os.path.join(os.path.dirname(__file__), "testdata")
        file_path = os.path.join(testdata_dir, filename)

        try:
            with open(file_path, "r") as file:
                content = file.read()
                return content
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo '{filename}' não encontrado em 'testdata'."
            )

    return _read_file
