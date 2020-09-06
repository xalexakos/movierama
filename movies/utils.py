def get_response_query_params(request):
    """ Formats any query params received on request as url search params. """
    q_params = []
    ordering = request.GET.get('ordering')
    if ordering:
        q_params.append('ordering=' + ordering)

    user_filter = request.GET.get('user')
    if user_filter:
        q_params.append('user=' + user_filter)

    page_no = request.GET.get('page')
    if page_no:
        q_params.append('page=' + page_no)

    url_params = ''
    for i, p in enumerate(q_params):
        url_params += '?' if i == 0 else '&'
        url_params += p

    return url_params
