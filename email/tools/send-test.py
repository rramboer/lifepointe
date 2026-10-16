#!/usr/bin/env python3
"""send-test.py: email the newsletter template to yourself, exactly as written.

Sends email/index.html through the office@ Google Workspace mailbox, so a test looks the way a
real send will: images, the <style> block (phone layout and resets), tel: links and all. Pasting
the page into Gmail's compose window, or sending it through an app that cleans up HTML, strips
those, and the test shows a different email.

    python3 email/tools/send-test.py you@gmail.com [more@example.com ...]

It asks for office@'s app password (made at myaccount.google.com/apppasswords; see
email/README.md, Sending a test) and keeps it in memory only. To skip the prompt, put it in the
LIFEPOINTE_SMTP_PASSWORD environment variable for that one command. Never save it in a file.

Options:
    --from ADDRESS   send from this Workspace account (default office@lifepointechiro.com)
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
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
DEFAULT_FROM = 'office@lifepointechiro.com'
DEFAULT_FILE = Path(__file__).resolve().parent.parent / 'index.html'
PLAIN_TEXT = ('This is a test of the Lifepointe newsletter template. Open it in an email app that '
              'shows HTML to see the design.\n')


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
    parser.add_argument('--from', dest='sender', default=DEFAULT_FROM)
    parser.add_argument('--file', type=Path, default=DEFAULT_FILE)
    parser.add_argument('--subject', default='Test: Lifepointe newsletter')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    try:
        html = args.file.read_text(encoding='utf-8')
    except OSError as e:
        sys.exit(f'can\'t read {args.file}: {e}')
    msg = build(args.sender, args.to, args.subject, html)

    if args.dry_run:
        sys.stdout.write(msg.as_string())
        return

    password = os.environ.get('LIFEPOINTE_SMTP_PASSWORD') or getpass.getpass(f'App password for {args.sender}: ')
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(args.sender, password.replace(' ', ''))
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        sys.exit(f'Google refused the login for {args.sender}. Use an app password '
                 '(myaccount.google.com/apppasswords, which needs 2-Step Verification on), '
                 'not the account password.')
    except (smtplib.SMTPException, OSError) as e:
        sys.exit(f'sending failed: {e}')
    print(f'Sent "{args.subject}" to {", ".join(args.to)} from {args.sender}.')


if __name__ == '__main__':
    main()
