def list_time_zones(self):
    """Auto-generated method for 'listTimeZones'

    This endpoint allows you to retrieve a list of the supported time zones.  
  
It is important to note that after using the pageSize parameter, the "totalSize"  in the response represents the total number of available time zones, not the number of time zones resulting from the query string.


    HTTP Method: GET
    Endpoint: /timeZones

    Parameters:
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 500: No description provided
    """
    endpoint = "/timeZones"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
