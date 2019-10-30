#include "Header.h"

auto begin = std::chrono::system_clock::now();
std::vector<std::vector<double>> time_results;

void boucle()
{
	auto start = std::chrono::high_resolution_clock::now();
	for (volatile int i = 0; i < 999999; i++) { tanh(i); }
	auto finish = std::chrono::high_resolution_clock::now();
	time_results.push_back(std::vector<double>());
	int last_index = time_results.size() - 1;
	time_results[last_index].push_back(start.time_since_epoch().count() / 1000000000.0);
	time_results[last_index].push_back(finish.time_since_epoch().count() / 1000000000.0);
}

static PyObject* GetList(std::vector < std::vector<double>> list)
{
	int const N = list.size();
	PyObject* python_val = PyList_New(N);
	for (int i = 0; i < N; i++)
	{
		PyObject* python_double = Py_BuildValue("dd", list[i][0], list[i][1]);
		PyList_SetItem(python_val, i, python_double);
	}
	return python_val;
}

static PyObject* thread_exec_time(PyObject* self, PyObject* args)
{
	time_results.clear();
	int workers;
	PyArg_ParseTuple(args, "i", &workers);

	std::cout << " workers: " << workers << std::endl;

	std::vector<std::thread> threads;
	for (int i = 0; i < workers; i++) { threads.push_back(std::thread(boucle)); }
	for (int i = 0; i < workers; i++) { threads[i].join(); }

	return GetList(time_results);
}

static PyObject* process_exec_time(PyObject* self, PyObject* args)
{
	time_results.clear();
	int iterations;
	PyArg_ParseTuple(args, "i", &iterations);

	PyObject *pythonVal = Py_BuildValue("");
	return pythonVal;
}

static PyMethodDef methods[] = {
	   { "thread_exec_time", thread_exec_time, METH_VARARGS, "Thread execution" },
	   { "process_exec_time", process_exec_time, METH_VARARGS, "Process execution" },
	   { NULL, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"exec_time",
	"NULL",
	-1,
	methods
};

PyMODINIT_FUNC PyInit_exec_time(void)
{
	return PyModule_Create(&cModPyDem);
}
