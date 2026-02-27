# content

> [!WARNING]
> **DO NOT EDIT**: this **README.md** file was automatically generated on **2026-02-27 06:04:50 UTC** by the **build.py** script based on the contents of the repository.

https://sfmunoz.com/ site content

## Architecture

```mermaid
flowchart LR
    user(["user"])
    sfmunoz("`sfmunoz.github.io<br>**frontend**<br>SvelteKit`")
    cms("`cms<br>**backend**<br>Hugo`")
    content("`content<br>**data**<br>Git`")
    style content stroke-width:4px
    user -->|https| sfmunoz --> cms --> content
```

## g

* [golang-exec-command](g/go/golang-exec-command/index.md)

## j

* [jq-examples](j/jq/jq-examples/index.md)

## l

* [lvm-snapshots](l/lv/lvm-snapshots/index.md)

## p

* [python-http-client](p/py/python-http-client/index.md)
* [python-http-server](p/py/python-http-server/index.md)
* [python-subprocess](p/py/python-subprocess/index.md)

## r

* [runc-basics](r/ru/runc-basics/index.md)
