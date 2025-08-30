---
slug: jq-examples
title: 'jq examples'
summary: 'List of jq examples'
url: 'tips/:slug'
date: '2025-06-24T16:51:14Z'
categories: ['tips']
tags: ['jq','examples']
draft: false
legacy_id: 5012
---

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

## Example 5: compose array of strings from array of dictionaries

```bash
jq '.people | [.[] | {name,age} | join("|")]'
```

```json
["Alfred|34", "Bob|40", "Charles|22"]
```

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
