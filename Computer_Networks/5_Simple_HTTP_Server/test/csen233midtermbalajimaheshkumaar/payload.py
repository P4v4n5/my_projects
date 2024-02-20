class HttpRequest:
    def __init__(self):
        self.RequestMethod = str()
        self.RequestPath = str()
        self.Version = str()
        self.Headers = dict()

    def parse(self, request_string: str):
        request_string = request_string.strip().strip("\r\n")
        request_string_lines = request_string.split("\r\n")
        request_line = request_string_lines[0]
        request_line_parts = request_line.split(" ")
        self.RequestMethod = request_line_parts[0]
        self.RequestPath = request_line_parts[1]
        self.Version = request_line_parts[2]
        for index in range(1, len(request_string_lines) - 1):
            CurrentHeader = request_string_lines[index]
            self.Headers.update({CurrentHeader.split(":")[0].strip(): CurrentHeader.split(":")[1].strip()})


class HttpResponse:
    def __init__(self):
        self.ResponseMethod = "HTTP/1.1"
        self.StatusCode = str()
        self.StatusMessage = str()
        self.Headers = dict()
        self.Body = str()

    def __str__(self) -> str:
        response_string = f"{self.ResponseMethod} {self.StatusCode} {self.StatusMessage}\r\n"
        for header in self.Headers:
            response_string += f"{header}:{self.Headers[header]}\r\n"
        response_string += "\r\n"
        response_string += self.Body
        response_string += "\r\n"

        return response_string
