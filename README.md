# pyfast
200 - get - ok
201 - post - created
204 - put - no content (updated in bg)
400 - bad request
401 - unautorised
404 - not found
422 - unprocessable
500 - internal server error

httpexception - raise

starlette => easier to remember status codes 


pydantic 1 to 2
.dict() function is now renamed to .model_dump()

schema_extra function within a Config class is now renamed to json_schema_extra

Optional variables need a =None example: id: Optional[int] = None

