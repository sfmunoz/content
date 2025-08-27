# jq examples

[jq](https://jqlang.org/) examples

- [References](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#references)
- [Input](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#input)
- [Example 1](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e1): create string out of document data
- [Example 2](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e2): keys
- [Example 3](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e3): get some fields from dictionary
- [Example 4](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e4): get some fields from array of dictionaries
- [Example 5](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e5): compose array of strings from array of dictionaries
- [Example 6](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e6): to_entries
- [Example 7](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e7): convert array to dictionary → from_entries
- [Example 8](https://gist.github.com/sfmunoz/3bbe909b6c578c0c94d2a696b00ce60b#e8): dictionary filter → to_entries + select() + from_entries

## References

- [jq](https://jqlang.org/): a lightweight and flexible command-line JSON processor.
- [jq manual](https://jqlang.org/manual/)
- My https://github.com/jqlang/jq/issues/2246 recap:
  - Q: Is there a jq --slurp builtin .ie the inverse of .[] ?
  - A: No

## Input

```json
{
  "ts": 20250624,
  "title": "Some random data",
  "people": [
    { "name": "Alfred", "age": 34, "country": "Canada" },
    { "name": "Bob", "age": 40, "country": "USA" },
    { "name": "Charles", "age": 22 }
  ],
  "countries": {
    "Canada": { "population": 40, "capital": "Ottawa" },
    "USA": { "population": 340, "capital": "Washington, D.C." },
    "Germany": { "population": 83 },
    "India": { "population": 1438, "capital": "New Delhi" }
  }
}
```

<a name="e1"></a>

## Example 1: create string out of document data

```bash
jq -r '. | "export TS=\"\(.ts)\"\nexport TITLE=\"\(.title)\"\nexport PEOPLE=\"\(.people|length)\"\nexport COUNTRIES=\"\(.countries|length)\""'
```

```
export TS="20250624"
export TITLE="Some random data"
export PEOPLE="3"
export COUNTRIES="4"
```

<a name="e2"></a>

## Example 2: keys

```bash
jq 'keys'
jq keys
```

```json
["countries", "people", "title", "ts"]
```

---

```bash
jq 'keys[]'
jq 'keys | .[]'
```

```
"countries"
"people"
"title"
"ts"
```

---

```bash
jq -r 'keys[]'
jq -r 'keys | .[]'
```

```
countries
people
title
ts
```

<a name="e3"></a>

## Example 3: get some fields from dictionary

```bash
jq '. | {ts,title}'
jq '{ts,title}'
```

```json
{
  "ts": 20250624,
  "title": "Some random data"
}
```

<a name="e4"></a>

## Example 4: get some fields from array of dictionaries

```bash
jq '.people | [.[] | {name,age}]'
```

```json
[
  { "name": "Alfred", "age": 34 },
  { "name": "Bob", "age": 40 },
  { "name": "Charles", "age": 22 }
]
```

<a name="e5"></a>

## Example 5: compose array of strings from array of dictionaries

```bash
jq '.people | [.[] | {name,age} | join("|")]'
```

```json
["Alfred|34", "Bob|40", "Charles|22"]
```

<a name="e6"></a>

## Example 6: to_entries

```bash
jq '.countries | to_entries'
```

```json
[
  {
    "key": "Canada",
    "value": { "population": 40, "capital": "Ottawa" }
  },
  {
    "key": "USA",
    "value": { "population": 340, "capital": "Washington, D.C." }
  },
  {
    "key": "Germany",
    "value": { "population": 83 }
  },
  {
    "key": "India",
    "value": { "population": 1438, "capital": "New Delhi" }
  }
]
```

<a name="e7"></a>

## Example 7: convert array to dictionary → from_entries

```bash
jq '.people | [.[] | {"key":.name,"value":.}] | from_entries'
```

```json
{
  "Alfred": { "name": "Alfred", "age": 34, "country": "Canada" },
  "Bob": { "name": "Bob", "age": 40, "country": "USA" },
  "Charles": { "name": "Charles", "age": 22 }
}
```

<a name="e8"></a>

## Example 8: dictionary filter → to_entries + select() + from_entries

```bash
jq '.countries | to_entries | [.[] | select(.value.population > 100)] | from_entries'
```

```json
{
  "USA": {
    "population": 340,
    "capital": "Washington, D.C."
  },
  "India": {
    "population": 1438,
    "capital": "New Delhi"
  }
}
```

---

#tip 5012
