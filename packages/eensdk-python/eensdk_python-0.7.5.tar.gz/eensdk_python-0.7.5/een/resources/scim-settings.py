def get_scim_settings(self):
    """Auto-generated method for 'getScimSettings'

    Returns SCIM Settings of the account.


    HTTP Method: GET
    Endpoint: /accounts/self/scimSettings

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/accounts/self/scimSettings"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_scim_settings(self, body):
    """Auto-generated method for 'updateScimSettings'

    Updates SCIM setting of the account.


    HTTP Method: PATCH
    Endpoint: /accounts/self/scimSettings

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - enabled (boolean): True if user management via SCIM is enabled for the account.
        - apiKey (string): Optionally, you can reset the API key by setting its value to null.  Once the API key is reset, the previous key will be immediately invalidated with no grace period.


    Responses:
        - 200: SCIM settings updated.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/accounts/self/scimSettings"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
