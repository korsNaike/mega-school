from src.dependency_injector import DependencyInjector

if __name__ == '__main__':
    dependency_injector = DependencyInjector()

    # Для инъекции зависимостей с помощью @inject
    dependency_injector.wire(
        packages=["src"],
    )

    server = dependency_injector.uvicorn_server_singleton()
    del dependency_injector
    # Запуск uvicorn
    server.run()
