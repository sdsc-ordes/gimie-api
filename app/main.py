from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from gimie.project import Project


app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the Gimie API v0.1.0. Gimie Version 0.7.2"}

@app.get("/test/{string}")
async def test(string):
    return {"output": string}

@app.get("/gimie/project/{full_path:path}")
async def gimieJSON(full_path:str):
    try:
        proj = Project(full_path)

        return {"link": full_path, "output": proj}
    except Exception as e:
        print("Exception:"+str(e))
        print(os.environ.get('ACCESS_TOKEN'))
        return {"link": full_path, "output": str(e)}
    
@app.get("/gimie/ttl/{full_path:path}")
async def gimieTTL(full_path:str):
    try:
        print(os.environ.get('ACCESS_TOKEN'))
        proj = Project(full_path)

        # To retrieve the rdflib.Graph object
        g = proj.extract()

        # To retrieve the serialized graph
        output = g.serialize(format='ttl')

        return {"link": full_path, "output": output}
    except Exception as e:
        print(e)
        return {"link": full_path, "output": e}

    
@app.get("/gimie/jsonld/{full_path:path}")
async def gimie_jsonld(full_path:str):
    try:
        proj = Project(full_path)

        # To retrieve the rdflib.Graph object
        g = proj.extract()

        # To retrieve the serialized graph
        output = g.serialize(format='json-ld')

        return {"link": full_path, "output": output}
    except Exception as e:
        return {"link": full_path, "output": e}

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
