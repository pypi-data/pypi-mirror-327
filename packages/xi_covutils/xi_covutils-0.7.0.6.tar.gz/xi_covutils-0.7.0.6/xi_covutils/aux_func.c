#include <Python.h>
#include <stdio.h>
#include <string.h>

// My functions
static PyObject* identity_fraction(PyObject* self, PyObject *args) {
  char *s1;
  char *s2;
  if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
    Py_RETURN_NONE;
  }
  int l1 = strlen(s1);
  int l2 = strlen(s2);
  if (l1 != l2) {
    Py_RETURN_NONE;
  }
  int identical = 0;
  int total = 0;
  for (int c = 0; c < l1; c++) {
    char c1 = s1[c];
    char c2 = s2[c];
    if (!((c1 == '-' || c1 == '.') && (c2 == '-' || c2 == '.'))) {
        total++;
        if (s1[c] == s2[c]) {
          identical++;
        }
    }
  }
  double f = ((double)identical)/total;
  return Py_BuildValue("d", f);
}

// Documentation of identity_fraction
static char identity_fraction_docs[] = (
  "identity_fraction(seq1, seq2): -> float\n"
  "Computes identity fraction between two sequences\n"
);

// Mapping table
static PyMethodDef auxl_funcs[] = {
  {"identity_fraction", (PyCFunction) identity_fraction,
      METH_VARARGS, identity_fraction_docs},
  {NULL}
};

static struct PyModuleDef auxl =
{
  PyModuleDef_HEAD_INIT,
  "auxl", /* name of module */
  "Auxiliary function", /* module documentation, may be NULL */
  -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
  auxl_funcs
};

PyMODINIT_FUNC PyInit_auxl(void)
{
  return PyModule_Create(&auxl);
}
