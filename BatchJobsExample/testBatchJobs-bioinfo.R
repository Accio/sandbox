library(BatchJobs)

## run the script on bioinfo!

##----------------------------------------##
## Map-Reduce using BatchJobs
##----------------------------------------##
f <- function(x) {
  if (x > 4) Sys.sleep(x/10)
  if (x == 7) stop("Invalid 'x': ", x)
  -x
}

source("makeClusterFunctionRemoteTorque.R")

loadConfig(".BatchJobs-bioinfo.R")

## setup a BatchJob registration

library(ribiosUtils)
reg <- makeRegistry(id="HBcalcBioinfo", file.dir=ribiosTempdir())
print(reg)
ids <- batchMap(reg, fun=f, 5:14)
print(ids)

## show status of registry
print(reg)
showStatus(reg)

done <- submitJobs(reg, resources=list(walltime=3600))

print(done)
showStatus(reg)

## load result of job #2
loadResult(reg, 2)

## laod results of all 'done jobs'
loadResults(reg)

## remove the registry
BatchJobs::removeRegistry(reg, ask="no")
