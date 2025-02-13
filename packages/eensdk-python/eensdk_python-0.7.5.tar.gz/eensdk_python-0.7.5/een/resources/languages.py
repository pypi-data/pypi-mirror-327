def list_languages(self):
    """Auto-generated method for 'listLanguages'

    This endpoint allows you to retrieve a list of languages supported by the service.  
It is important to note that after using the pageSize parameter, the "totalSize" in  the response represents the total number of available languages, not the number of languages resulting from the query string.


    HTTP Method: GET
    Endpoint: /languages

    Parameters:
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 500: No description provided
    """
    endpoint = "/languages"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
