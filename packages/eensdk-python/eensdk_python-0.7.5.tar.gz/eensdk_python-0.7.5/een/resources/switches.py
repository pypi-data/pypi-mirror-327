def list_switches(self, id__in=None, name__contains=None, id__contains=None, include=None):
    """Auto-generated method for 'listSwitches'

    This endpoint allows users to retrieve a paginated list of switches within a given account.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response  represents the total number of available switches, not the number of switches resulting from the query string.


    HTTP Method: GET
    Endpoint: /switches

    Parameters:
        - id__in (query): List of IDs to filter on that is comma separated.
        - name__contains (query): Filter to get the switches whose the name contains the provided substring. The lookup is exact and case insensitive

        - id__contains (query): Filter to get the switches whose the id contains the provided substring. The lookup is exact and case insensitive

        - include (query): No description provided
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/switches"
    params = {}
    if id__in is not None:
        params['id__in'] = id__in
    if name__contains is not None:
        params['name__contains'] = name__contains
    if id__contains is not None:
        params['id__contains'] = id__contains
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_switch(self, switchId, include=None):
    """Auto-generated method for 'getSwitch'

    This endpoint allows users to retrieve a specific switch based on its id.

    HTTP Method: GET
    Endpoint: /switches/{switchId}

    Parameters:
        - switchId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/switches/{switchId}"
    params = {}
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_switch(self, body, switchId):
    """Auto-generated method for 'updateSwitch'

    This endpoint allows users to update a given switch.

    HTTP Method: PATCH
    Endpoint: /switches/{switchId}

    Parameters:
        - switchId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Switch name

    Responses:
        - 204: Switch Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/switches/{switchId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def update_port(self, body, switchId, portId):
    """Auto-generated method for 'updatePort'

    A specific port can be turned On/Off with this endpoint. A port can also be power cycled.

    HTTP Method: POST
    Endpoint: /switches/{switchId}/ports/{portId}/actions

    Parameters:
        - switchId (path): No description provided
        - portId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - action (string): Possible values:
* `enable` - Turn on the port. * `disable` - Turn off the port. * `reboot` - Power cycle the port.


    Responses:
        - 204: Port Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/switches/{switchId}/ports/{portId}/actions"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
