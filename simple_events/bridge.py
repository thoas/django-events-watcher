from .settings import BACKEND


def get_backend(backend):
    from .utils import load_class

    klass = load_class(backend)

    return klass()

backend = get_backend(BACKEND)
