#include <stdlib.h>
#include <meschach/matrix.h>

#include "neuroevo_test.h"

void test_meschach(){

	printf("--- STARTING MESCHACH TEST ---\n");

	// Creating pointers to meschach strutures
	MAT   *A; // Matrix
	VEC   *x; // Vector
	PERM  *p; // Permutation

	// Initializing structures
	A = m_get(3,4); // Zero matrix 3x4 
//    x = v_get(10); // Zero vector with 10 elements
//    p = px_get(10); // Identity permutation

	// Freeing memory
	// M_FREE(A);
	// V_FREE(x);
	// PX_FREE(p);

	printf("Size of matrix A is %d x %d.\n", A->m, A->n);
//	printf("Size of vector x is %d.\n", x->dim);
//	printf("Size of permutation p is %d.\n", p->size);
}

