# Distributed rk4 integration

split up a task and give it to multiple web clients to do that work in js in their browser, then aggregate the results

At the cost of much performance the client does not need to install anything, theoretically making use of idle devices

proof of concept using a simple additive numerical integration that is easy to split into chunks

## Use

recommended for learning purposes only

insecure (for local network only):

    pip install flask flask-session

    python3 app.py

## Development notes

### TODO

- implement a mechanism to deal with exiting the page or reloading. prbably track pending tasks per client and only allow one task per client
- implement main server loop to allow user to query current state of the integration
- make it easier to change the function/task other than directly editing the js script, config file.
- implement logging over print
- BUG: updating the current task in the client window doesn't work
- FUTURE: validate data integrity
