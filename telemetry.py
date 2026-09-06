import json, logging, time
from uuid import uuid4
log=logging.getLogger('tagi.telemetry')

def event(name, **fields):
    log.info(json.dumps({'event':name,'trace_id':fields.pop('trace_id',str(uuid4())),'ts':time.time(),**fields},default=str))
