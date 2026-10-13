"""Notice of Privacy Practices: the practice's HIPAA notice (45 CFR 164.520).

A covered entity that has a website must post its notice prominently on it and make it
available electronically (164.520(c)(3)(i)). Every page's footer links here, and the privacy
policy points here too.

The text is the practice's own notice, "Notice of Privacy Practices" (Word and PDF, in the
office's documents folder), which is HHS's model notice for health care providers, revised
February 2026, with the practice's details filled in. Keep this page word for word in step with
that document, apart from these web adaptations:
- the contact details come from data/practice.json, so the email shown is always one that
  works (the document gives office@lifepointechiro.com, live once that mailbox is set up);
- "the information on page 1" reads "the information at the top of this notice";
- the contact box's label has the serial comma the site uses, "Questions, requests, or complaints";
- the notice of free language help ends the page, as 45 CFR 92.11(c)(5)(ii) requires
  (nondiscrimination.language_help).
When the office changes its notice, update this page and EFFECTIVE.
"""
from ..helpers import esc
from ..layout import V, page, page_hero
from .nondiscrimination import language_help

FILENAME = 'notice-of-privacy-practices.html'
EFFECTIVE = 'November 1, 2026'
HHS_COMPLAINTS = 'https://www.hhs.gov/hipaa/filing-a-complaint/index.html'
HHS_NOTICE_INFO = 'https://www.hhs.gov/ocr/privacy/hipaa/understanding/consumers/noticepp.html'


def _list(items):
    return '<ul class="list-tight">' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>'


def _item(heading, *paragraphs, level=4):
    """One right or use: a small heading and its paragraphs (trusted HTML). level is the heading's
    rank: 4 under an h3, 3 straight under a section's h2 (_right)."""
    return (f'<h{level} class="display-4">{heading}</h{level}>'
            + ''.join(f'<p>{para}</p>' for para in paragraphs))


def _right(heading, *paragraphs):
    """An item straight under the "Your Rights" h2."""
    return _item(heading, *paragraphs, level=3)


def render(site):
    p = site.practice
    name = esc(p.name)
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    email = esc(p.email)
    email_link = esc('mailto:' + p.email)
    address = esc(p.address)
    part2_short = ('To the extent that we have your substance use disorder patient records, subject to 42 CFR part 2, '
                   'we will not share that information for investigations or legal proceedings against you without '
                   '(1) your written consent or (2) a court order and a subpoena.')

    body = page_hero('Your privacy', 'Notice of Privacy Practices',
                     'This notice describes how medical information about you may be used and disclosed and how you '
                     'can get access to this information. Please review it carefully.',
                     f'Effective {EFFECTIVE}') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="summary-h">
  {V}
  <div class="wrap">
    <h2 id="summary-h" class="display-2">Your Information. Your Rights. Our Responsibilities.</h2>
    <div class="measure mt-15">
      <div class="card">
        <h3 class="display-3">Questions, requests, or complaints</h3>
        <p>Privacy Officer &nbsp;&middot;&nbsp; {name}<br><a href="{tel}">{phone}</a> &nbsp;&middot;&nbsp; <a href="{email_link}">{email}</a><br>{address}</p>
      </div>

      <h3 class="display-3 mt-2">Your Rights</h3>
      <p>You have the right to:</p>
      {_list([
          'Get a copy of your paper or electronic medical record',
          'Correct your paper or electronic medical record',
          'Request confidential communication',
          'Ask us to limit the information we share',
          'Get a list of those with whom we&rsquo;ve shared your information',
          'Get a copy of this privacy notice',
          'Choose someone to act for you',
          'File a complaint if you believe your privacy rights have been violated',
      ])}

      <h3 class="display-3 mt-2">Your Choices</h3>
      <p>You have some choices in the way that we use and share information as we:</p>
      {_list([
          'Tell family and friends about your condition',
          'Provide disaster relief',
          'Include you in a hospital directory',
          'Provide mental health care',
          'Market our services and sell your information',
          'Raise funds',
      ])}

      <h3 class="display-3 mt-2">Our Uses and Disclosures</h3>
      <p>We may use and share your information as we:</p>
      {_list([
          'Treat you',
          'Run our organization',
          'Bill for your services',
          'Help with public health and safety issues',
          'Do research',
          'Comply with the law',
          'Respond to organ and tissue donation requests',
          'Work with a medical examiner or funeral director',
          'Address workers&rsquo; compensation, law enforcement, and other government requests',
          'Respond to lawsuits and legal actions',
      ])}
      <p>{part2_short}</p>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="rights-h">
  {V}
  <div class="wrap">
    <h2 id="rights-h" class="display-2">Your Rights</h2>
    <div class="measure mt-15">
      <p><strong>When it comes to your health information, you have certain rights.</strong> This section explains your rights and some of our responsibilities to help you.</p>
      {_right('Get an electronic or paper copy of your medical record',
             'You can ask to see or get an electronic or paper copy of your medical record and other health information we have about you. Ask us how to do this.',
             'We will provide a copy or a summary of your health information, usually within 30 days of your request. We may charge a reasonable, cost-based fee.')}
      {_right('Ask us to correct your medical record',
             'You can ask us to correct health information about you that you think is incorrect or incomplete. Ask us how to do this.',
             'We may say &ldquo;no&rdquo; to your request, but we&rsquo;ll tell you why in writing within 60 days.')}
      {_right('Request confidential communications',
             'You can ask us to contact you in a specific way (for example, home, office, or cell phone) or to send mail to a different address.',
             'We will say &ldquo;yes&rdquo; to all reasonable requests.')}
      {_right('Ask us to limit what we use or share',
             'You can ask us not to use or share certain health information for treatment, payment, or our operations. We are not required to agree to your request, and we may say &ldquo;no,&rdquo; for example, if it could affect your care. If we agree to your request, we may still share this information in the event that you need emergency treatment.',
             'If you pay for a service or health care item out-of-pocket in full, you can ask us not to share that information for the purpose of payment or our operations with your health insurer. We will say &ldquo;yes&rdquo; unless a law requires us to share that information.')}
      {_right('Get a list of those with whom we&rsquo;ve shared information',
             'You can ask for a list (accounting) of the times we&rsquo;ve shared your health information for six years prior to the date you ask, who we shared it with, and why.',
             'We will include all the disclosures except for those about treatment, payment, and health care operations, and certain other disclosures (such as any you asked us to make). We&rsquo;ll provide one accounting a year for free but will charge a reasonable, cost-based fee if you ask for another one within 12 months.')}
      {_right('Get a copy of this privacy notice',
             'You can ask for a paper copy of this notice at any time, even if you have agreed to receive the notice electronically. We will provide you with a paper copy promptly.')}
      {_right('Choose someone to act for you',
             'If someone has authority to act as your personal representative, such as if someone has your medical power of attorney or if someone is your legal guardian, that person can exercise your rights and make choices about your health information.',
             'We will make sure the person has this authority and can act for you before we take any action.')}
      {_right('File a complaint if you feel your rights are violated',
             'You can complain if you feel we have violated your rights by contacting us using the information at the top of this notice.',
             f'You can file a complaint with the U.S. Department of Health and Human Services Office for Civil Rights by sending a letter to 200 Independence Avenue, S.W., Washington, D.C. 20201, calling <span class="nowrap">1-877-696-6775</span>, or visiting <a class="url" href="{esc(HHS_COMPLAINTS)}">{esc(HHS_COMPLAINTS)}</a>.',
             'We will not retaliate against you for filing a complaint.')}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="choices-h">
  {V}
  <div class="wrap">
    <h2 id="choices-h" class="display-2">Your Choices</h2>
    <div class="measure mt-15">
      <p><strong>For certain health information, you can tell us your choices about what we share.</strong> If you have a clear preference for how we share your information in the situations described below, talk to us. Tell us what you want us to do, and we will follow your instructions.</p>
      <p><strong>In these cases, you have both the right and choice to tell us to:</strong></p>
      {_list([
          'Share information with your family, close friends, or others involved in your care or payment for your care',
          'Share information in a disaster relief situation',
          'Include your information in a hospital directory',
      ])}
      <p>If you are not able to tell us your preference, for example if you are unconscious, we may go ahead and share your information if we believe it is in your best interest. We may also share your information when needed to lessen a serious and imminent threat to health or safety.</p>
      <p><strong>In these cases we never share your information unless you give us written permission:</strong></p>
      {_list([
          'Marketing purposes',
          'Sale of your information',
          'Most sharing of psychotherapy notes',
      ])}
      <p><strong>In the case of fundraising:</strong></p>
      {_list([
          'We do not contact you for fundraising.',
          'If we have your substance use disorder patient records, subject to 42 CFR part 2, we will give you clear and obvious notice in advance and a choice about whether to receive fundraising communications that use your Part 2 information.',
      ])}
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="uses-h">
  {V}
  <div class="wrap">
    <h2 id="uses-h" class="display-2">Our Uses and Disclosures</h2>
    <div class="measure mt-15">
      <h3 class="display-3">How do we typically use or share your health information?</h3>
      <p>We typically use or share your health information in the following ways.</p>
      {_item('Treat you',
             'We can use your health information and share it with other professionals who are treating you.',
             'Example: A doctor treating you for an injury asks another doctor about your overall health condition.')}
      {_item('Run our organization',
             'We can use and share your health information to run our practice, improve your care, and contact you when necessary.',
             'Example: We use health information about you to manage your treatment and services.')}
      {_item('Bill for your services',
             'We can use and share your health information to bill and get payment from health plans or other entities.',
             'Example: We give information about you to your health insurance plan so it will pay for your services.')}

      <h3 class="display-3 mt-2">How else can we use or share your health information?</h3>
      <p>We are allowed or required to share your information in other ways &ndash; usually in ways that contribute to the public good, such as public health and research. We have to meet many conditions in the law before we can share your information for these purposes.</p>
      <p><strong>In all cases, including those listed below, if we have substance use disorder patient records about you, subject to 42 CFR part 2, we cannot use or share information in those records in civil, criminal, administrative, or legislative investigations or proceedings against you without (1) your consent or (2) a court order and a subpoena.</strong></p>
      <h4 class="display-4">Help with public health and safety issues</h4>
      <p>We can share health information about you for certain situations such as:</p>
      {_list([
          'Preventing disease',
          'Helping with product recalls',
          'Reporting adverse reactions to medications',
          'Reporting suspected abuse, neglect, or domestic violence',
          'Preventing or reducing a serious threat to anyone&rsquo;s health or safety',
      ])}
      {_item('Do research', 'We can use or share your information for health research.')}
      {_item('Comply with the law',
             'We will share information about you if state or federal laws require it, including with the Department of Health and Human Services if it wants to see that we&rsquo;re complying with federal privacy law.')}
      {_item('Respond to organ and tissue donation requests',
             'We can share health information about you with organ procurement organizations.')}
      {_item('Work with a medical examiner or funeral director',
             'We can share health information with a coroner, medical examiner, or funeral director when an individual dies.')}
      <h4 class="display-4">Address workers&rsquo; compensation, law enforcement, and other government requests</h4>
      <p>We can use or share health information about you:</p>
      {_list([
          'For workers&rsquo; compensation claims',
          'For law enforcement purposes or with a law enforcement official',
          'With health oversight agencies for activities authorized by law',
          'For special government functions such as military, national security, and presidential protective services',
      ])}
      {_item('Respond to lawsuits and legal actions',
             'We can share health information about you in response to a court or administrative order, or in response to a subpoena.')}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="responsibilities-h">
  {V}
  <div class="wrap">
    <h2 id="responsibilities-h" class="display-2">Our Responsibilities</h2>
    <div class="measure mt-15">
      {_list([
          'We are required by law to maintain the privacy and security of your protected health information.',
          'We will let you know promptly if a breach occurs that may have compromised the privacy or security of your information.',
          'We must follow the duties and privacy practices described in this notice and give you a copy of it.',
          'We will not use or share your information other than as described in this notice unless you tell us we can in writing. If you tell us we can, you may change your mind at any time. Let us know in writing if you change your mind.',
      ])}
      <p>For more information see: <a class="url" href="{esc(HHS_NOTICE_INFO)}">www.hhs.gov/ocr/privacy/hipaa/understanding/consumers/noticepp.html</a>.</p>

      <h3 class="display-3 mt-2">Changes to the Terms of this Notice</h3>
      <p>We can change the terms of this notice, and the changes will apply to all information we have about you. The new notice will be available upon request, in our office, and on our web site.</p>
      <p><strong>We never market or sell personal information.</strong></p>
      <p>Questions about this notice or your privacy? Contact our Privacy Officer at <a href="{tel}">{phone}</a> or <a href="{email_link}">{email}</a>, or write to us at {address}.</p>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="language-help-h">
  {V}
  <div class="wrap">
    <h2 id="language-help-h" class="display-2">Free language help and other formats</h2>
    <div class="measure mt-15">
      {language_help(site)}
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Notice of Privacy Practices | {p.name}',
                f'How {p.name} may use and share your medical information, your rights, and how to get access '
                f'to your information. Effective {EFFECTIVE}.',
                body)
