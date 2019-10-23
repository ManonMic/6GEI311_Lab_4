#include "Header.h"

static PyObject* boucle(PyObject* self, PyObject* args)
{
	std::cout << "C++ loop running" << std::endl;
	for (int i = 0; i < 999999; i++) {
		tanh(i);
	}

	PyObject *pythonVal = Py_BuildValue("");
	return pythonVal;
}

static PyMethodDef methods[] = {
	   { "boucle", boucle, METH_VARARGS, "Fonction simple" },
	   { NULL, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"time_tanh",
	"NULL",
	-1,
	methods
};

PyMODINIT_FUNC PyInit_time_tanh(void)
{
	return PyModule_Create(&cModPyDem);
}
