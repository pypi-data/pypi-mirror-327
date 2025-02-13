def create_token(self, body):
    """Auto-generated method for 'createToken'

    Resellers can retrieve access tokens for a given end-user account, assuming that the end-user account falls under the reseller's account.


    HTTP Method: POST
    Endpoint: /authorizationTokens

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Responses:
        - 201: Token created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/authorizationTokens"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
