---
slug: golang-exec-command
title: 'Golang: exec.Command() examples'
summary: 'List of Golang "exec.Command()" examples'
url: 'tips/:slug'
date: '2025-06-21T05:34:05Z'
categories: ['tips']
tags: ['golang','exec','command']
draft: false
legacy_id: 5118
---

## stat-bin.go

```go
$ cat stat-bin.go
package main

import (
        "bytes"
        "log"
        "os"
        "os/exec"
        "strings"
)

func main() {
        folder := "/bin"
        if os.Getenv("FORCE_ERROR") == "1" {
                folder = "/does-not-exist"
        }
        var stdout bytes.Buffer
        var stderr bytes.Buffer
        cmd := exec.Command("stat", folder)
        cmd.Stdout = &stdout
        cmd.Stderr = &stderr
        if err := cmd.Run(); err != nil {
                log.Fatalf("error: 'cmd.Run()' failed: %v -> %s", err, stderr.String())
        }
        lines := strings.Split(stdout.String(), "\n")
        for _, line := range lines {
                if line == "" {
                        continue
                }
                log.Print(line)
        }
}
```
Successful execution:
```
$ go run stat-bin.go
2024/12/11 17:33:29   File: /bin -> usr/bin
2024/12/11 17:33:29   Size: 7           Blocks: 0          IO Block: 4096   symbolic link
2024/12/11 17:33:29 Device: fd03h/64771d        Inode: 132         Links: 1
2024/12/11 17:33:29 Access: (0777/lrwxrwxrwx)  Uid: (    0/    root)   Gid: (    0/    root)
2024/12/11 17:33:29 Access: 2024-12-10 19:07:43.216006371 +0000
2024/12/11 17:33:29 Modify: 2023-06-10 10:38:34.042107526 +0000
2024/12/11 17:33:29 Change: 2023-06-10 10:38:34.042107526 +0000
2024/12/11 17:33:29  Birth: 2023-06-10 10:38:34.042107526 +0000
```
Failed execution:
```
$ FORCE_ERROR=1 go run stat-bin.go
2024/12/11 17:33:31 error: 'cmd.Run()' failed: exit status 1 -> stat: cannot statx '/does-not-exist': No such file or directory
exit status 1
```
## head-5-cat-n.go
```go
$ cat head-5-cat-n.go
package main

import (
        "log"
        "os"
        "os/exec"
)

func main() {
        buf, err := os.ReadFile("head-5-cat-n.go")
        if err != nil {
                log.Fatal("error: 'os.ReadFile()' failed", "err", err)
        }
        cmd := exec.Command("/bin/bash", "-c", "head -n 5 | cat -n")
        cmd.Stdout = os.Stdout
        cmd.Stderr = nil // == /dev/null
        stdin, err := cmd.StdinPipe()
        if err != nil {
                log.Fatal("error: 'cmd.StdinPipe()' failed: %v", err)
        }
        if err := cmd.Start(); err != nil {
                log.Fatal("error: 'cmd.Start()' failed: %v", err)
        }
        _, err = stdin.Write([]byte(buf))
        if err != nil {
                log.Fatal("error: 'stdin.Write()' failed: %v", err)
        }
        err = stdin.Close()
        if err != nil {
                log.Fatal("error: 'stdin.Close()' failed: %v", err)
        }
        err = cmd.Wait()
        if err != nil {
                log.Fatal("error: 'cmd.Wait()' failed: %v", err)
        }
}
```
Execution:
```
$ go run head-5-cat-n.go
     1  package main
     2
     3  import (
     4          "log"
     5          "os"
```
## cat-pipe.go
```go
$ cat cat-pipe.go
package main

import (
        "bufio"
        "fmt"
        "log"
        "os/exec"
        "time"
)

func main() {
        cmd := exec.Command("cat", "-n")
        cmd.Stderr = nil // == /dev/null
        stdin, err := cmd.StdinPipe()
        if err != nil {
                log.Fatal("error: 'cmd.StdinPipe()' failed: %v", err)
        }
        stdout, err := cmd.StdoutPipe()
        if err != nil {
                log.Fatal("error: 'cmd.StdoutPipe()' failed: %v", err)
        }
        if err := cmd.Start(); err != nil {
                log.Fatal("error: 'cmd.Start()' failed: %v", err)
        }
        go func() {
                for i := 0; i < 5; i++ {
                        if i > 0 {
                                time.Sleep(time.Second)
                        }
                        _, err = stdin.Write([]byte(fmt.Sprintf("**** %d ****\n", i)))
                        if err != nil {
                                log.Fatal("error: 'stdin.Write()' failed: %v", err)
                        }
                }
                err = stdin.Close()
                if err != nil {
                        log.Fatal("error: 'stdin.Close()' failed: %v", err)
                }
        }()
        scanner := bufio.NewScanner(stdout)
        for scanner.Scan() {
                line := scanner.Text()
                log.Print(">>> " + line)
        }
        if err := scanner.Err(); err != nil {
                log.Fatal("error: 'scanner.Err()' is not nil: %v", err)
        }
        err = cmd.Wait()
        if err != nil {
                log.Fatal("error: 'cmd.Wait()' failed: %v", err)
        }
}
```
Execution:
```
$ go run cat-pipe.go
2024/12/11 17:39:44 >>>      1  **** 0 ****
2024/12/11 17:39:45 >>>      2  **** 1 ****
2024/12/11 17:39:46 >>>      3  **** 2 ****
2024/12/11 17:39:47 >>>      4  **** 3 ****
2024/12/11 17:39:48 >>>      5  **** 4 ****
```
