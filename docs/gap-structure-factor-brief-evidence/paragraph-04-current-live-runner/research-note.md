# Paragraph 04 Research Note

## Plain Claim

The fourth panel should report the current implementation surface exactly:
three committed ladder rows, with public inference and downstream audit shown
as separate columns.

## Draft Public Paragraph

The live runner now has a clear committed surface. On the 40-bit row, public
endpoint closure emits a factor endpoint and downstream audit confirms it. On
the 50-bit row, the public structure reaches a carrier mismatch and the runner
returns unresolved before audit. On the 64-bit row, mutual public closure emits
a factor endpoint and downstream audit confirms it. These rows are
implementation evidence for the current rule, not a universal theorem.

## Evidence Status

```text
implementation_status = live runner emits committed rows
measured_status = three official ladder rows recorded
audit_status = 40-bit true, 50-bit false, 64-bit true
theorem_status = no universal factor theorem claimed
```

## Infographic Direction

Use a three-row ladder with two columns: public inference and downstream audit.

