# Metaclassifier
This repository implements the metaclassification process as described in the Metaclassifier paper

## Install
The code itself requires no installation, you can run the code as-is.

The source code depends on these libraries: 

 * Numpy
 * Pandas
 * Scikit-learn, which you can install from [here][sklearn]
 * UnbalancedDataset which you can find on [GitHub][unbalanced]


## Use
You can find usage samples in the Metaclassifier_Test*.py files. The Metaclassifier_Class has been
implemented to look like a SciKit classifier, therefore any function accepting a scikit classifier
as an argument can accept the metaclassifier as well.

Scikit's pipelines don't support a dataset with changing cardinality, therefore to implement SMOTE
we had to reimplement the cross-validation procedure. This function is defined in GeneralCrossValidation.py


[sklearn]: http://scikit-learn.org/stable/install.html
[unbalanced]: https://github.com/fmfn/UnbalancedDataset
