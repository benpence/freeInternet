import commands

import common

class JobClient(object):
    @classmethod
    def doJob(cls, job_path):
        """
        job_path:str -> results_path:str
        """
        
        """ADD IN CHECKING?"""
        
        # Decompress job and input data
        print commands.getoutput('tar xzv -C %s --file=%s' % (
            common._CLIENT_DIRECTORY,
            job_path,
            ))
        print "1"
        # Run job on input data
        commands.getoutput('%s/job < %s/jobInput > %s/jobOutput' %
            tuple(3 * [common._CLIENT_DIRECTORY]))
        print "2"
        # Generate results_path for compressed results
        filename = common.random_hash()
        results_path = "%s/%s" % (common._CLIENT_DIRECTORY, filename)
        print "3"
        # Compress results
        print commands.getoutput('tar zv --file=%s --create -C %s jobOutput' % (
            results_path,
            common._CLIENT_DIRECTORY,
            ))
        print "4"
        # Remove unnecessary files
        print commands.getoutput('rm %s/job %s/jobInput %s/jobOutput' % (
            tuple(3 * [common._CLIENT_DIRECTORY])))
        print "5"    
        return results_path
        
def test():
    import setup
    
    common._CLIENT_DIRECTORY = common._SERVER_DIRECTORY
    JobClient.doJob("%s/0" % common._SERVER_DIRECTORY)
        
if __name__ == "__main__":
    test()