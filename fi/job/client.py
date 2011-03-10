import fi.job
import fi.shell

class JobClient(object):
    @classmethod
    def doJob(cls, job_path):
        """
        job_path:str -> results_path:str
        """
        
        print "Running job"
        
        shell = fi.shell.Shell()
        
        """TODO: Add in command-line checking"""

        # Decompress job and input data
        shell.add(
            'tar xzv -C %s --file=%s' % (
                fi.job.JOBS_DIRECTORY,
                job_path,
            )
        )
        
        # Run job on input data
        shell.add('%s/job' % fi.job.JOBS_DIRECTORY)
        
        # Generate results_path for compressed results
        filename = fi.job.randomHash()
        results_path = "%s/%s" % (fi.job.JOBS_DIRECTORY, filename)
                
        # Compress results
        shell.add(
            'tar zv --file=%s --create -C %s jobOutput' % (
                results_path,
                fi.job.JOBS_DIRECTORY,
            )
        )
                    
        # Remove unnecessary files
        shell.add(
            'rm %s/job %s/jobInput %s/jobOutput' % (
                tuple(3 * [fi.job.JOBS_DIRECTORY])
            )
        )

        return results_path, shell