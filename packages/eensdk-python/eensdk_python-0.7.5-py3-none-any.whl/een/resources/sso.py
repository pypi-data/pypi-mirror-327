def get_auth_settings(self, include=None):
    """Auto-generated method for 'getAuthSettings'

    Returns Single Sign On Authentication Settings for the given account.


    HTTP Method: GET
    Endpoint: /accounts/self/ssoAuthSettings

    Parameters:
        - include (query): Allows clients to request optional information such us URLs necessary to configure third party IDPs.

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/accounts/self/ssoAuthSettings"
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


def update_auth_settings(self, body):
    """Auto-generated method for 'updateAuthSettings'

    Updates Single Sign On Authentication Settings with the given values.


    HTTP Method: PATCH
    Endpoint: /accounts/self/ssoAuthSettings

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Responses:
        - 204: IDP Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/accounts/self/ssoAuthSettings"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
