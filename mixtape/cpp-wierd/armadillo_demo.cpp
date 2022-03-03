/*
 * sudo apt install cmake libopenblas-dev liblapack-dev
 * g++ armadillo_demo.cpp -DARMA_DONT_USE_WRAPPER -lopenblas -llapack
 */



#include <iostream>
#include <armadillo>

using std::cout;
using std::endl;
using arma::Mat;


int main(){
	arma::arma_rng::set_seed_random();
	Mat<double> matrix = arma::randu(4,4);
	cout << matrix << endl;
	matrix.save("mat.out", arma::raw_ascii);
}
