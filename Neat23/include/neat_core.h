

template<class Numeric> class Link;
template<class Numeric> class Node;


enum AgregationType{
	SUM,
	PRODUCT,
	MIN,
	MAX
};

enum ActivationType{
	LINEAR,
	RECTIFIER,
	UNIPOLAR,
	BIPOLAR
};

enum NodeRole{
	INPUT,
	OUTPUT,
	HIDDEN
};

