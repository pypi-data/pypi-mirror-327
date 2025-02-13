def list_auditlogs(self, timestamp__gte, timestamp__lte, include=None, userId=None, targetId=None, targetType=None, locationId=None, auditType=None):
    """Auto-generated method for 'listAuditlogs'

    This endpoint filters audit events by userId, targetId, targetType, auditType


    HTTP Method: GET
    Endpoint: /auditLogs

    Parameters:
        - include (query): No description provided
        - userId (query): Filter by userId
        - targetId (query): Filter by targetId
        - targetType (query): Filter by targetType
        - locationId (query): Filter by locationId
        - auditType (query): Filter by auditType
        - timestamp__gte (query): Minimum timestamp to list auditlogs.
        - timestamp__lte (query): Maximum timestamp to list auditlogs.
        - unknown (None): No description provided

    Responses:
        - 200: List of audit events
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/auditLogs"
    params = {}
    if include is not None:
        params['include'] = include
    if userId is not None:
        params['userId'] = userId
    if targetId is not None:
        params['targetId'] = targetId
    if targetType is not None:
        params['targetType'] = targetType
    if locationId is not None:
        params['locationId'] = locationId
    if auditType is not None:
        params['auditType'] = auditType
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
