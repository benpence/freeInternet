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
        }
        
        function_input = name.replace('.json', '').split('-')
        
        for function_name in MAP:
            if function_name in name:
                return json.dumps(
                    MAP[function_name](function_input))

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
                'children': [],
            })
            
            for i, instance in enumerate(fi.job.model.Instance.query.filter_by(job_id=job.id).all()):
                # Add child reference in parent
                items[-1 - i]['children'].append(
                    {'_reference': "%d%d" % (job.id, instance.id)}
                )
                
                # Add child
                items.append(
                    {
                        'id': "%d%d" % (job.id, instance.id),
                        'label': '%d: %s' % (instance.id, str(instance.input)),
                        'type': 'instance',
                        'job': job.name,
                        'job_id': str(job.id),
                        'instance_id': str(instance.id),
                    }
                )
            
        # Create context around the tree and return it
        return {
            'identifier': 'id',
            'label': 'label',
            'items': items,
        }
        

    def _assignments(self, input):
        try:
            name, job_id, instance_id = input
        except ValueError, e:
            return {"error": "Invalid JSON request"}
        
        job_id = int(job_id)
        instance_id = int(instance_id)
        
        model = fi.job.model.Assignment
        query = model.query.filter_by(
            job_id=job_id,
            instance_id=instance_id,
        ).all()
    
        data = {}
        
        for ass in query:
            if ass.date_issued and ass.date_returned and ass.output and ass.verified:
                data[ass.id] = {
                    'ip': ass.client.ip,
                    'date_issued': ass.date_issued.strftime("%Y/%m/%d %H:%M EST"),
                    'date_returned': ass.date_returned.strftime("%Y/%m/%d %H:%M EST"),
                    'output': ass.output,
                    'verified': ass.verified
                }
        
        return data