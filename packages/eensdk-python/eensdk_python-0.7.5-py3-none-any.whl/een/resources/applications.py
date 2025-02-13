def list_applications(self):
    """Auto-generated method for 'listApplications'

    This endpoint allows retrieval of all applications accessible by the requesting user.  
It is important to note that after using the pageSize parameter, the "totalSize" in the  response represents the total number of available applications, not the number of applications resulting from the query string.


    HTTP Method: GET
    Endpoint: /applications

    Parameters:
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/applications"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_application(self, body):
    """Auto-generated method for 'createApplication'

    This endpoint allows you to create a new application under the requesting user's account. A maximum of 100 applications can be created under the account.


    HTTP Method: POST
    Endpoint: /applications

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the application.
        - displayName (string): Display name of the application.
        - website (string): URL to the website of this application.
        - developer (string): Name of the developer/company which developed this application.
        - privacyPolicy (string): URL to the privacy policy of this application.
        - termsOfService (string): URL to the terms of service of this application.
        - description (string): The description of the application.
        - isPublic (boolean): Whether this application is intended to be public (available for other parties through an application store).
        - logo (string): URL to the logo of the application.
        - technicalContact (object): Request body for application update.

    Responses:
        - 201: Application Created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/applications"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_application(self, applicationId):
    """Auto-generated method for 'getApplication'

    This endpoint allows you to retrieve a single application.

    HTTP Method: GET
    Endpoint: /applications/{applicationId}

    Parameters:
        - applicationId (path): Identifier of an application

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_application(self, body, applicationId):
    """Auto-generated method for 'updateApplication'

    This endpoint allows you to update a single application.

    HTTP Method: PATCH
    Endpoint: /applications/{applicationId}

    Parameters:
        - applicationId (path): Identifier of an application

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the application.
        - displayName (string): Display name of the application.
        - website (string): URL to the website of this application.
        - developer (string): Name of the developer/company which developed this application.
        - privacyPolicy (string): URL to the privacy policy of this application.
        - termsOfService (string): URL to the terms of service of this application.
        - description (string): The description of the application.
        - isPublic (boolean): Whether this application is intended to be public (available for other parties through an application store).
        - logo (string): URL to the logo of the application.
        - technicalContact (object): Request body for application update.

    Responses:
        - 204: Application Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_application(self, applicationId):
    """Auto-generated method for 'deleteApplication'

    This endpoint allows you to delete a single application.

    HTTP Method: DELETE
    Endpoint: /applications/{applicationId}

    Parameters:
        - applicationId (path): Identifier of an application

    Responses:
        - 204: Application deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_oauth_clients(self, applicationId):
    """Auto-generated method for 'getOauthClients'

    This endpoint allows retrieval of all OAuth credentials for the given application.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available OAuth credentials, not the number of OAuth credentials resulting from the query string.


    HTTP Method: GET
    Endpoint: /applications/{applicationId}/oauthClients

    Parameters:
        - applicationId (path): Identifier of an application
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def add_oauth_client(self, body, applicationId):
    """Auto-generated method for 'addOauthClient'

    This endpoint allows you to create a new OAuth client for the given application. A maximum of 250 oauth client credentials can be created under the application.


    HTTP Method: POST
    Endpoint: /applications/{applicationId}/oauthClients

    Parameters:
        - applicationId (path): Identifier of an application

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the oauth client.
        - redirectUris (array): No description provided.
        - loginUris (array): No description provided.
        - type (string): This defines the type of this client . Clients are CONFIDENTIAL by default.

    Responses:
        - 201: Created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: No description provided
        - 409: No description provided
        - 415: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_oauth_client(self, applicationId, clientId):
    """Auto-generated method for 'getOauthClient'

    This endpoint allows you to retrieve a specific OAuth client.

    HTTP Method: GET
    Endpoint: /applications/{applicationId}/oauthClients/{clientId}

    Parameters:
        - applicationId (path): Identifier of an application
        - clientId (path): Identifier of a OAuth client

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients/{clientId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_client(self, body, applicationId, clientId):
    """Auto-generated method for 'updateClient'

    This endpoint allows you to update a specific Oauth client.

    HTTP Method: PATCH
    Endpoint: /applications/{applicationId}/oauthClients/{clientId}

    Parameters:
        - applicationId (path): Identifier of an application
        - clientId (path): Identifier of a OAuth client

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the oauth client.
        - redirectUris (array): No description provided.
        - loginUris (array): No description provided.

    Responses:
        - 204: Client Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients/{clientId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_oauth_client(self, applicationId, clientId):
    """Auto-generated method for 'deleteOauthClient'

    This endpoint allows you to delete a specific OAuth client of a given application.

    HTTP Method: DELETE
    Endpoint: /applications/{applicationId}/oauthClients/{clientId}

    Parameters:
        - applicationId (path): Identifier of an application
        - clientId (path): Identifier of a OAuth client

    Responses:
        - 204: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients/{clientId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
