library(checkmate)
ribiosCfBrewTemplate <- function(conf, template, rscript, extension) {
    checkmate::assertEnvironment(conf)
    checkmate::assertString(template)
    checkmate::assertString(rscript)
    checkmate::assertString(extension)
    if (conf$debug) {
        outfile = sub("\\.R$", sprintf(".%s", extension), rscript)
    }
    else {
        outfile = ribiosTempfile("template")
    }
    pf = parent.frame()
    old = getOption("show.error.messages")
    on.exit(options(show.error.messages = old))
    options(show.error.messages = FALSE)
    z = suppressAll(try(brew::brew(text = template, output = outfile, 
        envir = pf), silent = TRUE))
    if (is.error(z)) 
        stopf("Error brewing template: %s", as.character(z))
    BatchJobs:::waitForFiles(outfile, conf$fs.timeout)
    return(outfile)
}

makeClusterFunctionsRemoteTorque <- function (template.file,
                                              list.jobs.cmd = c("qselect-rbalhpc05", "-u $USER", "-s EHQRTW")) 
{
    checkmate::assertCharacter(list.jobs.cmd, min.len = 1L, any.missing = FALSE)
    template = cfReadBrewTemplate(template.file)
    submitJob = function(conf, reg, job.name, rscript, log.file, 
        job.dir, resources, arrayjobs) {
        outfile = ribiosCfBrewTemplate(conf, template, rscript, "pbs")
        res = BatchJobs:::runOSCommandLinux("qsub-rbalhpc05", 
            outfile, stop.on.exit.code = FALSE)
        max.jobs.msg = "Maximum number of jobs already in queue"
        output = collapse(res$output, sep = "\n")
        if (grepl(max.jobs.msg, output, fixed = TRUE)) {
            makeSubmitJobResult(status = 1L, batch.job.id = NA_character_, 
                msg = max.jobs.msg)
        }
        else if (res$exit.code > 0L) {
            cfHandleUnknownSubmitError("qsub-rbalhpc05", res$exit.code, 
                res$output)
        }
        else {
            makeSubmitJobResult(status = 0L, batch.job.id = stringr::str_trim(output))
        }
    }
    killJob = function(conf, reg, batch.job.id) {
        cfKillBatchJob("qdel-rbalhpc05", batch.job.id)
    }
    listJobs = function(conf, reg) {
        batch.ids = BatchJobs:::runOSCommandLinux(list.jobs.cmd[1L], list.jobs.cmd[-1L])$output
        unique(gsub("\\[[[:digit:]]\\]", "[]", batch.ids))
    }
    getArrayEnvirName = function() "PBS_ARRAYID"
    makeClusterFunctions(name = "RemoteTorque", submitJob = submitJob, 
        killJob = killJob, listJobs = listJobs, getArrayEnvirName = getArrayEnvirName)
}
