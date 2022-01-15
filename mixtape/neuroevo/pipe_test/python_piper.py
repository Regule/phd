import sys


def main():
    out_pipe = open("/tmp/python_to_cpp_pipe", "w")
    in_pipe = open('/tmp/cpp_to_python_pipe', 'r')
    out_pipe.write('This is test')
    line = in_pipe.readline()
    out_pipe.close()
    print(line)
    in_pipe.close()


if __name__ == '__main__':
    main()

