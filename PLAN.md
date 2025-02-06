Fast As Possible - Christmas Break Development

Links!
https://railway.com/features

Purpose -> Individualistic QR code scanner platform for people to see good!

Frontend -> use a random site builder for fastest end game home landing page or do we want a more nuance site builder since we need the platform

people print qr code on box. then they link their qr code to their "inbox link" -> email

on creation of qr code link you need to place a "indox id/link" within 30 mins. Good way making sure people dont forget

-> on receiving side, you can just take a picture / of goods
Optional
  Different BINS
    -> friends -> christmas gifts
    -> work
      -> chef: will have stickers uber eats or whatever...
    -> random person
      -> see it face

Caddy - https://caddyserver.com/docs/quick-starts/static-files - read about later.

I really like this structure, on our big refactor we should do this

src/
├── ui/
│   ├── components/   # UI components (React/Vue/Flutter widgets, etc.)
│   ├── views/        # Screens/pages in the app
│   └── controllers/  # Handles user interactions, calls Business Logic Layer
├── logic/
│   ├── services/     # Implements business logic
│   └── models/       # Data models (DTOs, validation schemas)
├── data/
│   ├── firebase/     # Firebase facade with modular services
│   │   ├── auth.ts   # Authentication operations
│   │   ├── db.ts     # Firestore operations
│   │   ├── storage.ts # Storage operations
│   └── repositories/ # Optional: Abstract repositories for data access
└── utils/            # Shared utilities (e.g., formatters, constants)



