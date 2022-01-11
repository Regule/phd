import sys


def main():
    out_pipe = open("/tmp/python_to_cpp_pipe", "w")
    out_pipe.write('This is test')
    out_pipe.close()

if __name__ == '__main__':
    main()

