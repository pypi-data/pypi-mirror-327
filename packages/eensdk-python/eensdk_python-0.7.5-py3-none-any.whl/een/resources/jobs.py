def list_jobs(self):
    """Auto-generated method for 'listJobs'

    List Jobs.  Filtering by userId, type, state namespace, createTimestamp, updateTimestamp, expireTimestamp.


    HTTP Method: GET
    Endpoint: /jobs

    Parameters:
        - unknown (None): No description provided

    Responses:
        - 200: List Jobs
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/jobs"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_job(self, jobId):
    """Auto-generated method for 'getJob'

    Get a single Job

    HTTP Method: GET
    Endpoint: /jobs/{jobId}

    Parameters:
        - jobId (path): No description provided

    Responses:
        - 200: Get a single Job
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/jobs/{jobId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def delete_job(self, jobId):
    """Auto-generated method for 'deleteJob'

    Deletes a Job regardless of state.


    HTTP Method: DELETE
    Endpoint: /jobs/{jobId}

    Parameters:
        - jobId (path): No description provided

    Responses:
        - 204: Job deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/jobs/{jobId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
