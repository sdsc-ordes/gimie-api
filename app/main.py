from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
import os
from gimie.project import Project
import json
from pprint import pprint

from .orcid import run_analysis_from_github_username
from .semantics import filter_person_with_github

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the Gimie API v0.1.0. Gimie Version 0.7.2"}

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
    

### V2

@app.get("/v2/repository/getgimie/jsonld/{full_path:path}")
async def v2_repository_jsonld(
    full_path: str,
    output_type: str = Query("json", regex="^(string|json)$")
):
    try:
        proj = Project(full_path)

        # To retrieve the rdflib.Graph object
        g = proj.extract()

        # To retrieve the serialized graph
        output = g.serialize(format='json-ld')

        if output_type == "json":
            jsonld = json.loads(output)
            return {"link": full_path, "output": jsonld}
        else:
            return {"link": full_path, "output": output}
    except Exception as e:
        return {"link": full_path, "output": f"Error: {e}"}

@app.get("/v2/repository/getorcids/json/{full_path:path}")
async def v2_repository_jsonld(
    full_path: str
):
    try:
        proj = Project(full_path)

        # To retrieve the rdflib.Graph object
        g = proj.extract()

        # To retrieve the serialized graph
        output = g.serialize(format='json-ld')

        jsonld = json.loads(output)

        github_persons = filter_person_with_github(jsonld)

        orcid_records = []
        for person in github_persons:

            # In some cases the run_analysis_from_github_username is 
            try:
                output = run_analysis_from_github_username(person["http://schema.org/identifier"][0]["@value"])

                if output is not None:
                    orcid_records.append({
                        '@id': person["@id"],
                        'orcid': output
                    })
            except Exception as e:
                print (f"Error: {e}, {person["@id"]}")
                pass

        return {"url": full_path, "output": orcid_records}

    except Exception as e:
        return {"url": full_path, "output": f"Error: {e}"}
    
    
@app.get("/v2/user/getorcid/json/{git_username}")
async def v2_repository_jsonld(
    git_username: str
):
    try:
        output = run_analysis_from_github_username(git_username)
        return {"username": git_username, "output": output}
    
    except Exception as e:
        return {"username": git_username, "output": f"Error: {e}"}


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
