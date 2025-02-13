from flaskavel.lab.catalyst.exceptions import DumpFlaskavelException
from flaskavel.lab.catalyst.http_status_code import HttpStatusCode
from flask import has_request_context, jsonify, send_file, redirect

def dd(*args, **kwargs):

    from flaskavel.lab.beaker.console.output import Console
    import inspect
    import sys

    # Obtener el lugar donde se llamó a la función dd()
    trace = inspect.stack()[1]

    # Convertir los valores de args a cadenas válidas para jsonify
    sanitized_args = []
    for arg in args:
        if not isinstance(arg, (dict, list, str, int, float, bool)):
            sanitized_args.append(str(arg))
        else:
            sanitized_args.append(arg)

    # Convertir los key-value pairs de kwargs a cadenas válidas para jsonify
    sanitized_kwargs = {}
    for key, value in kwargs.items():
        if not isinstance(value, (dict, list, str, int, float, bool)):
            sanitized_kwargs[str(key)] = str(value)
        else:
            sanitized_kwargs[str(key)] = value

    # Estructurar la respuesta
    response = {
        'filename': trace.filename,
        'function': trace.function,
        'line': trace.lineno,
        'values': sanitized_args,
        'values_key': sanitized_kwargs
    }

    # Mostrar información en la consola
    filename = f"Filename: {trace.filename}"
    Console.newLine()
    Console.line("-" * len(filename))
    Console.textSuccess("Flaskavel Debugger")
    Console.line("-" * len(filename))
    Console.textDanger(filename)
    Console.textDanger(f"Function: {trace.function}")
    Console.textDanger(f"Line: {trace.lineno}")

    if sanitized_args:
        Console.newLine()
        Console.info("VALUES:")
        for value in sanitized_args:
            Console.line(value)

    if sanitized_kwargs:
        Console.newLine()
        Console.info("KEY-VALUE PAIRS:")
        for key, value in sanitized_kwargs.items():
            Console.line(f"{str(key)}: {str(value)}")

    Console.line("-" * len(filename))
    Console.newLine()

    sys.stdout.flush()

    raise DumpFlaskavelException(response)

class Response:
    """
    Provides standardized static methods to generate common JSON responses used in web services.
    Follows a consistent format inspired by Laravel’s response methods.
    """

    @staticmethod
    def json(data:dict=None, errors:dict=None, code:int=200, message:str="Operation successful", status:str="Ok", headers:dict={}):
        """
        General method for sending a standard JSON response.

        Args:
            data (dict): The data to include in the response. Defaults to None.
            code (int): The HTTP status code. Defaults to 200.
            message (str): The message to include in the response. Defaults to "Success".
            status (str): The status text. Defaults to "Ok".
            headers (dict): Optional HTTP headers. Defaults to None.

        Returns:
            tuple: A tuple containing a JSON object, the HTTP status code, and optional headers.
        """

        response = {
            "status": status,
            "message": message,
            "data": data or {},
            "errors": errors or {}
        }

        if has_request_context():
            return jsonify(response), code, headers or {}
        return response

    @staticmethod
    def success(data:dict=None, message:str="Operation successful", headers:dict=None):
        """
        Responds with a 200 OK for successful operations.
        """
        return Response.json(
            data=data,
            code=HttpStatusCode.OK.code,
            message=message,
            status=HttpStatusCode.OK.description,
            headers=headers
        )

    @staticmethod
    def created(data:dict=None, message:str="Resource created successfully", headers:dict=None):
        """
        Responds with a 201 Created when a resource is successfully created.
        """
        return Response.json(
            data=data,
            code=HttpStatusCode.CREATED.code,
            message=message,
            status=HttpStatusCode.CREATED.description,
            headers=headers
        )

    @staticmethod
    def noContent(headers:dict=None):
        """
        Responds with a 204 No Content.
        """
        return Response.json(
            data=None,
            code=HttpStatusCode.NO_CONTENT.code,
            message='',
            status=HttpStatusCode.NO_CONTENT.description,
            headers=headers
        )

    @staticmethod
    def badRequest(errors:dict=None, message:str="Bad request", headers:dict=None):
        """
        Responds with a 400 Bad Request when the request is invalid.
        """
        return Response.json(
            errors=errors,
            code=HttpStatusCode.BAD_REQUEST.code,
            message=message,
            status=HttpStatusCode.BAD_REQUEST.description,
            headers=headers
        )

    @staticmethod
    def unauthorized(message:str="Unauthorized", headers:dict=None):
        """
        Responds with a 401 Unauthorized for authentication failures.
        """
        return Response.json(
            code=HttpStatusCode.UNAUTHORIZED.code,
            message=message,
            status=HttpStatusCode.UNAUTHORIZED.description,
            headers=headers
        )

    @staticmethod
    def forbidden(message:str="Forbidden", headers:dict=None):
        """
        Responds with a 403 Forbidden when the user does not have permission.
        """
        return Response.json(
            code=HttpStatusCode.FORBIDDEN.code,
            message=message,
            status=HttpStatusCode.FORBIDDEN.description,
            headers=headers
        )

    @staticmethod
    def notFound(errors:dict=None, message:str="Resource not found", headers:dict=None):
        """
        Responds with a 404 Not Found when a resource is not found.
        """
        return Response.json(
            errors=errors,
            code=HttpStatusCode.NOT_FOUND.code,
            message=message,
            status=HttpStatusCode.NOT_FOUND.description,
            headers=headers
        )

    @staticmethod
    def unprocessableEntity(errors:dict=None, message:str="Unprocessable Entity", headers:dict=None):
        """
        Responds with a 422 Unprocessable Entity for validation errors.
        """
        return Response.json(
            errors=errors,
            code=HttpStatusCode.UNPROCESSABLE_ENTITY.code,
            message=message,
            status=HttpStatusCode.UNPROCESSABLE_ENTITY.description,
            headers=headers
        )

    @staticmethod
    def serverError(errors:dict=None, message:str="Internal server error", headers=None):
        """
        Responds with a 500 Internal Server Error for unexpected server issues.
        """
        return Response.json(
            errors=errors,
            code=HttpStatusCode.INTERNAL_SERVER_ERROR.code,
            message=message,
            status=HttpStatusCode.INTERNAL_SERVER_ERROR.description,
            headers=headers
        )

    @staticmethod
    def flaskavelError(errors:dict=None, message:str="Flaskavel HTTP Runtime Exception", headers=None):
        """
        Flaskavel HTTP Runtime Exception.
        """
        return Response.json(
            errors=errors,
            code=HttpStatusCode.INTERNAL_SERVER_ERROR.code,
            message=message,
            status=HttpStatusCode.INTERNAL_SERVER_ERROR.description,
            headers=headers
        )

    @staticmethod
    def dd(data:dict=None):
        """
        Flaskavel Dump Exception.
        """
        return Response.json(
            data=data,
            code=HttpStatusCode.INTERNAL_SERVER_ERROR.code,
            message="Flaskavel Dump And Die",
            status=HttpStatusCode.INTERNAL_SERVER_ERROR.description,
            headers=None
        )

    @staticmethod
    def redirect(location):
        """
        Performs a redirect to a different location (similar to Laravel’s `redirect()`).
        """
        if has_request_context():
            return redirect(location)
        raise ValueError("An attempt was made to use the 'redirect' functionality outside the context of an HTTP request.")

    @staticmethod
    def download(file_path, filename=None, mimetype=None):
        """
        Responds by sending a file to the client (similar to Laravel’s `download()`).
        """
        if has_request_context():
            return send_file(file_path, as_attachment=True, download_name=filename, mimetype=mimetype)
        raise ValueError("An attempt was made to use the 'download' functionality outside the context of an HTTP request.")

