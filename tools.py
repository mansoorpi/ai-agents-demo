"""Safe, explicit tool registry used by the agent runtime."""
from datetime import datetime, timezone
import ast, operator, urllib.parse, urllib.request, re
from html import unescape
from typing import Any, Dict

def get_current_time() -> Dict[str, Any]: return {"utc":datetime.now(timezone.utc).isoformat(),"timezone":"UTC"}
_BIN={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}; _UN={ast.UAdd:operator.pos,ast.USub:operator.neg}
def _calc(n):
    if isinstance(n,ast.Expression): return _calc(n.body)
    if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
    if isinstance(n,ast.BinOp) and type(n.op) in _BIN: return _BIN[type(n.op)](_calc(n.left),_calc(n.right))
    if isinstance(n,ast.UnaryOp) and type(n.op) in _UN: return _UN[type(n.op)](_calc(n.operand))
    raise ValueError('Only numeric arithmetic is supported')
def calculator(expression:str)->Dict[str,Any]:
    if len(expression)>200:return {'error':'Expression too long'}
    try:return {'expression':expression,'result':_calc(ast.parse(expression,mode='eval'))}
    except Exception as exc:return {'error':str(exc)}
def web_search(query:str,max_results:int=5)->Dict[str,Any]:
    """Search the public web via DuckDuckGo HTML; returns titles, URLs and snippets."""
    max_results=max(1,min(max_results,5)); url='https://html.duckduckgo.com/html/?'+urllib.parse.urlencode({'q':query})
    req=urllib.request.Request(url,headers={'User-Agent':'TAGI-Agent/1.0'})
    html=urllib.request.urlopen(req,timeout=10).read().decode('utf-8','ignore')
    blocks=re.findall(r'<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',html,re.S)
    out=[]
    for href,title in blocks[:max_results]: out.append({'title':re.sub('<.*?>','',unescape(title)).strip(),'url':unescape(href)})
    return {'query':query,'results':out}
TOOLS={
'get_current_time':{'description':'Get the current UTC date and time.','parameters':{'type':'object','properties':{},'required':[]},'handler':get_current_time},
'calculator':{'description':'Evaluate simple numeric arithmetic.','parameters':{'type':'object','properties':{'expression':{'type':'string'}},'required':['expression']},'handler':calculator},
'web_search':{'description':'Search the public web for current information.','parameters':{'type':'object','properties':{'query':{'type':'string'},'max_results':{'type':'integer','minimum':1,'maximum':5}},'required':['query']},'handler':web_search}}
def tool_definitions(): return [{'type':'function','function':{'name':n,'description':s['description'],'parameters':s['parameters']}} for n,s in TOOLS.items()]
def execute_tool(name:str,arguments:Dict[str,Any]):
    spec=TOOLS.get(name)
    if not spec:return {'error':f'Unknown tool: {name}'}
    try:return spec['handler'](**arguments)
    except Exception as exc:return {'error':f'Tool execution failed: {exc}'}
