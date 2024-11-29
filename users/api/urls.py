from ninja import NinjaAPI

app = NinjaAPI()

@app.post("login")
def login(
    request, 
    uname: str, 
    passwd: str
    ) -> str:

    "API login througn username and password"

    '''
    TODO
    '''

@app.post("register")
def register(
    request
    ) -> bool:

    "API registet througn token"

    '''
    TODO
    '''

@app.get("getAssignments")
def getAssignments(
    request,
    id: str
    ):

    '''
    TODO
    '''
