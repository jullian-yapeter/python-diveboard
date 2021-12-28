from diveboard.diveboard import Tester, File, Image


if __name__ == "__main__":
    '''
    initialize demo
    '''
    tester = Tester(level="DEBUG")
    test_file_class = True
    test_image_class = True

    if test_file_class:
        '''
        File Class Demo
        '''
        tester.time_start("File_Runtime")
        # initialize File object using filename
        f = File("demo/temp.txt")
        # create the file
        f.create_file()
        create_exists = f.exists()
        # (over)write to the file
        content_1 = "1st line\n"
        f.write_to_file(content_1)
        # append to the file
        content_2 = "2nd line\n"
        content_2_split = content_2.split(" ")
        f.append_to_file(content_2)
        # read from the file
        f.open_file_reader()
        line_1 = f.read_line()
        line_2_split = f.read_line(" ")
        f.close_reader()
        # delete file
        f.delete_file()
        delete_exists = f.exists()
        tester.time_end("File_Runtime")

        tester.test("File.create_file", create_exists, True)
        tester.test("File.write_to_file", line_1, content_1)
        tester.test("File.append_to_file_1", line_2_split[0], content_2_split[0])
        tester.test("File.append_to_file_2", line_2_split[1], content_2_split[1])
        tester.test("File.delete_file", delete_exists, False)

    if test_image_class:
        '''
        Image Class Demo
        '''
        tester.time_start("Image_Runtime")
        # initialize Image object using filename
        try:
            i = Image("demo/test.jpg", color=1)
            init_test = True
        except Exception:
            init_test = False
        # Show the read-in image
        try:
            i.show_image(milliseconds=10)
            show_test = True
        except Exception:
            show_test = False
        # resize the image
        i_resized = i.resize_image((20, 20))
        tester.time_end("Image_Runtime")

        tester.test("Image.__init__", init_test, True)
        tester.test("Image.show_image", show_test, True)
        tester.test("Image.resize_image", i_resized.image.shape, (20, 20, 3))

    tester.write_tests_report("diveboard_demo_report.txt")
