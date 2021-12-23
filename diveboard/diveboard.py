import os
import time


class Tester():
    def __init__(self, level="INFO"):
        self.level = level
        self.tests = {}

    def test(self, test_label, actual, expected):
        if test_label not in self.tests:
            self.tests[test_label] = []
        if actual == expected:
            self.tests[test_label].append("PASS")
            if self.level == "DEBUG":
                print(f"{test_label}: PASS")
        else:
            self.tests[test_label].append("FAIL")
            if self.level == "DEBUG":
                print(f"{test_label}: FAIL {actual} != {expected}")

    def time_start(self, test_label):
        self.tests[test_label] = {}
        self.tests[test_label]["start"] = time.time()

    def time_end(self, test_label):
        if test_label not in self.tests or "start" not in self.tests[test_label]:
            raise Exception("TesterLabelNotFound", test_label)
        self.tests[test_label]["end"] = time.time()
        self.tests[test_label]["elap"] = self.tests[test_label]["end"] - self.tests[test_label]["start"]
        if self.level == "DEBUG":
            print(f"{test_label}: {self.tests[test_label]['elap']}s")


class File():
    def __init__(self, filename):
        '''
        File Class:
        Contains functionality to easily work with files; read and write

        params:
        filename [str] : the name of the file to be worked with

        attr:
        reader [_io.TextIOWrapper] : file reader
        '''
        self.filename = filename
        self.reader = None

    def create_file(self):
        '''
        creates a file using the given filename that does not yet exist
        '''
        f = open(self.filename, "x")
        f.close()

    def open_file_reader(self):
        '''
        opens a file with the given filename for reading
        '''
        self.reader = open(self.filename, "r")

    def read_line(self):
        '''
        reads the next line in the file that has been opened
        '''
        return self.reader.readline()

    def close_reader(self):
        '''
        closes the file reader
        '''
        self.reader.close()

    def write_to_file(self, content):
        '''
        overwrites the content of a file using the given new content

        params:
        content [str] : new content to be written to file
        '''
        with open(self.filename, "w") as f:
            f.write(content)

    def append_to_file(self, content):
        '''
        appends new content to file

        params:
        content [str] : new content to be appended to file
        '''
        with open(self.filename, "a") as f:
            f.write(content)

    def exists(self):
        return os.path.exists(self.filename)

    def delete_file(self):
        if self.exists():
            os.remove(self.filename)
        else:
            print(f"File.delete_file({self.filename}): The file does not exist")
