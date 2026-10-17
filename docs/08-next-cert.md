# 8. Reuse It for Your Next Cert

Nothing in this system is specific to networking except the content. The loop works for any exam with published objectives.

## What to change

| Piece | Change |
|---|---|
| Target | New exam code, domains, weights, passing score |
| Prompts | Replace "CompTIA Network+ N10-009" with your exam. Paste in the new objectives. |
| Lexicon | Add the new exam's acronyms (e.g. `systemctl`, `SELinux` for Linux+; `SAML`, `XDR` for Security+) |
| Card mix | More command cards for Linux+. More scenario cards for Security+. |
| Audio | Great for acronyms, frameworks, and concepts. Weak for commands and syntax. |

## Suggested order after Network+

A common CompTIA path:

1. **Network+** → how traffic moves.
2. **Security+** → how to protect it. Heavy overlap with Network+ Domain 4.
3. **Linux+** or **CySA+** → depending on whether you want systems or security operations.

Cloud (AWS Cloud Practitioner / Solutions Architect Associate, Azure AZ-900 / AZ-104) and Cisco CCNA all fit the same loop.

## What carries over

- Your Anki habit and settings.
- Your miss-type codes. After two certs, you'll know your personal pattern.
- The tools. `make_deck.py` and `make_audio.py` don't care what the content is.
- Overlap cards. Tag ports, protocols, and security basics `shared` so you can pull them into the next deck.

## Contribute a kit

If you adapt this for another exam, fork it and send a link. A `linuxplus-ai-study-kit` or `secplus-ai-study-kit` built on this structure is welcome.
