import requests
import json
from .errors import *


class Client():
    """"Class client. Can be declared using client = dscbio.Client()"""
    def __init__(self, base_url:str):
        self.base_url = base_url
    
    def get(self, id: int = None, query: str = None, save: bool = None):
        if id is None:
            # ID is required
            raise MissingArgument("User-ID should be provided")
        try:
            res = requests.get(f'{self.base_url}/{id}')
            res_json = res.json()
            # response to json
            if res_json == {"message": "Bad request."}:
                # bot user ID/ ID does not exist
                raise BadArgument("The user-ID does not exists/belongs to a bot  user.")

            if res_json == {"message": "No profile found."}:
                # no profile found
                raise NotFound(f"No profile for user with ID {id} was found.")

        except requests.exceptions.ConnectionError:

            raise HttpExcpetion("An error with the API occurred.\n"
                                "Please contant an website administator.")

        if query is None:
            response = res_json
            # no query provided - whole response
        else:
            try:
                response = res_json[query]
                # get value of query
            except KeyError:
                # no values at "index" of query
                raise BadArgument(f"Query `{query}` was not found.")

        if save is not None and save == True:
            filename = f"{res_json['_id']}.json"  # creating filename "ID".json
            try:
                with open(filename, "w") as f:
                    # open json file , "w"= write "mode"
                    if query is None:
                        conf = response
                    else:
                        conf = {
                            f"{query}": response
                        }
                    json.dump(conf, f, indent=4)
                    # dump values into file with indent 4
            except Exception as e:
                raise Exception(f"An error occurred by saving into `{filename}.\n"
                                f"{e}")
        return response
