/*
The following code inverts the matrix input using LU-decomposition with backsubstitution of unit vectors. Reference: Numerical Recipies in C, 2nd ed., by Press, Teukolsky, Vetterling & Flannery.

you can solve Ax=b using three lines of ublas code:

permutation_matrix<> piv;
lu_factorize(A, piv);
lu_substitute(A, piv, x); 

*/
 #ifndef INVERT_MATRIX_HPP
 #define INVERT_MATRIX_HPP

 // REMEMBER to update "lu.hpp" header includes from boost-CVS
 #include <boost/numeric/ublas/vector.hpp>
 #include <boost/numeric/ublas/vector_proxy.hpp>
 #include <boost/numeric/ublas/matrix.hpp>
 #include <boost/numeric/ublas/triangular.hpp>
 #include <boost/numeric/ublas/lu.hpp>
 #include <boost/numeric/ublas/io.hpp>

 namespace ublas = boost::numeric::ublas;

 namespace Minisat { namespace Util {
 /* Matrix inversion routine.
    Uses lu_factorize and lu_substitute in uBLAS to invert a matrix */

#ifdef GENERIC
 template<class M, class IM>
 bool InvertMatrix (M &input, IM &inverse) {
#else
 template<class T>
 bool InvertMatrix (const ublas::matrix<T>& input, ublas::matrix<T>& inverse) {
#endif
 	using namespace boost::numeric::ublas;
 	typedef permutation_matrix<std::size_t> pmatrix;
 	// create a working copy of the input
 	matrix<T> A(input);
 	// create a permutation matrix for the LU-factorization
 	pmatrix pm(A.size1());

 	// perform LU-factorization
 	int res = lu_factorize(A,pm);
        if( res != 0 ) return false;

 	// create identity matrix of "inverse"
 	inverse.assign(ublas::identity_matrix<T>(A.size1()));

 	// backsubstitute to get the inverse
 	lu_substitute(A, pm, inverse);

 	return true;
 }

 template<class T>
 bool solve (const ublas::matrix<T>& input, ublas::vector<T>& b) {
 	using namespace boost::numeric::ublas;
 	typedef permutation_matrix<std::size_t> pmatrix;
 	// create a working copy of the input
 	matrix<T> A(input);
 	// create a permutation matrix for the LU-factorization
 	pmatrix pm(A.size1());

 	// perform LU-factorization
 	int res = lu_factorize(A,pm);
        if( res != 0 ) return false;

 	// backsubstitute to get the inverse
 	lu_substitute(A, pm, b);

 	return true;

 }
template <typename T>
T determinant(const ublas::matrix<T>& m)
{
 	using namespace boost::numeric::ublas;
 	typedef permutation_matrix<std::size_t> pmatrix;
 	// create a working copy of the input
 	matrix<T> A(m);
 	// create a permutation matrix for the LU-factorization
 	pmatrix pm(A.size1());

 	// perform LU-factorization
 	int res = lu_factorize(A,pm);
    T determinant = 1;

     for(int i = 0; i < A.size1(); i++)
     {
      determinant *= A(i,i);
     }
    int pm_sign=1;
    typedef pmatrix::size_type size_type;
    size_type size=pm.size();
    for (size_type i = 0; i < size; ++i)
        if (i != pm(i))
            pm_sign*= -1; // swap_rows would swap a pair of rows here, so we change sign
    return pm_sign * determinant;
}

} }
 #endif //INVERT_MATRIX_HPP
