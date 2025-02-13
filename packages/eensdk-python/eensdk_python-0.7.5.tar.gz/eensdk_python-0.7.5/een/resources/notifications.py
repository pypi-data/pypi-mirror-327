def list_notifications(self, language=None, timestamp__lte=None, timestamp__gte=None, alertId=None, alertType=None, actorId=None, actorType=None, actorAccountId=None, category=None, userId=None, read=None, status=None, sort=None):
    """Auto-generated method for 'listNotifications'

    Search and sort notifications by alertId, alertType, actorId, actorType, actorAccountId, category, and read


    HTTP Method: GET
    Endpoint: /notifications

    Parameters:
        - Accept-Language (header): No description provided
        - language (query): Language query overrides Accept-Language header
        - timestamp__lte (query): Filter by timestamp__lte
        - timestamp__gte (query): Filter by timestamp__gte
        - alertId (query): Filter by alertId
        - alertType (query): Filter by alertType
        - actorId (query): Filter by actorId
        - actorType (query): Filter by actorType
        - actorAccountId (query): Filter by actorAccountId
        - category (query): Filter by category
        - userId (query): Filter by userId
        - read (query): Filter by read
        - status (query): Filter by status
        - sort (query): Sort by timestamp
        - unknown (None): No description provided

    Responses:
        - 200: Notification results
        - 400: No description provided
        - 401: No description provided
        - 500: No description provided
    """
    endpoint = "/notifications"
    params = {}
    if language is not None:
        params['language'] = language
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if alertId is not None:
        params['alertId'] = alertId
    if alertType is not None:
        params['alertType'] = alertType
    if actorId is not None:
        params['actorId'] = actorId
    if actorType is not None:
        params['actorType'] = actorType
    if actorAccountId is not None:
        params['actorAccountId'] = actorAccountId
    if category is not None:
        params['category'] = category
    if userId is not None:
        params['userId'] = userId
    if read is not None:
        params['read'] = read
    if status is not None:
        params['status'] = status
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_notification(self, id):
    """Auto-generated method for 'getNotification'

    Get a notification


    HTTP Method: GET
    Endpoint: /notifications/{id}

    Parameters:
        - id (path): Notification id

    Responses:
        - 200: Notification result
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/notifications/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_notification(self, id, body=None):
    """Auto-generated method for 'updateNotification'

    Update if a notification is read


    HTTP Method: PATCH
    Endpoint: /notifications/{id}

    Parameters:
        - id (path): Notification id

    Request Body:
        - body (application/json):
            Description: Update if a notification is read
            Required: False

    Top-level Request Body Properties:
        - read (boolean): No description provided.

    Responses:
        - 204: The notification has been successfully updated.
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/notifications/{id}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
