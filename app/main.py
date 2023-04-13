from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from starlette.requests import Request
from starlette.responses import Response
from traceback import print_exception

from gimie.project import Project


app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, Welcome to the Gimie API"}

@app.get("/test/{string}")
async def test(string):
    return {"output": string}

@app.get("/gimie/project/{full_path:path}")
async def gimieJSON(full_path:str):
    try:
        proj = Project("https://github.com/SDSC-ORD/gimie")

        return {"link": full_path, "output": proj}
    except Exception as e:
        return {"link": full_path, "output": e}
    
@app.get("/gimie/ttl/{full_path:path}")
async def gimieJSON(full_path:str):
    try:
        proj = Project("https://github.com/SDSC-ORD/gimie")

        # To retrieve the rdflib.Graph object
        g = proj.to_graph()

        # To retrieve the serialized graph
        output = proj.serialize(format='ttl')

        return {"link": full_path, "output": output}
    except Exception as e:
        return {"link": full_path, "output": e}


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )