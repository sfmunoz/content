# Python subprocess

Python **subprocess.call()** and **subprocess.Popen()** examples

- [References](https://gist.github.com/sfmunoz/4127f06554f25e022eb26496c0363dc2#references)
- [Simplified usage](https://gist.github.com/sfmunoz/4127f06554f25e022eb26496c0363dc2#simplified-usage)
- [subprocess.Popen()](https://gist.github.com/sfmunoz/4127f06554f25e022eb26496c0363dc2#subprocesspopen)

## References

- http://docs.python.org/library/subprocess.html

## Simplified usage

**call(shell=True)** means a subshell is created to run the command (a string):

```python
>>> from subprocess import call
>>> ret = call("ls -l /tmp/",shell=True)
```

**call(shell=False)** means an array must be used (there's no subshell):

```python
>>> ret = call(["ls","-l","/tmp/"])
```

For a command with no arguments we can use:

```python
>>> ret = call("ls")
```

## subprocess.Popen()

Code:

```python
$ cat sp.py 
from subprocess import Popen, PIPE
if __name__ == "__main__":
    cmd = ['awk','BEGIN { if (ENVIRON["SP_FAIL"]=="1") { print("error: SP_FAIL=1") > "/dev/stderr"; exit(1); } } { printf("%d: %s\\n",NR,$0); }']
    p = Popen(args=cmd,stdin=PIPE,stdout=PIPE,stderr=PIPE)
    (odata,edata) = p.communicate(b"first line\nsecond line\nlast line\n")
    if p.returncode != 0:
        raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
    print(odata.decode().strip())
```

Successful execution:

```
$ python3 sp.py
1: first line
2: second line
3: last line
```

Forced failure:

```
$ SP_FAIL=1 python3 sp.py 
Traceback (most recent call last):
  File "/tmp/sp.py", line 8, in <module>
    raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
Exception: 'awk BEGIN { if (ENVIRON["SP_FAIL"]=="1") { print("error: SP_FAIL=1") > "/dev/stderr"; exit(1); } } { printf("%d: %s\n",NR,$0); }' command failed: error: SP_FAIL=1
```

Taking the following information into account **p.communicate()** is preferred instead of **p.wait()**:
	
> [https://docs.python.org/3/library/subprocess.html](https://docs.python.org/3/library/subprocess.html)\
> (...)\
> **Popen.wait(timeout=None)**\
> Wait for child process to terminate. Set and return returncode attribute.
>
> If the process does not terminate after timeout seconds, raise a TimeoutExpired exception. It is safe to catch this exception and retry the wait.
>
> **Note**\
> This will deadlock when using stdout=PIPE or stderr=PIPE and the child process generates enough output to a pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use Popen.communicate() when using pipes to avoid that.
>
> **Note**\
> When the timeout parameter is not None, then (on POSIX) the function is implemented using a busy loop (non-blocking call and short sleeps). Use the asyncio module for an asynchronous wait: see asyncio.create_subprocess_exec.
>
> Changed in version 3.3: timeout was added.\
> (...)

---

#tip 5113