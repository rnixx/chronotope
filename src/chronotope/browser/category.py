from pyramid.view import view_config


@view_config(name='chronotope.category',
             accept='application/json',
             renderer='json')
def json_category(model, request):
    return [
        {'id': 'Category1-uid', 'text': 'Category1'},
        {'id': 'Category2-uid', 'text': 'Category2'},
    ]
