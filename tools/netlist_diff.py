#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Diff OrCAD pstxnet.dat vs board allpins.txt — connectivity as node SETS, name-agnostic."""
import re
import sys
from pathlib import Path
from collections import defaultdict

def parse_pstxnet(path):
    nets = {}
    cur = None
    expect_name = False
    for raw in open(path, encoding='utf-8', errors='replace'):
        line = raw.rstrip('\n')
        s = line.strip()
        if s == 'NET_NAME':
            expect_name = True
            cur = None
            continue
        if expect_name:
            m = re.match(r"^'([^']+)'$", s)
            if m:
                cur = m.group(1)
                nets.setdefault(cur, set())
            expect_name = False
            continue
        m = re.match(r'^NODE_NAME\s+(\S+)\s+(\S+)', s)
        if m and cur is not None:
            nets[cur].add((m.group(1), m.group(2)))
    return nets

def parse_board(path):
    bynet = defaultdict(set)
    for line in open(path, encoding='utf-8', errors='replace'):
        m = re.match(r'^PIN\s+(\w+)\."?(\w+)"?\s+(\S+)\s', line)
        if m and m.group(3) != 'nil':
            bynet[m.group(3)].add((m.group(1), m.group(2)))
    return dict(bynet)

sch_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / 'allegro/pstxnet.dat'
brd_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('allpins.txt')
print(f'SCHEMATIC SOURCE: {sch_path.resolve()}')
print(f'BOARD SOURCE (read-only): {brd_path.resolve()}')
sch = parse_pstxnet(sch_path)
brd = parse_board(brd_path)
print(f'schematic nets: {len(sch)}  board nets: {len(brd)}')

sch_idx = {frozenset(v): k for k, v in sch.items()}
brd_idx = {frozenset(v): k for k, v in brd.items()}

exact = sum(1 for v in sch.values() if frozenset(v) in brd_idx)
only_sch = [(k, v) for k, v in sch.items() if frozenset(v) not in brd_idx]
only_brd = [(k, v) for k, v in brd.items() if frozenset(v) not in sch_idx]
print(f'exact node-set matches: {exact}')
print(f'unmatched schematic nets: {len(only_sch)}, unmatched board nets: {len(only_brd)}')

# near-miss pairing to name the deltas
print('\n=== near-miss pairs (schematic vs board), sorted by overlap:')
pairs = []
for k1, n1 in only_sch:
    s1 = frozenset(n1)
    best = None
    for k2, n2 in only_brd:
        s2 = frozenset(n2)
        ov = len(s1 & s2)
        if ov and (best is None or ov > best[0]):
            best = (ov, k2, n2)
    if best:
        ov, k2, n2 = best
        pairs.append((ov, k1, n1, k2, n2))
    else:
        pairs.append((0, k1, n1, None, None))
pairs.sort(key=lambda x: -x[0])
for ov, k1, n1, k2, n2 in pairs:
    if k2 is None:
        print(f'  SCH[{k1}] ({len(n1)} nodes) NO board overlap at all: {sorted(n1)}')
    else:
        miss_in_brd = sorted(set(n1) - set(n2))
        extra_in_brd = sorted(set(n2) - set(n1))
        print(f'  ov={ov} SCH[{k1}] vs BRD[{k2}]  sch_only={miss_in_brd}  brd_only={extra_in_brd}')
print('\n=== board nets never overlapped by any schematic net:')
used = set()
for ov, k1, n1, k2, n2 in pairs:
    if k2: used.add(k2)
for k, v in sorted(only_brd, key=lambda x: -len(x[1])):
    if k not in used:
        print(f'  BRD[{k}] ({len(v)} nodes): {sorted(v)}')
