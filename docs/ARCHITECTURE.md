# SupportIQ architecture

```text
React / Vite UI --Bearer JWT--> FastAPI
                                  ├── bcrypt + JWT authentication
                                  ├── SQLAlchemy -> SQLite locally / PostgreSQL when configured
                                  ├── Knowledge upload -> text extraction -> chunking
                                  │                         └── Sentence Transformers -> persistent ChromaDB
                                  ├── CSV ticket import -> SQL ticket records
                                  ├── RAG draft -> user-scoped retrieval -> LLM -> editable draft + source names
                                  └── Analytics -> ticket aggregates

AI output is always a draft. A human reviews and approves; no automatic email sending.
```

Every ticket and knowledge document is assigned to the authenticated user's ID. Vector records include `owner_id`; retrieval filters by the current user's ID and validates returned metadata.

## Draft flow
1. Agent opens a ticket and requests a draft.
2. The backend embeds the subject, issue, and optional agent context.
3. ChromaDB returns relevant passages from that user's uploaded documents.
4. The LLM receives the ticket and retrieved excerpts with instructions not to invent unsupported policy.
5. The draft and source filenames are saved to the ticket.
6. The agent edits and approves the draft. Approval does not send a message.

## Current limitations
Scanned PDFs need OCR. There is no direct Zendesk/Freshdesk integration, outbound email transport, fine-tuning, or automated evaluation harness. Add a labelled test set before claiming model accuracy. Use PostgreSQL, HTTPS, migrations, secret management, monitoring, and rate limits for production.
