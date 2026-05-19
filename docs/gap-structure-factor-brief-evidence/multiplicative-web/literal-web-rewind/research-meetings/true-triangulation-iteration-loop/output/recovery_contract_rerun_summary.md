# Recovery Contract Rerun Summary

The 128-bit and 256-bit rungs were rerun under the public evidence integrity
contract.

The public phase emitted actual distance nominations from `N` alone. The
private audit phase used only the canonical membership checker. No known-factor
rank, score, band position, or containment calculation was performed.

## 128-Bit Rung

- public output: `output/recovery_contract_128bit/public/public_output.jsonl`
- public output SHA-256: `33c90a29d0d3b807f9407c10f4d40dae4a1eaa02145225b47eb6bfd49d83908b`
- public record count: `30`
- audit status: `missed`
- status SHA-256: `b10f1db41d94742b016ef61a5542c0b4923c48a6f4146e15f7a5a65d8138d4e5`

## 256-Bit Rung

- public output: `output/recovery_contract_256bit/public/public_output.jsonl`
- public output SHA-256: `50a6c06438d1583fe225b0b06684f2c595b9ca16635b732997840689d1b830b5`
- public record count: `30`
- audit status: `missed`
- status SHA-256: `b10f1db41d94742b016ef61a5542c0b4923c48a6f4146e15f7a5a65d8138d4e5`

## Status Meaning

`missed` means the frozen public nomination file did not emit either hidden
factor distance. It does not mean containment, partial recovery, or scale
progress.

The previous 128-bit and 256-bit rank-audit artifacts are not admissible
recovery evidence under this contract because they measured known-factor
positions after the fact.
