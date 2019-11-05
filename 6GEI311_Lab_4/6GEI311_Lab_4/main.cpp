#include "main.h"

auto begin = std::chrono::system_clock::now();
std::vector<std::vector<double>> time_results;
std::mutex vectorLock;

void calculate(int id)
{
	auto start = std::chrono::high_resolution_clock::now();
	for (volatile int i = 0; i < 999999; i++) { tanh(i); }
	auto finish = std::chrono::high_resolution_clock::now();
	std::vector<double> delta;
	delta.push_back(start.time_since_epoch().count() / 1000000000.0);
	delta.push_back(finish.time_since_epoch().count() / 1000000000.0);
	vectorLock.lock();
	time_results.push_back(delta);
	vectorLock.unlock();
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


static PyObject* simple_loop(PyObject* self, PyObject* args)
{
	auto start = std::chrono::high_resolution_clock::now();
	for (volatile int i = 0; i < 999999; i++) { tanh(i); }
	auto finish = std::chrono::high_resolution_clock::now();
	auto delta = std::chrono::duration_cast<std::chrono::microseconds>(finish - start).count();

	PyObject *pythonVal = Py_BuildValue("L", delta);
	return pythonVal;
}


static PyObject* thread_exec_time(PyObject* self, PyObject* args)
{
	time_results.clear();
	int workers;
	PyArg_ParseTuple(args, "i", &workers);

	ctpl::thread_pool p(workers);
	for (int i = 0; i < 16; ++i)
	{
		p.push(calculate);
	}

	p.stop(true);
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
	   { "simple_loop", simple_loop, METH_VARARGS, "Simple execution"},
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
