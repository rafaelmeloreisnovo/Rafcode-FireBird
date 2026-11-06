# ISO 8000-oriented data-quality engineering (informative; not certification)

**Important taxonomy:** ISO 8000 is a *data-quality* standards family, not a generic document formatting standard. Standards are copyrighted; this document references titles/scope only and does not reproduce normative text.

- ISO 8000-61:2016 (https://www.iso.org/standard/63086.html): data quality management process reference model.
- ISO 8000-63:2019 (https://www.iso.org/standard/65344.html): process measurement; goal → subgoal → question → indicator → metric.
- RFC 5424 (https://www.rfc-editor.org/rfc/rfc5424.html): event message format, not audit-record storage or authentication.

| Quality question | Indicator (planned) | Metric/gate | Current observation |
| --- | --- | --- | --- |
| Can source be located? | repo + exact SHA | 3/3 pinned source roles | Registry implemented; actual source fetch not automatic |
| Is a missing value explicit? | known bit/type | 0 cases treating unknown as 0 | C synthetic tests, CI pending for new module |
| Are schema/version semantics reconstructible? | version, policy revision, source SHA | rejected invalid/duplicate/stale values | Spec+tests provided |
| Does an event reveal user data? | only enums/counters in preview | zero free-text interpolations | Static property; external privacy review NOT_RUN |
| Can failure be contained? | disable/failback result | 10k synthetic transitions; no DB intervention | NOT_RUN until exact-head CI |
| Is evidence authenticated? | independent signer + checkpoint | signatures verified externally | NOT_IMPLEMENTED |
| Does failover preserve committed data? | RPO, durability, consistency | independent fault injection | NOT_RUN |

**Control:** objective, measurement semantics, data origin, unit, sampling cadence, confidence, denominator, observed result, falsifier and new evidence ref are required before claiming a quality level. An empty or unobservable denominator is `TOKEN_VAZIO`, not 100%.

Docs lifecycle: `AUTHOR -> REVIEW -> TEST -> EVIDENCE -> VERSION -> RELEASE_NOTE -> RETIRE/SUPERSEDE`. Do not mistake a comment/diagram or an LLM summary for the primary source or execution receipt.

ISO 8000 conformity requires a separately scoped assessment against applicable normative clauses and official licensed materials; nothing here constitutes one.
