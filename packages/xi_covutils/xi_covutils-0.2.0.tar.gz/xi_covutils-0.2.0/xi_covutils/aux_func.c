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
static char identity_fraction_docs[] =
   "identity_fraction(seq1, seq2): Computes sequence identity fraction for two strings.\n";

// Mapping table 
static PyMethodDef aux_funcs[] = {
   {"identity_fraction", (PyCFunction)identity_fraction, 
      METH_VARARGS, identity_fraction_docs},
   {NULL}
};

static struct PyModuleDef aux =
{
    PyModuleDef_HEAD_INIT,
    "aux", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    aux_funcs
};


// Initialization of the module
// void initaux(void) {
//    Py_InitModule3(
//       "aux",
//       aux_funcs,
//       "Auxiliary Functions");
// }


PyMODINIT_FUNC PyInit_aux(void)
{
    return PyModule_Create(&aux);
}

// View this code to fix
// #include <Python.h>

// static PyObject* uniqueCombinations(PyObject* self)
// {
//     return Py_BuildValue("s", "uniqueCombinations() return value (is of type 'string')");
// }

// static char uniqueCombinations_docs[] =
//     "usage: uniqueCombinations(lstSortableItems, comboSize)\n";

// /* deprecated: 
// static PyMethodDef uniqueCombinations_funcs[] = {
//     {"uniqueCombinations", (PyCFunction)uniqueCombinations, 
//      METH_NOARGS, uniqueCombinations_docs},
//     {NULL}
// };
// use instead of the above: */

// static PyMethodDef module_methods[] = {
//     {"uniqueCombinations", (PyCFunction) uniqueCombinations, 
//      METH_NOARGS, uniqueCombinations_docs},
//     {NULL}
// };


// /* deprecated : 
// PyMODINIT_FUNC init_uniqueCombinations(void)
// {
//     Py_InitModule3("uniqueCombinations", uniqueCombinations_funcs,
//                    "Extension module uniqueCombinations v. 0.01");
// }
// */

// static struct PyModuleDef Combinations =
// {
//     PyModuleDef_HEAD_INIT,
//     "Combinations", /* name of module */
//     "usage: Combinations.uniqueCombinations(lstSortableItems, comboSize)\n", /* module documentation, may be NULL */
//     -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
//     module_methods
// };

// PyMODINIT_FUNC PyInit_Combinations(void)
// {
//     return PyModule_Create(&Combinations);
// }