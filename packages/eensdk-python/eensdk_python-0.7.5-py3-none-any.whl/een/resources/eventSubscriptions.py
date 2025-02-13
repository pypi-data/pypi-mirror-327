def list_event_subscriptions(self):
    """Auto-generated method for 'listEventSubscriptions'

    Gets all visible event subscriptions defined for the current account.

    HTTP Method: GET
    Endpoint: /eventSubscriptions

    Parameters:
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 500: No description provided
    """
    endpoint = "/eventSubscriptions"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_event_subscription(self, body=None):
    """Auto-generated method for 'createEventSubscription'

    Creates a new event subscription.

    HTTP Method: POST
    Endpoint: /eventSubscriptions

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - deliveryConfig (object): Describes how the event subscription should deliver events to the client.
        - filters (array): Optional list of filters that should be added to the event subscription from the moment of creation.


    Responses:
        - 201: EventSubscription created
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/eventSubscriptions"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_event_subscription(self, eventSubscriptionId):
    """Auto-generated method for 'getEventSubscription'

    This endpoint allows you to retrieve a specific event subscription.

    HTTP Method: GET
    Endpoint: /eventSubscriptions/{eventSubscriptionId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def delete_event_subscription(self, eventSubscriptionId):
    """Auto-generated method for 'deleteEventSubscription'

    Deletes a specific event subscription.

    HTTP Method: DELETE
    Endpoint: /eventSubscriptions/{eventSubscriptionId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID

    Responses:
        - 204: EventSubscription deleted
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def list_event_subscription_filters(self, eventSubscriptionId):
    """Auto-generated method for 'listEventSubscriptionFilters'

    Gets all event subscription filters defined for the given event subscription.

    HTTP Method: GET
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_event_subscription_filter(self, eventSubscriptionId, body=None):
    """Auto-generated method for 'createEventSubscriptionFilter'

    Creates an event subscription filter for a given event subscription.

    HTTP Method: POST
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - actors (array): List of actors for which events should be delivered to this event subscription.
        - types (array): List of event types of which events should be delivered to this event subscription.

    Responses:
        - 201: Filter created
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_event_subscription_filter(self, eventSubscriptionId, filterId):
    """Auto-generated method for 'getEventSubscriptionFilter'

    Gets info about a specific filter of a given event subscription ID.

    HTTP Method: GET
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters/{filterId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID
        - filterId (path): Event Subscription Filter ID

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters/{filterId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def delete_event_subscription_filter(self, eventSubscriptionId, filterId):
    """Auto-generated method for 'deleteEventSubscriptionFilter'

    Deletes a filter based on the given ID.

    HTTP Method: DELETE
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters/{filterId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID
        - filterId (path): Event Subscription Filter ID

    Responses:
        - 204: Filter deleted
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters/{filterId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
