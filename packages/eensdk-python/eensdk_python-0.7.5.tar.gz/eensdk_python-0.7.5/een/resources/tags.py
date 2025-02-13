def get_tags(self, sort=None, name__contains=None):
    """Auto-generated method for 'getTags'

    Retrieves a list of all tags visible to the current user.
You can filter the result by name__contains and sort the result by sort field. Additionally, you can paginate the results by pageToken and pageSize.


    HTTP Method: GET
    Endpoint: /tags

    Parameters:
        - sort (query): List of fields that should be sorted
        - name__contains (query): Filter to get Tags whose the name contains the provided substring. The lookup is exact and case insensitive
        - unknown (None): No description provided

    Responses:
        - 200: Account retrieved
        - 400: No description provided
        - 401: No description provided
        - 500: No description provided
    """
    endpoint = "/tags"
    params = {}
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    if name__contains is not None:
        params['name__contains'] = name__contains
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
