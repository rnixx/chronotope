from plumber import (
    Behavior,
    plumb,
)
from yafowil.base import factory
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


class UXMixin(object):

    @property
    def is_frontent(self):
        return self.request.params.get(UX_IDENT) == UX_FRONTEND

    @property
    def is_backend(self):
        return self.request.params.get(UX_IDENT) != UX_FRONTEND


class UXMixinProxy(Behavior):

    @plumb
    def prepare(_next, self):
        _next(self)
        self.form[UX_IDENT] = factory(
            'proxy',
            value=self.request.params.get(UX_IDENT),
        )
