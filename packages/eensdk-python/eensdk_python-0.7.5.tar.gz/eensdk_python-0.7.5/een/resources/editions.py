def get_editions(self, accountId=None):
    """Auto-generated method for 'getEditions'

    This endpoint allows you to retrieve a list of the editions that are available for your account.  
It is important to note that after using the pageSize parameter, the "totalSize" in  the response represents the total number of available editions, not the number of editions resulting from the query string.


    HTTP Method: GET
    Endpoint: /editions

    Parameters:
        - accountId (query): Account ID specified in as an ESN Type.
        - unknown (None): No description provided

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/editions"
    params = {}
    if accountId is not None:
        params['accountId'] = accountId
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_edition(self, id):
    """Auto-generated method for 'getEdition'

    This endpoint allows you to retrieve a specific edition by its ID.

    HTTP Method: GET
    Endpoint: /editions/{id}

    Parameters:
        - id (path): Edition ID

    Responses:
        - 200: Successfully authorized
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/editions/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
