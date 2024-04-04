Task-Manager creates a server that accepts the incoming requests from different services at localhost:3000 and returns the response of those requests

# File Description:

<code>scheduler</code>: It is a binary file of a service that sends requests to the server and outputs the response received (testing purpose)

<code>cmd</code>: It is a binary file that processes the requests from the scheduler (testing purpose)

<code>input.json</code>: This file helps to give custom inputs for the scheduler

<code>server.py</code>: This is the main server file that will handle all the requests from the schdeuler service and return it after getting the response for the requests


# How To Run:
- Download all the files in one place
- Start the server by running the command <code>python3 server.py</code> in the terminal --> this should show an output like "Server is listening on port 3000..."
- Run the scheduler service by running <code>./scheduler</code> command in the different tab --> This will sequentially run the all the requests from the scheduler
- Additionally there are two more options to run the scheduler: 
  1) For custom inputs, enter inputs in the input.json and use the command like <code>./scheduler -input input.json</code>
  2) For running the requests in parallel, use the -concurrent flag like  <code>./scheduler -input input.json -concurrent</code>

# Server.py
- Introduction:
  1) Intializing a TCP server listening on localhost (127.0.0.1) on port 3000.
  2) Upon accepting a connection from a client, it spawns a new thread to handle the client's requests concurrently.
  3) <code>handle_client</code>: Continuously reads data from the client socket, splits it into individual requests, and spawns a new thread to handle each request in parallel using the handle_request function. Additionally, it handles exceptions and closes the client socket gracefully.
  4) <code>handle_request</code>: Parses the incoming request string into a TaskRequest, executes the task, converts the result to JSON format, and sends it back to the client socket.
  5) <code>execute_task</code>: function is responsible for executing a given task request and returning a TaskResult object. It records the start time to measure the duration of task execution. It attempts to execute the task using the subprocess.run() function, capturing its output. If the task execution is successful within the specified timeout (if any), it records the exit code, output, and any potential errors. If the task exceeds the timeout duration, it sets the exit code to -1 and indicates a timeout error.  If an exception occurs during task execution, it captures the exception details and treats it as an error. It calculates the duration of task execution, creates a TaskResult object with the execution details, and returns it.
