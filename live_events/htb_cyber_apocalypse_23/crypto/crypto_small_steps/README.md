# Files

The package includes two files:

- `server.py`: code running on the TCP server
- `solver.py`: a Python script designed to help users unfamiliar with pwntools connect to the TCP server

# Connection

There are two ways to connect to the server:

## Method 1: nc

You can use `nc` with the IP and PORT provided by our platform when you click the spawn button. For example:

```bash
nc 10.10.1.104 4387
```

## Method 2: solver.py

You can also use the `solver.py` script to connect to the server. There are two ways to run the script:

### Option 1: Local connection

If you run the following command:

```bash
python3 solver.py
```

The script will try to find a `server.py` script in the current directory and interact with the process locally.

### Option 2: Remote connection

If you run the script with the `REMOTE` flag, you can specify a remote `HOST` to connect to. For example:

```bash
python3 solver.py REMOTE HOST=10.10.1.104:4387
```

This will attempt to connect to the specified `HOST` and interact with it.

# Hints

The implementation is textbook RSA, except for the value of `e`.
