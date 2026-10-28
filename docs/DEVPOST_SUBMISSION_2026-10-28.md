## Inspiration
Travel planning usually stops at a list of places. Travelers still have to decide what fits their taste, fill the gaps between activities, and call a restaurant in a language they may not speak. TasteTrip connects those steps in one conversational experience.

TasteTrip was built from scratch for the Qloo Agentic Hackathon, starting on October 20, 2026, using third-party APIs and open-source libraries.

## What it does
TasteTrip learns preferences through conversation and stores explicitly shared tastes in a reusable profile. A traveler can ask for a two-day trip to Paris, receive a personalized route, save it, and ask to move an existing museum stop from day two to day one.

The itinerary can include restaurants, cafes, bars, hotels, museums, parks and attractions, depending on available Qloo results. Place cards expose available business details and map links. During a break or journey, the traveler can explicitly request books, films, podcasts or artist recommendations. Optional Aviasales integration provides airport discovery and cached flight prices.

For a restaurant reservation, the traveler supplies the date, restaurant-local time, party size, booking name and special requests. The app requires business/phone and local-time verification, then a separate approval of the exact terms and paid call. Anna introduces herself as a digital assistant and calls on the traveler's behalf. The traveler can listen live and follow translated captions in their native language in a popup. After the call, the app returns to chat with a summary and a separate reservation outcome.

The interface starts in English, while assistant replies follow the language of the traveler's message. Sign-in is requested for actions such as saving routes and preparing reservations, rather than blocking initial exploration.

## Why it is Qloo-powered
Qloo grounds discovery in cultural taste. TasteTrip resolves supported favorites into Qloo entity and tag IDs, stores validated preferences, and sends relevant profile signals with destination context to place and content queries. Food-related constraints are applied to relevant place queries, rather than unrelated books or museums.

The LLM interprets the conversation and organizes Qloo's candidate places into an itinerary. Server validation constrains generated plans to known candidates. Without Qloo, the app would lose its taste-based candidate selection and cross-category cultural discovery; a generic LLM list would not provide the same recommendation foundation.

## How we built it
The application uses Python/Flask, SQLite and a vanilla JavaScript/CSS frontend. An OpenAI-compatible LLM integration currently uses DeepSeek for preference extraction, planning, edits, voice conversation, translation and summaries. Qloo provides place and cultural discovery. The optional flight adapter uses Aviasales/Travelpayouts.

The reservation system uses a durable outbox and a separate worker, Twilio telephony, Deepgram speech recognition and ElevenLabs speech synthesis with Anna as the main voice. A language router selects Flash v2.5 for supported languages and v3 for supported fallback languages, subject to voice and recognition support. Signed listener access protects live audio; explicit approval, ownership checks and idempotency protect call dispatch.

The live application runs as three services on a Hetzner ARM64 server through Coolify: web, voice gateway and reservation worker. The repository includes a Dockerfile, Compose configuration, persistent-data setup and an English installation guide. The application code is MIT-licensed.

## Challenges and lessons
Turning natural language into stable taste signals required separating long-term preferences from one-trip requests and validating entity IDs. Restaurant records also vary in phone, image and menu availability; missing data must stay visible rather than being invented.

Calls introduce different uncertainties: the phone can end without a confirmed reservation, a transcript can be incomplete, and a generated summary can sound more certain than the evidence. We therefore keep phone status and booking outcome separate, require explicit approval, preserve uncertain outcomes, and avoid automatic redialing. Closing the listening popup does not stop the phone call; a separate stop control does.

## Accomplishments
We shipped an externally hosted conversational travel application with Qloo discovery, reusable taste profiles, saved and editable itineraries, user-triggered cultural recommendations and an approved restaurant-calling workflow. The latest recorded full suite passed 126 tests. Isolated browser tests exercised verification gates, separate paid-call approval, the live-call popup, close/reopen and the pending-to-ready summary handoff.

The gallery's reservation screenshots use synthetic QA data and a simulated conversation; they are interface demonstrations, not evidence of a completed restaurant booking. Production health and worker readiness have been verified. The newly deployed complete product flow has not yet been validated through a new real restaurant booking.

## Try it
Live application: https://tastetrip.bahadirciftci.work
Public source code: https://github.com/baadir/tastetrip
Setup guide: https://github.com/baadir/tastetrip/blob/main/docs/INSTALLATION.md

Start by sharing what you enjoy and where you want to go. For example: “I enjoy art museums, quiet cafes and local food. Plan two days in Paris for three people.” Supply your travel dates when asked, review the itinerary, then ask to rearrange an existing stop. Cultural recommendations are available on request. Judges can explore planning without signing in; saving and reservation preparation require a free account. Real calls require explicit paid-call approval and incur provider costs.

## Current limits and what's next
Itineraries do not guarantee actual travel times, date-specific opening hours or availability. Flight data is cached, not confirmed ticket inventory. Artist discovery is not a playable playlist. Book/podcast language filtering depends on available metadata; film-language filtering is not implemented. Current itinerary editing rearranges existing stops.

Next steps are broader multilingual call evaluation, route-feasibility data, a clearer workflow for restaurant-proposed alternatives, and more destination and device testing. Hotel/museum ticket booking and payment are outside the current implementation. Allergen-related notes are requests to verify, not food-safety certification.

## Screenshots

Conversational welcome screen:

![TasteTrip conversational welcome](https://raw.githubusercontent.com/baadir/tastetrip/main/docs/images/chat-welcome.png)

Reservation approval and live call interface (synthetic QA data; simulated call):

![Explicit reservation approval](https://raw.githubusercontent.com/baadir/tastetrip/main/docs/images/reservation-approval.png)

![Live call popup](https://raw.githubusercontent.com/baadir/tastetrip/main/docs/images/live-call.png)