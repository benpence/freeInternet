import common

class JobClient(object):
    
    @classmethod
    def doJob(cls, job_path):
        """
        job_path:str -> results_path:str
        """
        
        shell = common.Shell()
        
        """ADD IN CHECKING?"""
        
        callStack = defer.succeed("None")
        
        
        
        # Decompress job and input data
        shell.execute('tar xzv -C %s --file=%s' % (
            common._CLIENT_DIRECTORY,
            job_path,
            )
        
        # Run job on input data
        shell.execute('%s/job' % common._CLIENT_DIRECTORY)
        
        # Generate results_path for compressed results
        filename = common.random_hash()
        results_path = "%s/%s" % (common._CLIENT_DIRECTORY, filename)
                
        # Compress results
        shell.execute('tar zv --file=%s --create -C %s jobOutput' % (
            results_path,
            common._CLIENT_DIRECTORY,
            ))
                    
        # Remove unnecessary files
        shell.execute('rm %s/job %s/jobInput %s/jobOutput' % (
            tuple(3 * [common._CLIENT_DIRECTORY])))

        return results_path, shell
        
def test():
    import setup
    
    common._CLIENT_DIRECTORY = common._SERVER_DIRECTORY
    JobClient.doJob("%s/0" % common._SERVER_DIRECTORY)
        
if __name__ == "__main__":
    test()