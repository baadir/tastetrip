# TasteTrip hackathon eligibility review

Checked 28 October 2026. This is an evidence-based project review, not an organizer eligibility decision. No submission content was modified.

## Assessment

The project fits the Qloo/agentic theme and has a submitted entry, public repository, detected MIT license, external demo, English project story, and English setup instructions. A fresh anonymous production test succeeded for conversation and Qloo-backed itinerary generation. Full eligibility remains conditional on functional voice testing, evaluator access and participant/IP declarations.

## Observed evidence

| Item | Evidence | Assessment |
| --- | --- | --- |
| Submitted entry | H-087: Project submitted! and SUBMITTED TO Qloo Agentic Hackathon | Verified submission receipt; not organizer approval |
| Recommendation integration | providers.py sends entity/tag signals to Qloo search/Insights; planner.py validates LLM assignments against returned candidates | Meaningful Qloo role, rather than a name-only integration |
| Live application | HTTPS /health 200; isolated anonymous chat 200 with plan action | Entry and core conversation available without login |
| Live planning | Anonymous /api/plan 200 in 19 seconds; mode LLM + Qloo; two days, eight stops, no warnings | New production evidence for core planning |
| Voice readiness | /api/reservations/options 200, worker_available=true | Readiness only; no new actual call or confirmed booking tested |
| Repository | Public GitHub page includes source folders, Docker/Compose, README and setup guide | Required artifacts present; clean-machine installation not repeated |
| License | GitHub public page explicitly displays MIT license in About/Resources | Detection requirement verified after publication |
| Language | English public story, README, installation guide and current fixed UI | Historical Turkish working documents remain in repository; not a claim that every repository document is translated |
| Timing | Recorded project work begins 20 October; Git history begins 27 October; submission completed 28 October | Within the published submission window; chronology is not a full provenance audit |

The anonymous production check used synthetic travel preferences, not the user's browser conversation. It created only a separate anonymous chat/draft. No account, account-saved itinerary, reservation or telephone call was created.

## Open risks

1. **Evaluator access:** the submitted story and call UI describe paid-call approval/provider charges. The server uses configured provider accounts and no new billing flow was demonstrated, but the wording may imply evaluator payment. Confirm that judges can test the claimed features free, without supplying keys, and explain provider cost coverage/test access clearly. A free account step is not automatically disqualifying; the rules explicitly contemplate private-site credentials. Daily call caps and access gates need to permit meaningful evaluation. No exemption is assumed.
2. **Voice functionality:** synthetic popup tests and worker health do not prove a complete production reservation conversation. Before the deadline, validate an authorized controlled call with listening, captions, outcome and summary, or narrow unsupported claims. Real calls were not authorized for this review and were not made.
3. **Ownership and integrations:** development history includes design/API references. That does not itself establish copied code or an infringement. If existing code was carried over, the from-scratch/new-project description must accurately reflect it. Confirm ownership, dependency/content licenses, provider rights, absence of disqualifying support and conflicts, and participant majority/residency; these were not independently certified.
4. **Availability:** maintain the app and provider access through evaluation. The formal rules currently end judging at 5 November 23:45 Eastern (6 November 07:45 Europe/Istanbul), later than the Schedule page's judging end. Use the later bound for availability; resolve ambiguity with the organizer if necessary.

Video is not required by the overview. External paid APIs, a custom agent implementation and AI coding assistance are not, by themselves, stated disqualifiers in the reviewed rules. This does not certify all third-party contract or IP requirements.

## Sources

- Official rules, especially sections 3–4, 6 and 11: https://qloo.devpost.com/rules
- Public requirements and video note: https://qloo.devpost.com/
- Schedule: https://qloo.devpost.com/details/dates
- Submitted project: https://devpost.com/software/tastetrip-concierge
- Public repository/license detection: https://github.com/baadir/tastetrip

The web extraction tool could not retrieve the submitted project page in this review; the submitted-state and saved-story evidence is the authenticated browser verification recorded in H-086/H-087. This distinction is preserved rather than claiming a new anonymous Devpost page check.
