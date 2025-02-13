def get_resource_grants(self, resourceType, userId__in=None, resourceId__in=None):
    """Auto-generated method for 'getResourceGrants'

    This endpoint allows you to Retrieve a list of resource grants with pagination and filter parameters.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents  the total number of available resource grants, not the number of resource grants resulting from the query string.


    HTTP Method: GET
    Endpoint: /resourceGrants

    Parameters:
        - unknown (None): No description provided
        - resourceType (query): Filter to get the grants with the specified resource type
        - userId__in (query): Filter to get the grants whose userId is on the provided list. The lookup is exact but case insensitive
        - resourceId__in (query): Filter to get the grants whose resourceId is on the provided list. The lookup is exact but case insensitive

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/resourceGrants"
    params = {}
    if resourceType is not None:
        params['resourceType'] = resourceType
    if userId__in is not None:
        if isinstance(userId__in, list):
            params['userId__in'] = ','.join(map(str, userId__in))
        else:
            params['userId__in'] = str(userId__in)
    if resourceId__in is not None:
        if isinstance(resourceId__in, list):
            params['resourceId__in'] = ','.join(map(str, resourceId__in))
        else:
            params['resourceId__in'] = str(resourceId__in)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_resource_grants(self, body=None):
    """Auto-generated method for 'createResourceGrants'

    This endpoint allows you to create multiple resource grants in one request.

    HTTP Method: POST
    Endpoint: /resourceGrants:bulkCreate

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Responses:
        - 200: Operations performed successfully
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/resourceGrants:bulkCreate"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def delete_resource_grants(self, body=None):
    """Auto-generated method for 'deleteResourceGrants'

    This endpoint allows you to delete multiple resource grants in one request.

    HTTP Method: POST
    Endpoint: /resourceGrants:bulkDelete

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - ids (array): No description provided.

    Responses:
        - 200: Operations performed successfully
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/resourceGrants:bulkDelete"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
