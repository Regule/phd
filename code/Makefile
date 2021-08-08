
LIB=-L /home/regule/dane/repo_naukowe/phd/code/lib
INC=-I /home/regule/dane/repo_naukowe/phd/code/include

SHARED_LIBS_SRC = src/c_python_test.c src/neuroevo-test.c
TEST_EXECUTABLE_SRC = src/run_tests.c

TEST_EXECUTABLE := run_tests

main: src/c_python_test.c 
	gcc -o lib/c_python_test.so -shared -fPIC -O2 src/c_python_test.c
	gcc -o lib/neuroevo.so $(LIB) $(INC) -shared -fPIC -l meschach  -O2 src/neuroevo-test.c
	gcc -o build/run_tests $(LIB) $(INC) -l meschach -l neuroevo src/run_tests.c
