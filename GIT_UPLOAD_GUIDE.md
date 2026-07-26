# 📤 Git Upload Guide — Step by Step (Tiny Steps Included)

---

## Part 1 — One-Time Setup (செய்யாட்டா முதல்ல செய்யுங்க)

### Step 1.1 — Git installed-ஆ இருக்கான்னு check பண்ணு

```bash
git --version
```

Output வராட்டா, Kali-ல install பண்ணு:

```bash
sudo apt update
sudo apt install git -y
```

### Step 1.2 — Git-க்கு உங்க identity set பண்ணு

GitHub commits-ல உங்க பெயரும் email-உம் தான் காமிக்கும், இதனால இது தேவை.

```bash
git config --global user.name "rithisingh2020"
git config --global user.email "your-email@example.com"
```

> 📌 உங்க actual GitHub account email-ஐ type பண்ணுங்க — இல்லன்னா commits "unverified"-ஆ காமிக்கும்.

### Step 1.3 — GitHub-ல login authentication setup (Personal Access Token)

GitHub இப்போ password login support பண்ணாது push பண்ண — Token தேவை.

1. Browser-ல போங்க: `github.com` → Login → top-right profile photo click
2. **Settings** → கீழ scroll → **Developer settings** (left sidebar, கீழ end-ல)
3. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
4. Note: `portfolio-upload-token` type பண்ணுங்க
5. Expiration: 90 days (அல்லது No expiration)
6. Scopes-ல tick பண்ணுங்க: ✅ `repo` (இது மட்டும் போதும்)
7. **Generate token** click
8. ⚠️ **இந்த token இப்போ ஒரு தடவை தான் காமிக்கும்** — Notepad-ல copy பண்ணி save பண்ணிக்குங்க. Page விட்டா திரும்ப பாக்க முடியாது.

📸 இந்த token-ஐ screenshot எடுக்காதீங்க — யாருகிட்டயும் share பண்ணாதீங்க (இது உங்க password மாதிரி).

---

## Part 2 — ஒவ்வொரு Project Repo Create + Upload பண்றது

இந்த steps-ஐ ஒவ்வொரு 7 projects-க்கும் repeat பண்ணுங்க. Example: Project 01 (Network Troubleshooting)-உடன் காட்டுறேன்.

### Step 2.1 — GitHub.com-ல புதுசா Repository create பண்ணு

1. github.com → top-right **+** icon → **New repository**
2. Repository name: `network-troubleshooting-lab`
3. Description: `L1 network diagnostics across a 3-VM lab — DNS, DHCP, gateway troubleshooting`
4. **Public** select பண்ணுங்க (recruiters பாக்கணும்னா public-ஆ இருக்கணும்)
5. ❌ "Add a README file" — **tick பண்ணாதீங்க** (நம்மள்ளோட README already இருக்கு, conflict ஆகும்)
6. **Create repository** click

### Step 2.2 — Local folder-ஐ Git repo-ஆ initialize பண்ணு

Kali terminal-ல, உங்க project folder இருக்கற இடத்துக்கு போங்க:

```bash
cd /path/to/01-network-troubleshooting
git init
```

### Step 2.3 — Files-ஐ Git-க்கு add பண்ணு

```bash
git add .
git status
```

`git status` run பண்ணும்போது README.md, SCREENSHOT_CHECKLIST.md, மற்றும் screenshots/ folder-ல உள்ள images green color-ல "Changes to be committed" கீழ காமிக்கணும்.

### Step 2.4 — Commit பண்ணு (இது போல ஒரு "save point")

```bash
git commit -m "Add network troubleshooting lab documentation and screenshots"
```

### Step 2.5 — Branch name confirm பண்ணு

```bash
git branch -M main
```

### Step 2.6 — GitHub repo-ஐ local repo-உடன் link பண்ணு

GitHub-ல உங்க repo create பண்ணும்போது கிடைக்கற URL இங்க use பண்ணுங்க:

```bash
git remote add origin https://github.com/rithisingh2020/network-troubleshooting-lab.git
```

### Step 2.7 — Push பண்ணு (GitHub-க்கு upload)

```bash
git push -u origin main
```

இது username கேக்கும் → `rithisingh2020` type பண்ணுங்க
Password கேக்கும் → **Part 1.3-ல generate பண்ண Token-ஐ paste பண்ணுங்க** (real password இல்ல)

### Step 2.8 — Verify பண்ணு

Browser-ல உங்க repo URL refresh பண்ணி பாருங்க — README.md content automatic-ஆ காமிக்கும், screenshots/ folder உள்ள images GitHub-ல render ஆகும்.

```
https://github.com/rithisingh2020/network-troubleshooting-lab
```

---

## Part 3 — மற்ற 6 Projects-க்கும் இதே Steps Repeat பண்ணுங்க

ஒவ்வொரு project-க்கும் repo name மாறும், மற்றபடி exact same steps:

| Project | Suggested Repo Name |
|---|---|
| 01 | `network-troubleshooting-lab` |
| 02 | `windows-os-support-lab` |
| 03 | `linux-administration-lab` |
| 04 | `active-directory-lifecycle-lab` |
| 05 | `dns-dhcp-infrastructure-lab` |
| 06 | `group-policy-management-lab` |
| 07 | `security-incident-response-lab` |

> 💡 **Time-save tip:** Token ஒரு தடவா generate பண்ணினா, அதே token எல்லா repos-க்கும் use ஆகும். Part 1.3 திரும்ப செய்ய வேண்டாம்.

---

## Part 4 — பின்னாடி Update பண்ணணும்னா (e.g. screenshot add பண்ணினப்போ)

Project folder-க்கு உள்ள போய்:

```bash
cd /path/to/01-network-troubleshooting
git add .
git commit -m "Add screenshots for network troubleshooting lab"
git push
```

இப்போ username/token திரும்ப கேக்காது (Git cache பண்ணிடும், ஒரு சில systems-ல).

---

## ⚠️ Common Errors & Fixes

| Error | Fix |
|---|---|
| `fatal: not a git repository` | நீங்க இருக்கற folder தப்பு — `cd` correct path-க்கு போங்க |
| `remote origin already exists` | `git remote remove origin` run பண்ணி Step 2.6 திரும்ப செய்யுங்க |
| `Authentication failed` | Token expired-ஆ இருக்கும் — Part 1.3 repeat பண்ணி புதுசா generate பண்ணுங்க |
| Push ஆகுது ஆனா screenshots காமிகல | Image file size 100MB-க்கு மேல இருக்கா check பண்ணுங்க — அதுக்கு Git LFS தேவை (இது rare) |

---
*Next: see `RESUME_BULLETS.md` and `LINKEDIN_POSTS.md` to put these projects to work.*
