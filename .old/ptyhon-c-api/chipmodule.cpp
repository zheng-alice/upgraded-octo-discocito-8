// Based on https://docs.python.org/3/extending/extending.html#compilation-and-linkage

#include <Python.h>
#include <dlib/image_transforms.h>

using namespace dlib;

static PyObject * get_chips(PyObject *self, PyObject *args){
	const char *command;
	int sts;

	if(!PyArg_ParseTuple(args, "s", &command))
		return NULL;
	get_face_chip_details(NULL, 150, 0.25);
	sts = system(command);
	return PyLong_FromLong(sts);
}

static PyMethodDef ChipMethods[] = {
	{"get", get_chips, METH_VARARGS, "Finds transformed cropouts of faces in images based on given face landmarks."},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef chipmodule = {
	PyModuleDef_HEAD_INIT,
	"chips",// Module name
	NULL,	// Module documentation
	-1,	// Size of per-interpreter state of the module,
		// or -1 if state is kept in global variables
	ChipMethods
};

PyMODINIT_FUNC
PyInit_chips(void){
	return PyModule_Create(&chipmodule);
}

int main(int argc, char *argv[]){
	wchar_t *program = Py_DecodeLocale(argv[0], NULL);
	if (program == NULL) {
		fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
		exit(1);
	}

	/* Add a built-in module, before Py_Initialize */
	PyImport_AppendInittab("chips", PyInit_chips);

	/* Pass argv[0] to the Python interpreter */
	Py_SetProgramName(program);

	/* Initialize the Python interpreter.  Required. */
	Py_Initialize();

	/* Optionally import the module; alternatively,
	   import can be deferred until the embedded script
	   imports it. */
	PyImport_ImportModule("chips");

	PyMem_RawFree(program);
	return 0;
}
