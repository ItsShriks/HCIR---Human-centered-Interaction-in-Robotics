//##############################################################################
//
// Class: VarArray
//
//##############################################################################
// #include "global.hpp"
#include "array.h"

//====== Constructor ===========================================================
//
//------------------------------------------------------------------------------

template <class T>
VarArray<T>::VarArray(long startSize, long stepSize):
				nItems(0), nHoles(0), lastItem(0),
				theSize(startSize),theStepSize(stepSize)
{
	init();
}

//====== Destructor ============================================================
//
//------------------------------------------------------------------------------

template <class T> VarArray<T>::~VarArray()
{
	if (item)		delete [] item;
}

//====== init ==================================================================
// initializes array elements and set all pointer to zero
//------------------------------------------------------------------------------

template <class T> void VarArray<T>::init()
{
	item		= new T* [theSize];
	memset(item, 0, theSize * sizeof(T*));
}

//====== grow ==================================================================
// increases array size by stepsize if overflow occurs
//------------------------------------------------------------------------------

template <class T> bool VarArray<T>::grow()
{
	T  **tempitem = new T*	  [theSize + theStepSize];

	if (!tempitem)
	{
		return false;
	}
	memcpy(tempitem, item, theSize*sizeof(T*));
	memset(&tempitem[theSize], 0, theStepSize*sizeof(T*));
	delete [] item;
	item		= tempitem;
	theSize     +=theStepSize;
	return true;
}

//====== shrink ================================================================
// shrinks array size to minimal size
//------------------------------------------------------------------------------

template <class T> void VarArray<T>::shrink()
{
	T **tempitem = new	T *[lastItem+1];
	if (!tempitem) return;
	if (lastItem)
	{
		memcpy(tempitem, item, lastItem*sizeof(T*));
	}
	delete [] item;
	theSize = lastItem+1;
	item	= tempitem;
}

//====== valid =================================================================
// return true, if entry of type T already exists. The implementation of type
// T must provide an appropriate test for equivalence of two variables of type
// T
//------------------------------------------------------------------------------

template <class T> bool VarArray<T>::valid(T const &x)
{
	for (long i=0; i<lastItem; i++) if (valid(i) && x == *((T *) item[i])) return true;
	return false;
}

//====== valid =================================================================
// returns true, if entry <eid> is used
//------------------------------------------------------------------------------

template <class T> bool VarArray<T>::valid(long const eid)
{
	return (bool) ((eid >= 0) && (eid < theSize) && item[eid]);
}

//====== get ===================================================================
// returns pointer to object of type T if entry is used, a zero pointer
// otherwise
//------------------------------------------------------------------------------

template <class T> T const *VarArray<T>::get(long eid)
{
	return item[eid];
}

//====== get ===================================================================
// returns pointer to object of type T if entry is used, a zero pointer
// otherwise
//------------------------------------------------------------------------------

template <class T> T const *VarArray<T>::get(T const &x)
{
long
	pos = getId(x);
	return pos != -1 ? item[pos] : 0;
}


//====== getId =================================================================
// returns eid (i.e. position) of entry T if it exists, otherwise -1. The
// implementation must provide an appropriate test for equivalence of two
// variables of type T.
//------------------------------------------------------------------------------

template <class T> const long VarArray<T>::getId(T const &x)
{
	for (long i=0; i<lastItem; i++) if (valid(i) && x == *((T*) item[i])) return i;
	return -1;
}

//====== set ===================================================================
// enters variable of type T in the array. If empty spaces inside of the
// array exist (due to erased variables) then these are used first. The values
// of an existing variable are replaced by the values of the new one.
//------------------------------------------------------------------------------

template <class T> long VarArray<T>::set(T const &x)
{
long
	pos, i;

	if ((pos = getId(x)) != -1)
	{
		*item[pos] = x;
		return pos;
	}

	if (nHoles > 0)
	{
		nHoles--;
		for (i=0; i<lastItem; i++) if (!item[i]) break;
		pos = i;
	}
	else
	{
		if (lastItem >= theSize) grow();
		pos = lastItem++;
	}
	item[pos]  = new T;
	*item[pos] = x;
	nItems++;
	return pos;
}

template <class T> long VarArray<T>::set(T const &x, long eid)
{
	if (!valid(eid) || x != *item[eid]) return -1;

	*item[eid] = x;
	nItems++;
	return eid;
}

//====== erase =================================================================
// deletes a variable of type T from the array
//------------------------------------------------------------------------------

template <class T> bool VarArray<T>::erase(T const &x)
{
	return erase(getId(x));
}

//====== erase =================================================================
// deletes variable referenced by eid from the array, if this entry is used
//------------------------------------------------------------------------------

template <class T> bool VarArray<T>::erase(long eid)
{
	if (!valid(eid)) return false;
	delete item[eid];
	item[eid] = 0;
	nItems--;

	if (eid == lastItem - 1)
		lastItem--;
	else
		nHoles++;
	return true;
}

//====== size =================================================================
// returns the number of possible entries in the array (without calling grow())
//------------------------------------------------------------------------------
template <class T> long VarArray<T>::size()
{
	return theSize;
}

//====== items =================================================================
// returns the number of used entries in the array
//------------------------------------------------------------------------------

template <class T> long VarArray<T>::items()
{
	return nItems;
}
