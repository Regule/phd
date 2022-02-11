import sys


def main():
    out_pipe = open("/tmp/python_to_cpp_pipe", "w")
    out_pipe.write('This is test')
    out_pipe.close()
    in_pipe = open('/tmp/cpp_to_python_pipe', 'r')
    line = in_pipe.readline()
    in_pipe.close()
    print(line)


if __name__ == '__main__':
    main()

