from plumber import (
    Behavior,
    default,
)
from webob.exc import HTTPFound
from pyramid.static import static_view
from cone.tile import registerTile
from cone.app.browser.utils import make_url
from cone.app.browser.ajax import AjaxAction


static_resources = static_view('static', use_subpath=True)

registerTile('logo', 'templates/logo.pt', permission='login', strict=False)
registerTile('footer', 'templates/footer.pt', permission='login', strict=False)


class AuthoringNext(Behavior):
    """Behavior for add and edit form tiles considering cancel action.
    """
    form_name = default('')

    @default
    @property
    def cancel_action(self):
        return 'action.{0}.cancel'.format(self.form_name)

    @default
    def next(self, request):
        model = self.model
        if self.request.params.get(self.cancel_action):
            model = model.parent
        url = make_url(request.request, node=model)
        if self.ajax_request:
            return [
                AjaxAction(url, 'content', 'inner', '#content'),
            ]
        return HTTPFound(location=url)
