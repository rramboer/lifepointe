#!/usr/bin/env python3
"""send-test.py: email the newsletter template to yourself, exactly as written.

Sends email/index.html through the office@ Google Workspace mailbox, so a test looks the way a
real send will: images, the <style> block (phone layout and resets), tel: links and all. Pasting
the page into Gmail's compose window, or sending it through an app that cleans up HTML, strips
those, and the test shows a different email.

    python3 email/tools/send-test.py you@gmail.com [more@example.com ...]

It asks for the sending account's app password (made at myaccount.google.com/apppasswords;
see email/README.md, Sending a test) and keeps it in memory only. To skip the prompt, put
LIFEPOINTE_SMTP_PASSWORD (and LIFEPOINTE_SMTP_FROM, the address it logs in as) in the repo's
.env file, which git ignores (.env.example shows the format), or in the environment for one
command; the environment wins. The script won't read a .env that git tracks.

Options:
    --from ADDRESS   send from this Google account (default: LIFEPOINTE_SMTP_FROM, or
                     office@lifepointechiro.com)
    --file PATH      the HTML to send (default: email/index.html next to this script)
    --subject TEXT   the subject line (default "Test: Lifepointe newsletter")
    --dry-run        print the message instead of sending it

Python standard library only. The {{UnsubscribeURL}} and {{PreferencesURL}} placeholders go out
as they are; a newsletter service replaces them on a real send.
"""
import argparse
import getpass
import os
import smtplib
import subprocess
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
DEFAULT_FROM = 'office@lifepointechiro.com'
DEFAULT_FILE = Path(__file__).resolve().parent.parent / 'index.html'
ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / '.env'
PLAIN_TEXT = ('This is a test of the Lifepointe newsletter template. Open it in an email app that '
              'shows HTML to see the design.\n')


def read_env_file():
    """KEY=VALUE lines from the repo's .env (git ignores it). Refuses a .env that git tracks:
    the repository is public, and the file holds a password."""
    if not ENV_FILE.is_file():
        return {}
    try:
        tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '.env'], cwd=ROOT,
                                 capture_output=True).returncode == 0
    except OSError:
        tracked = False
    if tracked:
        sys.exit('.env is in the git repository, which is public. Run "git rm --cached .env", '
                 'change the app password, and try again.')
    if ENV_FILE.stat().st_mode & 0o077:
        print('warning: other users on this computer can read .env; run "chmod 600 .env"', file=sys.stderr)
    values = {}
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key = key.strip().removeprefix('export ').strip()
        values[key] = value.strip().strip('"').strip("'")
    return values


def build(sender, recipients, subject, html):
    msg = EmailMessage()
    msg['From'] = f'Lifepointe Chiropractic & Wellness Center <{sender}>'
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain=sender.split('@')[1])
    msg.set_content(PLAIN_TEXT)
    msg.add_alternative(html, subtype='html')
    return msg


def main():
    parser = argparse.ArgumentParser(description='Email the newsletter template to yourself.')
    parser.add_argument('to', nargs='+', help='who gets the test')
    parser.add_argument('--from', dest='sender')
    parser.add_argument('--file', type=Path, default=DEFAULT_FILE)
    parser.add_argument('--subject', default='Test: Lifepointe newsletter')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    settings = read_env_file()
    settings.update(os.environ)
    sender = args.sender or settings.get('LIFEPOINTE_SMTP_FROM') or DEFAULT_FROM
    try:
        html = args.file.read_text(encoding='utf-8')
    except OSError as e:
        sys.exit(f'can\'t read {args.file}: {e}')
    msg = build(sender, args.to, args.subject, html)

    if args.dry_run:
        sys.stdout.write(msg.as_string())
        return

    password = settings.get('LIFEPOINTE_SMTP_PASSWORD') or getpass.getpass(f'App password for {sender}: ')
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(sender, password.replace(' ', ''))
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        sys.exit(f'Google refused the login for {sender}. Use an app password '
                 '(myaccount.google.com/apppasswords, which needs 2-Step Verification on), '
                 'not the account password.')
    except (smtplib.SMTPException, OSError) as e:
        sys.exit(f'sending failed: {e}')
    print(f'Sent "{args.subject}" to {", ".join(args.to)} from {sender}.')


if __name__ == '__main__':
    main()
