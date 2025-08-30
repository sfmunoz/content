---
title: 'LVM snapshots'
summary: 'LVM snapshots usage in a backup and restore procedure'
url: 'tips/:slug'
date: '2025-06-25T15:33:46Z'
categories: ['tips']
tags: ['lvm','backup','restore']
draft: false
legacy_id: 4171
---

## 1. LV setup
Create a **test** LV:
```
# lvcreate -n test -L 500m vg0
```
## 2. LV backup creation
**Preferred**: make sure **/dev/vg0/test** is unmounted
```
# lvcreate -n test-bck -L 500m -s /dev/vg0/test
```
**Notice**: both **/dev/vg0/test** and **/dev/vg0/test-bck** may be used although the usual case is to keep using **/dev/vg0/test**
## 3a. LV backup restore
**Preferred**: make sure **/dev/vg0/test-bck** is unmounted
```
# lvconvert --merge -i 1 /dev/vg0/test-bck
```
## 3b. LV backup removal
When restore is not required:
```
# lvremove /dev/vg0/test-bck
```

> [!WARNING]
> If possible don't use `lvchange -an /dev/vg0/test-bck` since it can lead to data loss (at least I managed to loss some data).

## XFS: mount both at a time

Problem trying to mount **/dev/vg0/test-bck** when **/dev/vg0/test** is already mounted (XFS):
```
# mount -o ro /dev/vg0/test-bck /mnt2
mount: wrong fs type, bad option, bad superblock on /dev/mapper/vg0-test-bck,
     missing codepage or helper program, or other error
     In some cases useful info is found in syslog - try
     dmesg | tail  or so

# dmesg
(...)
[ 6217.169848] XFS (dm-6): Filesystem has duplicate UUID - can't mount
```
**Fix 1**: use **nouuid** option:
```
# mount -o ro,nouuid /dev/vg0/test-bck /mnt2
(... nothing ...)
```
**Fix 2**: generate new **UUID** (notice that this changes the snapshot):
```
# xfs_admin -U generate /dev/vg0/test-bck
Clearing log and setting UUID
writing all SBs
new UUID = 38a8b708-a06f-4b5e-9de2-f8192dad21cc

# mount -o ro /dev/vg0/test-bck /mnt2
(... nothing ...)
```
