An running example of BatchJobs in R
====================================

__BatchJobs__ is a R package that provides map, filter, and reduce functionalities so that the jobs can be parallelised. 

The example file __testBatchJobs.R__ runs on rbalhpc05, the head of clusters where Torque/PBS is installed.

## Template file
zhangj83-rbalhpc05.tmpl, the template file digested by the brew package, is slighly modified from the [template file](https://raw.githubusercontent.com/tudo-r/BatchJobs/master/examples/cfTorque/simple.tmpl).

In the directives, nodes=<%= resources$nodes %>,vmem=<%= resources$memory %>,ppn=<%= resources$cpu %> shoud be used to specify nodes, virtual memory, and cpu used by the job. Correspondingly __nodes__, __memory__, and __cpu__ should be set in the __resources__ parameter of the __submitJobs__ function.
