| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request writes exactly one log line | 15 of 15 | 15/15 | 15/15 | 15/15 |  |
| 2. Logged status matches the response | 15 of 15 | 15/15 | 15/15 | 15/15 |  |
| 3. Cost fields count the right things | 100% of lines | 10/10 | 10/10 | 10/10 |  |
| 4. Model unreachable: logged, server keeps going | 5 of 5 | 5/5 | 5/5 | 5/5 |  |
| 5. Real run under 20 s | median < 20s, 8 of 10 < 30s | median 3.65s, 9/10 < 30s | median 2.54s, 8/10 < 30s | median 4.09s, 8/10 < 30s |  |
