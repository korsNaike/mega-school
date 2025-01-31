
import sys

from src.dependency_injector import DependencyInjector


def suppress_all_exceptions(exc_type, exc_value, traceback):
    pass  # Do nothing, suppressing all exceptions

sys.excepthook = suppress_all_exceptions


dependency_injector = DependencyInjector()

# Для инъекции зависимостей с помощью @inject
dependency_injector.wire(
    packages=["src"],
)

app = dependency_injector.fastapi_app_singleton().get_instance()
