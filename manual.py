
manual_pages = [
    # Page 1 - Introduction
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 1: Introduction\033[0m
================================================================================

UniLang Script (ULS) is a beginner-friendly, interpreted language inspired by Python and JavaScript.
It focuses on simplicity, ease of learning, and a small but useful set of built-in features.

\033[1mKey Concepts:\033[0m
- \033[1mStraightforward Syntax:\033[0m Uses `{}` for code blocks, similar to C-style languages.
- \033[1mBasic Data Types:\033[0m Supports `int`, `float`, `string`, `boolean`, and `list`.
- \033[1mControl Structures:\033[0m Includes `if`, `for`, `while`, and more.
- \033[1mBuilt-in Functions:\033[0m Provides I/O, math, string, list, file, and network functions.
- \033[1mAdvanced Features:\033[0m Supports `eval` and `python_eval` for dynamic code execution (use with caution).
- \033[1mAsynchronous Operations:\033[0m Implements `async` and `await` for concurrent programming.

Use `--man <page>` to navigate this manual.
""",

    # Page 2 - Getting Started
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 2: Getting Started\033[0m
================================================================================

\033[1mSaving Scripts:\033[0m
- Save your scripts with the `.uls` extension, e.g., `script.uls`.

\033[1mRunning Scripts:\033[0m
- Execute scripts using the following command:
  ```
  pypy interpreter.py script.uls
  ```

\033[1mInitialization:\033[0m
- The interpreter may require initialization to install necessary packages. Run:
  ```
  pypy interpreter.py --init
  ```

\033[1mAccessing the Manual:\033[0m
- View specific manual pages with:
  ```
  pypy interpreter.py --man <page>
  ```

\033[1mExample:\033[0m
```
pypy interpreter.py --man 3
```
""",

    # Page 3 - Basic Syntax
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 3: Basic Syntax\033[0m
================================================================================

\033[1mStatements:\033[0m
- End with a newline or block termination.
- Use `{` and `}` to define code blocks.

\033[1mComments:\033[0m
- Start with `#` and continue to the end of the line.

\033[1mExample:\033[0m
\033[36m\033[1m```uls\033[0m
# This is a comment
if (x > 10) {
    print("x is large")
} else {
    print("x is small")
}
\033[36m\033[1m```\033[0m

\033[1mExpressions:\033[0m
- Group using parentheses `()`.
- No semicolons required; line breaks or block ends terminate statements.

Use `--man 4` to learn about Variables and Data Types.
""",

    # Page 4 - Variables & Data Types
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 4: Variables & Data Types\033[0m
================================================================================

\033[1mVariable Assignment:\033[0m
- Use the `=` operator to assign values.
\033[36m\033[1m```uls\033[0m
x = 10
name = "Alice"
is_active = true
nums = [1, 2, 3]
\033[36m\033[1m```\033[0m

\033[1mData Types:\033[0m
- \033[1mIntegers (`int`):\033[0m Whole numbers, e.g., `10`, `-5`.
- \033[1mFloats (`float`):\033[0m Decimal numbers, e.g., `3.14`.
- \033[1mStrings (`string`):\033[0m Text enclosed in double quotes, e.g., `"Hello"`.
- \033[1mBooleans (`boolean`):\033[0m `true` or `false`.
- \033[1mLists (`list`):\033[0m Ordered collections, e.g., `[1, 2, 3]`, `["a", "b", "c"]`. Lists can be nested.

Use `--man 5` to learn about Operators.
""",

    # Page 5 - Operators
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 5: Operators\033[0m
================================================================================

\033[1mArithmetic Operators:\033[0m
- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)
- `%` (modulo)

\033[1mComparison Operators:\033[0m
- `==` (equal to)
- `!=` (not equal to)
- `>` (greater than)
- `<` (less than)
- `>=` (greater than or equal to)
- `<=` (less than or equal to)

\033[1mLogical Operators:\033[0m
- `and`
- `or`
- `not`

\033[1mExample:\033[0m
\033[36m\033[1m```uls\033[0m
if (x > 0 and x < 10) {
    print("x is between 1 and 9")
}
\033[36m\033[1m```\033[0m

Use `--man 6` to explore Built-in Functions.
""",

    # Page 6 - Built-in Functions
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 6: Built-in Functions\033[0m
================================================================================

\033[1mI/O & Conversion:\033[0m
- \033[1mprint(value)\033[0m: Display output.
- \033[1minput(prompt)\033[0m: Receive user input.
- \033[1mstr(value)\033[0m: Convert to string.
- \033[1mint(value)\033[0m: Convert to integer.
- \033[1mfloat(value)\033[0m: Convert to float.
- \033[1mlength(value)\033[0m: Get length of strings or lists.
- \033[1mrandomint(min, max)\033[0m: Generate a random integer between `min` and `max`.

\033[1mString Functions:\033[0m
- \033[1mreplace(s, old, new)\033[0m: Replace occurrences of `old` with `new` in string `s`.
- \033[1mupper(s)\033[0m, \033[1mlower(s)\033[0m, \033[1mcapitalize(s)\033[0m: Modify string cases.
- \033[1mfind(s, sub)\033[0m: Find substring `sub` in `s`.
- \033[1msubstring(s, start, end)\033[0m: Extract substring from `start` to `end`.
- \033[1msplit(s, delim)\033[0m, \033[1mjoin(delim, list)\033[0m: Split and join strings.

\033[1mList Functions:\033[0m
- \033[1mappend(lst, item)\033[0m, \033[1mremove(lst, item)\033[0m: Modify lists.
- \033[1msum(lst)\033[0m: Sum elements.
- \033[1many(lst)\033[0m, \033[1mall(lst)\033[0m: Logical checks.
- \033[1msorted(lst)\033[0m, \033[1mreverse(lst)\033[0m: Sort and reverse lists.
- \033[1mrandom_choice(lst)\033[0m, \033[1mrandom_shuffle(lst)\033[0m: Random operations on lists.

\033[1mMath & Utilities:\033[0m
- \033[1mabs(x)\033[0m, \033[1mround(x, ndigits=0)\033[0m: Basic math operations.
- \033[1mmin(...)\033[0m, \033[1mmax(...)\033[0m: Find minimum or maximum.
- \033[1mpow(x, y)\033[0m, \033[1msin(x)\033[0m, \033[1mcos(x)\033[0m, \033[1mtan(x)\033[0m, \033[1mlog(x, base)\033[0m: Advanced math functions.
- \033[1msqrt(x)\033[0m, \033[1mcurrent_time()\033[0m, \033[1mcurrent_date()\033[0m: Utilities for math and datetime.

Use `--man 7` to learn about Control Structures.
""",

    # Page 7 - Control Structures
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 7: Control Structures\033[0m
================================================================================

\033[1mIf/Else:\033[0m
\033[36m\033[1m```uls\033[0m
if (condition) {
    # Code if condition is true
} else {
    # Code if condition is false
}
\033[36m\033[1m```\033[0m

\033[1mExample:\033[0m
\033[36m\033[1m```uls\033[0m
if (x > 10) {
    print("x is large")
} else {
    print("x is small")
}
\033[36m\033[1m```\033[0m

\033[1mWhile Loops:\033[0m
\033[36m\033[1m```uls\033[0m
while (condition) {
    # Code to execute while condition is true
}
\033[36m\033[1m```\033[0m

\033[1mFor Loops:\033[0m
\033[36m\033[1m```uls\033[0m
for i in range(start, end) {
    print(i)
}
\033[36m\033[1m```\033[0m

\033[1mBreak Statement:\033[0m
- Use `break` to exit loops prematurely.

\033[1mExample:\033[0m
\033[36m\033[1m```uls\033[0m
for i in range(1, 5) {
    print(i)
    if (i == 3) {
        break
    }
}
\033[36m\033[1m```\033[0m

Use `--man 8` to understand Functions.
""",

    # Page 8 - Functions
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 8: Functions\033[0m
================================================================================

\033[1mDefining Functions:\033[0m
\033[36m\033[1m```uls\033[0m
define function_name(params) {
    # Code block
    result value
}
\033[36m\033[1m```\033[0m

\033[1mExample:\033[0m
\033[36m\033[1m```uls\033[0m
define greet(name) {
    result "Hello, " + name + "!"
}

message = greet("Alice")
print(message)
\033[36m\033[1m```\033[0m

\033[1mFunction Behavior:\033[0m
- Functions can accept parameters and return values.
- If no `result` statement is provided, the function results `None` by default.

\033[1mExample Without result:\033[0m
\033[36m\033[1m```uls\033[0m
define say_hello() {
    print("Hello!")
}

result = say_hello()
print(result)  # Outputs: None
\033[36m\033[1m```\033[0m

Use `--man 9` to explore File I/O.
""",

    # Page 9 - File I/O
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 9: File I/O\033[0m
================================================================================

\033[1mFile Operations:\033[0m
- \033[1mread_file(filename)\033[0m: Reads the entire file content as a string.
- \033[1mwrite_file(filename, content)\033[0m: Overwrites the file with `content`.
- \033[1mappend_file(filename, content)\033[0m: Appends `content` to the file.

\033[1mExamples:\033[0m

\033[1m1. Reading a File\033[0m
\033[36m\033[1m```uls\033[0m
content = read_file("example.txt")
print(content)
\033[36m\033[1m```\033[0m

\033[1m2. Writing to a File\033[0m
\033[36m\033[1m```uls\033[0m
write_file("output.txt", "Hello, World!")
\033[36m\033[1m```\033[0m

\033[1m3. Appending to a File\033[0m
\033[36m\033[1m```uls\033[0m
append_file("output.txt", "\\nMore text")
\033[36m\033[1m```\033[0m

\033[1m[!] Caution:\033[0m
- \033[1mData Loss:\033[0m Overwriting files can lead to data loss. Always ensure you're writing to the correct file.
- \033[1mPermissions:\033[0m Ensure you have the necessary permissions to read from or write to files.
- \033[1mSecurity:\033[0m Avoid reading from or writing to files with untrusted input to prevent security vulnerabilities.
""",

    # Page 10 - Advanced Features
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 10: Advanced Features\033[0m
================================================================================

\033[1mDynamic Code Execution:\033[0m
- \033[1meval(code)\033[0m: Executes ULS code provided as a string.
- \033[1mpython_eval(expr)\033[0m: Executes Python expressions within ULS.

\033[1mExamples:\033[0m

\033[1m1. Using `eval`\033[0m
\033[36m\033[1m```uls\033[0m
uls_code = "​"​"
define add(a, b) {
    result a + b
}
result = add(5, 7)
"​"​"
eval(uls_code)
print(result)  # Outputs: 12
\033[36m\033[1m```\033[0m

\033[1m2. Using `python_eval`\033[0m
\033[36m\033[1m```uls\033[0m
expression = "3 * 4 + 5"
result = python_eval(expression)
print(result)  # Outputs: 17
\033[36m\033[1m```\033[0m

\033[1m[!] Warning:\033[0m
- \033[1mSecurity Risks:\033[0m Both `eval` and `python_eval` can execute arbitrary code. **Never** use them with untrusted input as it can lead to code injection attacks.
- \033[1mError Handling:\033[0m Ensure proper error handling when using these functions to manage unexpected issues gracefully.
""",

    # Page 11 - Networking Features
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 11: Networking Features\033[0m
================================================================================

UniLang Script provides built-in functions to perform HTTP operations and handle JSON data, enabling your scripts to interact with web services and APIs seamlessly.

\033[1mHTTP Operations\033[0m
- \033[1mhttp_get(url, headers=None)\033[0m: Sends a GET request to the specified URL.
- \033[1mhttp_post(url, data=None, headers=None)\033[0m: Sends a POST request with an optional data payload.
- \033[1mhttp_put(url, data=None, headers=None)\033[0m: Sends a PUT request to update resources.
- \033[1mhttp_delete(url, headers=None)\033[0m: Sends a DELETE request to remove resources.

\033[1mJSON Handling\033[0m
- \033[1mparse_json(text)\033[0m: Parses a JSON-formatted string into a UniLang data structure (e.g., dictionaries, lists).
- \033[1mto_json(obj)\033[0m: Converts a UniLang data structure into a JSON-formatted string.

\033[1mExamples\033[0m

\033[1m1. Performing a GET Request\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Fetching data from a public API

response = http_get("https://api.agify.io?name=michael")
data = parse_json(response)

print("Name:", data["name"])
print("Predicted Age:", data["age"])
print("Count:", data["count"])
\033[36m\033[1m```\033[0m

\033[1mOutput:\033[0m
```
Name: michael
Predicted Age: 69
Count: 137828
```

\033[1m2. Sending a POST Request\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Submitting data to a mock API

payload = {
    "title": "Foo",
    "body": "Bar",
    "userId": 1
}

response = http_post("https://jsonplaceholder.typicode.com/posts", data=payload)
data = parse_json(response)

print("Created Post ID:", data["id"])
\033[36m\033[1m```\033[0m

\033[1mOutput:\033[0m
```
Created Post ID: 101
```

\033[1m3. Updating Data with PUT Request\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Updating a post

update_payload = {
    "id": 1,
    "title": "Updated Title",
    "body": "Updated body content",
    "userId": 1
}

response = http_put("https://jsonplaceholder.typicode.com/posts/1", data=update_payload)
data = parse_json(response)

print("Updated Title:", data["title"])
\033[36m\033[1m```\033[0m

\033[1mOutput:\033[0m
```
Updated Title: Updated Title
```

\033[1m4. Deleting a Resource\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Deleting a post

response = http_delete("https://jsonplaceholder.typicode.com/posts/1")
print("Delete Response:", response)
\033[36m\033[1m```\033[0m

\033[1mOutput:\033[0m
```
Delete Response: {}
```

\033[1m5. Handling JSON Data\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Parsing and Manipulating JSON

json_text = '{"name": "Alice", "age": 30, "hobbies": ["reading", "cycling"]}'
data = parse_json(json_text)

print("Name:", data["name"])
print("Age:", data["age"])
print("First Hobby:", data["hobbies"][0])

# Modifying data
data["age"] = 31
updated_json = to_json(data)
print("Updated JSON:", updated_json)
\033[36m\033[1m```\033[0m

\033[1mOutput:\033[0m
```
Name: Alice
Age: 30
First Hobby: reading
Updated JSON: {"name": "Alice", "age": 31, "hobbies": ["reading", "cycling"]}
```

\033[1m[!] Warning:\033[0m
When performing HTTP operations, ensure that you handle exceptions and validate responses to avoid unexpected errors. Avoid sending sensitive information without proper encryption.
""",

    # Page 12 - Socket Programming
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 12: Socket Programming\033[0m
================================================================================

UniLang Script allows low-level network communication through socket programming.
This enables the creation of custom network applications such as clients and servers.

\033[1mSocket Operations:\033[0m
- \033[1mcreate_socket()\033[0m: Creates a new TCP socket.
- \033[1mconnect_socket(sock, host, port)\033[0m: Connects the socket `sock` to the specified `host` and `port`.
- \033[1msend_socket(sock, data)\033[0m: Sends data through the connected socket `sock`.
- \033[1mreceive_socket(sock, buffer_size=1024)\033[0m: Receives data from the socket `sock` with an optional buffer size.
- \033[1mclose_socket(sock)\033[0m: Closes the socket `sock`.

\033[1mExamples:\033[0m

\033[1m1. Simple TCP Client\033[0m
\033[36m\033[1m```uls\033[0m
# Example: TCP Client that sends a message to a server

sock = create_socket()
if connect_socket(sock, "localhost", 8080) {
    send_socket(sock, "Hello, Server!")
    response = receive_socket(sock)
    print("Server says:", response)
    close_socket(sock)
} else {
    print("Failed to connect to the server.")
}
\033[36m\033[1m```\033[0m

\033[1m2. Simple TCP Server\033[0m
\033[36m\033[1m```uls\033[0m
# Example: TCP Server that echoes received messages

import socket

def handle_client(client_sock):
    message = receive_socket(client_sock)
    print("Received:", message)
    send_socket(client_sock, "Echo: " + message)
    close_socket(client_sock)

server_sock = create_socket()
server_sock.bind(("localhost", 8080))
server_sock.listen(5)
print("Server listening on port 8080...")

while true {
    client, addr = server_sock.accept()
    print("Connection from", addr)
    handle_client(client)
}
\033[36m\033[1m```\033[0m

\033[1m3. Multi-client TCP Server with Threads\033[0m
\033[36m\033[1m```uls\033[0m
# Example: TCP Server handling multiple clients asynchronously

import socket, threading

def handle_client(client_sock, addr):
    print("Connected to", addr)
    while true {
        data = receive_socket(client_sock)
        if data == "" {
            break
        }
        print(f"Received from {addr}: {data}")
        send_socket(client_sock, f"Echo: {data}")
    close_socket(client_sock)
    print("Connection closed with", addr)

server_sock = create_socket()
server_sock.bind(("localhost", 8080))
server_sock.listen(5)
print("Multi-client server listening on port 8080...")

while true {
    client_sock, addr = server_sock.accept()
    thread = threading.Thread(target=handle_client, args=(client_sock, addr))
    thread.start()
}
\033[36m\033[1m```\033[0m

\033[1m[!] Warning:\033[0m
- \033[1mSecurity Risks:\033[0m
  - \033[1mExposure:\033[0m Opening sockets can expose your system to network attacks. Ensure proper validation and handling of incoming data.
  - \033[1mPort Usage:\033[0m Avoid binding to privileged ports (below 1024) without necessary permissions.
  
- \033[1mResource Management:\033[0m
  - \033[1mClosing Sockets:\033[0m Always close sockets after communication to free system resources.
  - \033[1mException Handling:\033[0m Handle exceptions to prevent crashes and resource leaks.
""",

    # Page 13 - Asynchronous Programming
    """\033[1m\033[4mUniLang Script (ULS) Manual - Page 13: Asynchronous Programming\033[0m
================================================================================

UniLang Script supports asynchronous programming using `async` blocks and the `await` keyword.
This allows concurrent execution of tasks, improving performance, especially for I/O-bound operations.

\033[1mAsync/Await\033[0m
- \033[1masync { ... }\033[0m: Defines an asynchronous block of code.
- \033[1mawait\033[0m: Pauses the execution of an async block until the awaited operation completes.

\033[1mExamples:\033[0m

\033[1m1. Asynchronous HTTP Requests\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Fetching multiple URLs asynchronously

async {
    urls = [
        "https://api.agify.io?name=michael",
        "https://api.agify.io?name=emma",
        "https://api.agify.io?name=olivia"
    ]
    
    for url in urls {
        async {
            response = await http_get(url)
            data = parse_json(response)
            print(f"Name: {data['name']}, Predicted Age: {data['age']}")
        }
    }
}
\033[36m\033[1m```\033[0m

\033[1mOutput:\033[0m
```
Name: michael, Predicted Age: 69
Name: emma, Predicted Age: 29
Name: olivia, Predicted Age: 31
```

\033[1m2. Asynchronous File I/O\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Reading multiple files asynchronously

async {
    files = ["file1.txt", "file2.txt", "file3.txt"]
    
    for filename in files {
        async {
            content = await read_file(filename)
            print(f"Contents of {filename}:\n{content}")
        }
    }
}
\033[36m\033[1m```\033[0m

\033[1m3. Combining Async with Socket Programming\033[0m
\033[36m\033[1m```uls\033[0m
# Example: Asynchronously handling multiple socket connections

import socket, asyncio

async {
    server_sock = create_socket()
    server_sock.bind(("localhost", 9090))
    server_sock.listen(5)
    print("Async server listening on port 9090...")
    
    while true {
        client_sock, addr = await asyncio.accept(server_sock)
        print("Connected to", addr)
        
        async {
            while true {
                data = await receive_socket(client_sock)
                if data == "" {
                    break
                }
                print(f"Received from {addr}: {data}")
                await send_socket(client_sock, f"Echo: {data}")
            }
            close_socket(client_sock)
            print("Connection closed with", addr)
        }
    }
}
\033[36m\033[1m```\033[0m

\033[1m[!] Warning:\033[0m
- \033[1mComplexity:\033[0m Asynchronous programming can introduce complexity such as race conditions and deadlocks. Ensure proper synchronization where necessary.
- \033[1mError Handling:\033[0m Always handle exceptions within async blocks to prevent unexpected crashes.
- \033[1mResource Management:\033[0m Similar to synchronous operations, ensure that all resources (e.g., sockets, files) are properly managed and closed.
""",
]


  

