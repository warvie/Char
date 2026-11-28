# Setting up email sign-in for usernames

Outside Claude (on GitHub Pages or through the desktop launcher), claiming a username needs a signed-in, email-verified account. Dead Ground uses Firebase Authentication with email links for this: the player types their email, gets a one-time link, and opening it signs them in. Names are stored in Firestore, and the rules below let a name be claimed only by a verified account, and only if it's free or already theirs.

Until the config in step 4 is pasted into the game, the email box is disabled and names can't be claimed outside Claude. Inside Claude, names keep using your Claude account as before.

## 1. Create the project

1. Go to <https://console.firebase.google.com> and click **Add project** (or **Create a project**).
2. Name it (for example `dead-ground`). Google Analytics isn't needed, so you can turn it off.

## 2. Turn on email-link sign-in

1. In the project, open **Build → Authentication** and click **Get started**.
2. On the **Sign-in method** tab, choose **Email/Password**.
3. Turn on **Email/Password**, then also turn on **Email link (passwordless sign-in)**, and click **Save**.
4. On the **Settings** tab, open **Authorized domains** and make sure these are listed (add any that are missing):
   - `warvie.github.io`
   - `localhost`

## 3. Create the database and paste the rules

1. Open **Build → Firestore Database** and click **Create database**.
2. Pick a location near you, and start in **production mode**.
3. On the **Rules** tab, replace everything with the rules below and click **Publish**.

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // usernames: the document id is the name in lower case
    match /names/{name} {
      allow read: if true;
      // claim a free name: signed in with a verified email, valid name, stored under your own account
      allow create: if request.auth != null
        && request.auth.token.email_verified == true
        && name.matches('^[a-z0-9_]{3,16}$')
        && request.resource.data.u == request.auth.uid
        && request.resource.data.n.lower() == name;
      // re-save a name you already own
      allow update: if request.auth != null
        && request.auth.token.email_verified == true
        && resource.data.u == request.auth.uid
        && request.resource.data.u == request.auth.uid
        && request.resource.data.n.lower() == name;
      // give a name up (when switching to a new one)
      allow delete: if request.auth != null && resource.data.u == request.auth.uid;
    }

    // each player's profile: their current name and picture
    match /profiles/{uid} {
      allow read: if true;
      allow write: if request.auth != null
        && request.auth.token.email_verified == true
        && request.auth.uid == uid;
    }
  }
}
```

## 4. Register the web app and copy its config

1. Open **Project settings** (the gear next to *Project Overview*).
2. Under **Your apps**, click the **Web** icon (`</>`), give it a nickname (for example `Dead Ground`), and click **Register app**. Firebase Hosting isn't needed.
3. Firebase shows a `firebaseConfig` object like this:

```js
const firebaseConfig = {
  apiKey: "…",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "…",
  appId: "…"
};
```

4. Send that object to Claude (or paste it yourself in `index.html`, replacing `const FB_CFG=null;` with `const FB_CFG={ …the same fields… };`).

This config is safe to publish: it only identifies the project. The rules in step 3 are what protect the data.

## Notes

- Firebase's free plan covers this comfortably (sign-in links and small Firestore reads/writes).
- Sign-in links have to be opened on the same device and browser the email was typed into. If it's a different one, the game asks for the email address again.
- Names claimed here and names claimed inside Claude are separate lists, because Claude doesn't let games load outside sign-in services.
