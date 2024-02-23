# Dos formas de ejecutar fastapi
    1. uvicorn main:app
    2. Agragar las lineas de codigo
        if __name__ == '__main__':
            uvicorn.run("main:app", port=8000)

    y lugo correr python main.py