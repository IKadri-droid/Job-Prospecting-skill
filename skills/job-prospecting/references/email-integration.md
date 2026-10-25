# Mailbox setup — Gmail, Outlook and every other provider

Read this file when you reach the mailbox questions of Step 7, or when the person asks how replies and job alerts
can be followed. Explain everything with simple words, one step at a time, and adapt to their equipment.

## Rules that never change

1. **Read-only.** The mailbox is only read (replies from employers, job alerts). Nothing is sent, moved, deleted or
   marked as read automatically. Every application and every reminder is sent by the person, from their own mailbox.
2. **No password in the conversation.** Never ask for a password, an app password, a token or a secret, and tell the
   person to never paste one in the chat. They type it themselves, on their own computer, into the official sign-in
   page or into a hidden prompt (e.g. `getpass`), and it is stored only on their computer (system keychain, or a file
   readable only by them, outside any shared or synced folder).
3. **The smallest permission possible.** Ask for read access to mail only, never "send", "modify" or "full access".
   If a provider only offers broad access, say so plainly and suggest the manual level instead.
4. **Only the person's own data.** Read only the folders they choose (ideally one folder for replies and one for job
   alerts), never the whole mailbox history.
5. **The person can stop at any time.** Always explain how to revoke the access (last section).
6. **Job sites that forbid automatic collection (LinkedIn, etc.) are never read directly.** Use the alert e-mails the
   site sends on its own (see "Job alerts").

## Pick the level with the person

| Level | For whom | What it does |
|---|---|---|
| **A. Manual** | phone only, or no wish to connect anything | They create folders and rules (below). When a reply arrives, they paste it or tell you; you update the tracking. |
| **B. Folders and rules** | everyone, 5 minutes, no technical skill | Replies and job alerts are sorted automatically into two folders, so nothing is lost. Works with every provider. |
| **C. Automatic reading** | computer + Claude Code (or another agent able to run scripts) | A small script reads the two folders in read-only mode, attaches each reply to the right application and imports the job alerts into the daily search. |

If the person uses Claude in an app where a mail connector (for example Gmail or Outlook) is already enabled, you may
read the two folders through that connector instead of level C, still read-only, and never send anything with it.

Always start with level B: level C reads the folders that level B creates.

## Level B — folders and rules (all providers)

Create two folders (called "labels" in Gmail): **Applications** (or "Candidatures") and **Job alerts**.
Then one rule for each folder:
- **Applications**: messages containing words like *application, candidature, interview, entretien, recruitment,
  recrutement* (adapt to the language of the country), or coming from the addresses of companies the person applied to.
- **Job alerts**: messages from the alert senders of the job sites they use (for example LinkedIn job alerts,
  Indeed, the national employment service, trade job boards). Look up the exact sender addresses together.

Where to click (menus change over time; if a label differs, search the provider's help for "create a filter/rule"):
- **Gmail** (web): Settings ⚙ → See all settings → *Filters and Blocked Addresses* → Create a new filter → fill in
  "Has the words" or "From" → Create filter → *Apply the label* (create it) → also apply to matching conversations.
- **Outlook.com / Hotmail / Live / Microsoft 365** (web): Settings ⚙ → Mail → *Rules* → Add new rule → condition
  ("Subject or body includes" / "From") → action *Move to* a folder. In the Outlook desktop app: *Rules → Manage rules*.
- **Yahoo Mail**: Settings → More settings → *Filters* → Add new filters.
- **iCloud Mail** (icloud.com): Settings ⚙ → *Rules* → Add a rule.
- **Proton Mail**: Settings → *Filters* → Add filter.
- **Other providers** (Orange, Free, SFR, La Poste, GMX, Fastmail, a school or company address…): look for "filters",
  "rules" or "sorting" in the webmail settings; most offer it. If not, level A.

### Job alerts
Help the person create e-mail alerts on the job sites that matter in their country and trade (one alert per search:
trade + area + contract type), daily frequency, sent to the address they apply from. The alerts land in the
*Job alerts* folder; the daily search reads them first and then checks each offer on the employer's site or another
job site before keeping it (never by opening sites that forbid automatic access).

## Level C — automatic reading, by provider

The script must: connect read-only, read only the two folders and only recent messages (e.g. the last 3 days for
alerts, 120 days for replies), keep a list of messages already processed, and never write to the mailbox.

### Gmail (personal Google account)
Recommended: the **Gmail API** with the single permission `https://www.googleapis.com/auth/gmail.readonly`.
1. https://console.cloud.google.com/ → create a project.
2. *APIs & Services → Library* → **Gmail API** → Enable.
3. *OAuth consent screen*: type **External**, any app name, the person's address as support and developer contact.
   **Do not upload a logo** (it triggers Google's verification once the app leaves "Testing"). Add no scope there.
   In *Audience / Test users*, add the person's own Gmail address.
4. *Credentials → Create credentials → OAuth client ID* → type **Desktop app** → Download the JSON file.
   (If the wizard asks "User data or Application data", choose **User data**.)
5. The script opens the browser once; Google warns that the app is not verified (it is the person's own app):
   *Advanced → Go to …*, then accept **only "Read your e-mails"**. The script keeps the refresh token locally (file
   readable only by the person) and refuses any token with a broader permission.
6. While the app stays in "Testing", Google may expire the authorization after 7 days: simply authorize again.
Avoid IMAP for Gmail: it needs an app password and gives full access to the mailbox.

### Outlook.com, Hotmail, Live (personal Microsoft account)
Recommended: **Microsoft Graph** with the delegated permissions `Mail.Read` (read-only) and `offline_access`.
1. https://entra.microsoft.com (or portal.azure.com) → *App registrations* → **New registration**.
   Supported account types: include **personal Microsoft accounts**.
2. *Authentication* → add a platform **Mobile and desktop applications** (redirect `http://localhost`), and enable
   **Allow public client flows** (needed for the "device code" sign-in, which uses no secret).
3. *API permissions* → Microsoft Graph → Delegated → **Mail.Read** (and `offline_access`). Nothing else.
4. The script shows a short code and the address microsoft.com/devicelogin; the person signs in and accepts reading
   their mail. The script then reads the two folders (`/me/mailFolders/{id}/messages`).
Basic password sign-in (IMAP with the normal password) no longer works for Outlook.com: use this method.

### Microsoft 365 work or school address
The organization often blocks apps that the administrator has not approved. Ask the IT department, or stay at
level B (rules) and level A (paste the replies). Never try to bypass the organization's rules.

### Yahoo, AOL, iCloud, Proton, Orange, Free, SFR, La Poste, GMX, Fastmail and others: IMAP, read-only
1. In the provider's security settings, the person creates an **app-specific password** (two-step verification is
   usually required first). Examples: Yahoo → Account security → *Generate app password*; iCloud →
   account.apple.com → *Sign-In and Security → App-Specific Passwords*. Some French providers use the normal password
   for IMAP; check their help page.
2. IMAP server (port 993, SSL), to check on the provider's help page because settings change: Yahoo
   `imap.mail.yahoo.com`, iCloud `imap.mail.me.com`, Orange `imap.orange.fr`, Free `imap.free.fr`, SFR `imap.sfr.fr`,
   La Poste `imap.laposte.net`, GMX `imap.gmx.net` (enable IMAP in the settings first), Fastmail `imap.fastmail.com`.
   **Proton Mail** only allows IMAP through **Proton Mail Bridge** (paid plans), which runs locally (`127.0.0.1`).
3. The script asks for the app password with a hidden prompt, stores it in the system keychain (or a file readable
   only by the person), opens each folder with **EXAMINE / `select(readonly=True)`** and fetches with **`BODY.PEEK`**
   so nothing is marked as read.
An app password gives full access to the mailbox even if the script only reads: say it clearly, keep it only on the
person's computer, and delete it as soon as it is no longer needed.

## Attaching a reply to the right application

- Match by, in order: the sender's domain (only if it matches a contact published in the offer or the company site,
  never a generic one like gmail.com or a job site), the company name in the message, then the job title when the
  person applied twice to the same company.
- **If in doubt, attach nothing**: put the message in a "to check" list and tell the person.
- Any reply, even an automatic acknowledgment, stops the reminders for that application.
- The status becomes "reply received — to classify"; the **person** decides: interview, rejection, offer.

## Sending and reminders

- The person always sends from their own mailbox (or the site's form, or in person).
- For a reminder, show the draft text to copy. Creating drafts directly in the mailbox needs a write permission
  (e.g. Gmail `gmail.compose`, Graph `Mail.ReadWrite`): only if the person explicitly asks, as a separate
  permission, and never with sending enabled.

## Test before relying on it

From another address or a phone, the person sends themselves a fake reply that names one company from their
tracking table (for example "Company X has received your application [TEST]"). Check that it lands in the
*Applications* folder, that it is attached to the right row, and that nothing changed in the mailbox.

## Revoking the access

- Google: myaccount.google.com/permissions → the app → Remove access; delete the local token file.
- Microsoft (personal): account.live.com/consent/Manage → the app → Remove; delete the local token.
- App passwords (Yahoo, iCloud…): delete them in the provider's security settings.
