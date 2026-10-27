# Devpost Application Draft

Prepared: October 20, 2026. Not submitted. The authenticated submission form has not yet been inspected.

## Working project name

TasteTrip Concierge

Working name only; not a trademark or availability check.

## Tagline

A travel dining concierge that learns your taste, calls your chosen restaurant, and lets you follow the reservation live in your own language.

## Short concept description

TasteTrip Concierge is a planned agent-powered app for travelers who want dining recommendations that reflect their tastes and help booking across language barriers. It will collect preferences that can be mapped to Qloo entities and tags, use Qloo to recommend relevant restaurants at the destination, and let the traveler choose a venue. A voice agent will then call the restaurant to request a reservation under the traveler's specified conditions. The traveler will be able to listen live and follow translated captions in their native language.

## Problem and audience

Travelers face two connected tasks: finding a restaurant that fits their personal taste and arranging the reservation in a language they may not speak. The proposed product connects discovery with the booking conversation, while keeping the traveler informed about what is being requested and agreed.

## Planned Qloo integration

The app will resolve supported preferences into Qloo entities and tags, then request place recommendations scoped to the destination. Qloo will supply the preference relationships behind candidate selection. The application will handle restaurant selection, booking constraints, conversation orchestration, and reservation status. Restaurant coverage, available metadata, and the contribution of Qloo to recommendation quality must still be validated with live API calls.

## Planned reservation experience

1. Collect destination, preferences, native language, and dining constraints.
2. Present Qloo-powered restaurant candidates.
3. Let the traveler select a restaurant and confirm date, local time, party size, reservation name, and special requests.
4. Call a verified restaurant number through a telephony provider.
5. Generate agent speech using ElevenLabs or an equivalent TTS provider.
6. Stream both sides of the conversation to the traveler.
7. Provide live translated captions when the call language differs from the traveler's native language.
8. Report the restaurant's confirmed outcome; distinguish rejection, disconnection, and uncertain status from success.

The agent will not accept alternatives outside the traveler's agreed constraints without a new decision from the traveler.

## Implementation status — accurate as of this draft

Product requirements and acceptance criteria have been documented. The application, Qloo integration, telephony, TTS, live audio, and translation features have not yet been demonstrated. No functional demo or public source repository URL has been provided for this application.

Do not reuse this draft as a claim that the product is already working. Update it with implemented features and actual validation before final submission.

## Missing submission materials

- Functional externally hosted demo URL.
- Public source repository URL and detected open-source license.
- Verified implementation details and test instructions.
- Any additional fields required by the authenticated Devpost form.

## Browser progress

- Opened the Qloo hackathon page and followed Join hackathon.
- Devpost requires sign-in or account creation.
- Left the browser on the Devpost login page, returning to Qloo registration after login.
- No hackathon registration or project submission has been completed.
