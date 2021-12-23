from diveboard.diveboard import File, Tester


if __name__ == "__main__":
    '''
    initialize demo
    '''
    tester = Tester()
    test_file_class = True

    if test_file_class:
        '''
        File Class Demo
        '''
        tester.time_start("File_Time")
        # initialize File object using filename
        f = File("Demo/temp.txt")
        # create the file
        f.create_file()
        create_exists = f.exists()
        # (over)write to the file
        content_1 = "1st line\n"
        f.write_to_file(content_1)
        # append to the file
        content_2 = "2nd line\n"
        f.append_to_file(content_2)
        # read from the file
        f.open_file_reader()
        line_1 = f.read_line()
        line_2 = f.read_line()
        f.close_reader()
        # delete file
        f.delete_file()
        delete_exists = f.exists()

        tester.test("File.create_file", create_exists, True)
        tester.test("File.write_to_file", line_1, content_1)
        tester.test("File.append_to_file", line_2, content_2)
        tester.test("File.delete_file", delete_exists, False)
        tester.time_end("File_Time")

    print(tester.tests)
