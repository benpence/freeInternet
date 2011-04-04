import json

from twisted.web.server import Site

import fi
import fi.web.protocol
import fi.throttle.model
import fi.job.model

class WebController(Site):
    noisy = False
    
    def __init__(self):
        Site.__init__(self, fi.web.protocol.WebProtocol(self))
    
    def json(self, request, name):
        MAP = {
            'creditbandwidth': self._creditBandwidth,
            'jobs': self._jobs,
            'assignments': self._assignments,
            'output': self._output,
        }
        
        function_input = name[:-5].split('-')
        
        for function_name in MAP:
            if function_name in name:
                return json.dumps(
                    MAP[function_name](function_input)
                )

        # Catch all
        return json.dumps(_creditBandwidth(function_input))
    
    def _creditBandwidth(self, *args):
        clients = fi.throttle.model.Client.query.all()

        credit = {}
        bandwidth = {}
        for client in clients:
            credit[client.vpn_ip] = client.credit
            bandwidth[client.vpn_ip] = client.bandwidth
    
        return {"credit": credit, "bandwidth": bandwidth}
    
    def _jobs(self, *args):
        """
        This data must conform to dojo's expected json input for a dojo.data.ItemFileReadStore'
        
        """
        items = []

        for job in fi.job.model.Job.query.all():
            # Add parent
            items.append({
                'id': str(job.id),
                'label': '%d: %s' % (job.id, job.name),
                'type': 'job',
                'description': job.description,
                'input': job.input_desc,
                'output': job.output_desc,
                'children': [],
                'name': job.name,
            })
            
            for i, instance in enumerate(fi.job.model.Instance.query.filter_by(job_id=job.id).all()):
                # Add child reference in parent
                items[-1 - i]['children'].append(
                    {'_reference': "%d%d" % (job.id, instance.id)}
                )
                
                # Add child
                items.append({
                    'id': "%d%d" % (job.id, instance.id),
                    'label': '%d: %s' % (instance.id, str(instance.input)),
                    'type': 'instance',
                    'job': job.name,
                    'job_id': str(job.id),
                    'instance_id': str(instance.id),
                })
            
        # Create context around the tree and return it
        return {
            'identifier': 'id',
            'label': 'label',
            'items': items,
        }
        

    def _assignments(self, string):
        try:
            name, job_id, instance_id = string
        except ValueError, e:
            return {"error": "Invalid JSON request"}
        
        job_id = int(job_id)
        instance_id = int(instance_id)
        
        model = fi.job.model.Assignment
        query = model.query.filter_by(
            job_id=job_id,
            instance_id=instance_id,
        ).all()
    
        data = []
        
        for ass in query:
            if ass.time_issued and ass.time_returned and ass.output and ass.verified:
                data.append({
                    'id': ass.id,
                    'ip': ass.client.ip,
                    'time_issued': ass.time_issued.strftime("%Y/%m/%d %H:%M:%S EST"),
                    'time_returned': ass.time_returned.strftime("%Y/%m/%d %H:%M:%S EST"),
                    'verified': ass.verified,
                })
        
        # Make compatible with dojo expected format
        return {
            "identifier": 'id',
            "items": data
        }
        
    def _output(self, string):
        try:
            name, job_id, instance_id, assignment_id = string
        except ValueError, e:
            return {"error": "Invalid JSON request"}

        ass = fi.job.model.Assignment.get_by(
            job_id=int(job_id),
            instance_id=int(instance_id),
            id=int(assignment_id)
        )    

        return {'output': ass.output}