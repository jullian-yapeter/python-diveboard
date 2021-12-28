import os
import time

import numpy as np
import cv2


class Tester():
    def __init__(self, level="INFO"):
        '''
        Tester Class:
        Contains functionality to easily test and profile code

        params:
        level [str] : the level at which to test the code
        "DEBUG": Fine-grain progress reports
        "INFO": Coarse-grain progress reports
        "WARN": Potentially harmful situations
        "ERROR": Harmful situations that are non-fatal
        "FATAL": Sever errors; reason to abort

        attr:
        rank [dict] : the hierarchy of testing levels
        tests [dict] : dictionary to track results of tests
        '''
        self.level = level
        self.rank = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3, "FATAL": 4}
        self.tests = {}

    def test(self, test_label, actual, expected):
        '''
        compares actual and expected outputs. If a test with the same identifies is run multiple times, it
        appends the results of each run to a list

        params:
        test_label [str] : a unique identifier for the test
        actual [obj] : the actual output
        expected [obj] : the expected output
        '''
        if test_label not in self.tests:
            self.tests[test_label] = []
        if actual == expected:
            self.tests[test_label].append("PASS")
            if self.rank[self.level] <= self.rank["DEBUG"]:
                print(f"DEBUG: {test_label}: PASS")
        else:
            self.tests[test_label].append("FAIL")
            if self.rank[self.level] <= self.rank["ERROR"]:
                print(f"ERROR: {test_label}: FAIL\n actual: {actual}\n expected: {expected}")

    def time_start(self, test_label):
        '''
        starts a timer at any given point in the code and keeps track of it in the tests dict

        params:
        test_label [str] : a unique identifier for the test
        '''
        self.tests[test_label] = {}
        self.tests[test_label]["start"] = time.time()

    def time_end(self, test_label):
        '''
        ends a timer at any given point in the code and keeps track of it in the tests dict

        params:
        test_label [str] : a unique identifier for the test, should be same as one used in time_start
        '''
        if test_label not in self.tests or "start" not in self.tests[test_label]:
            raise Exception("TesterLabelNotFound", test_label)
        self.tests[test_label]["end"] = time.time()
        self.tests[test_label]["elap"] = self.tests[test_label]["end"] - self.tests[test_label]["start"]
        if self.rank[self.level] <= self.rank["DEBUG"]:
            print(f"DEBUG: {test_label}: {self.tests[test_label]['elap']}s")

    def write_tests_report(self, filename):
        '''
        write out a file containing the results of all the testing perfromed using this Tester object
        '''
        f = File(filename)
        f.erase_file_content()
        for k, v in self.tests.items():
            f.append_to_file(f"{k}: {v}\n")


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

    def read_line(self, delimiter=None):
        '''
        reads the next line in the file that has been opened

        params:
        delimiter [str] : the delimiter on which to split the read-in line
        '''
        line = self.reader.readline()
        if delimiter is None:
            return line
        return line.split(delimiter)

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

    def erase_file_content(self):
        '''
        overwrites the content of a file with an empty character
        '''
        with open(self.filename, "w") as f:
            f.write("")

    def exists(self):
        return os.path.exists(self.filename)

    def delete_file(self):
        if self.exists():
            os.remove(self.filename)
        else:
            print(f"File.delete_file({self.filename}): The file does not exist")


class Image():
    def __init__(self, template, color=1):
        '''
        Image Class:
        Contains functionality to work with images and perform basic processing

        attr:
        image [numpy.ndarray] : read-in image represented as numpy array

        params:
        filename [str] : the filename of the image file
        color [int] : 1 for 3-channel color images, 0 for 1-channel grayscale images
        '''
        if type(template) == str:
            self.filename = template
            self.image = self._read_image(color)
        elif type(template) == np.ndarray:
            self.image = template
        else:
            raise Exception("ImageInputError",
                            "Input template is of an invalid type: input filename [str] or image [numpy.ndarray]")

    def _read_image(self, color):
        '''
        reads in the image into the attribute
        '''
        try:
            return cv2.imread(self.filename, color)
        except Exception as e:
            print(f"Image._read_image({self.filename}): Unable to read in image, {e}")

    def show_image(self, window_name="image", milliseconds=None):
        '''
        show the read-in image

        params:
        window_name [str] : name of the window in which the image will be displayed
        milliseconds [int] : milliseconds for which to display the image; if None, show until a key is pressed
        '''
        cv2.imshow(window_name, self.image)
        if milliseconds is not None:
            cv2.waitKey(milliseconds)
        else:
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    def resize_image(self, dims):
        '''
        resize the image to the given dimensions

        params:
        dims [(int, int)] : the (height, width) to resize the image to
        '''
        return Image(cv2.resize(self.image, dims))
