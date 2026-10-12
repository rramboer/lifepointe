"""Good Faith Estimate notice: the No Surprises Act right of uninsured and self-pay patients to
an estimate of their costs before care.

A provider must make information about this right "prominently displayed (and easily
searchable from a public search engine)" on its website, in the office and where people
schedule or ask about costs (45 CFR 149.610(b)(1)(iii)(A)). Every page's footer links here,
and the page is in the sitemap. The notice is the CMS standard notice, "Right to Receive a Good
Faith Estimate of Expected Charges" (Appendix 1, April 2022), word for word: CMS treats using it
as good-faith compliance. Only the last paragraph, how to ask this office for an estimate, is
the practice's own. Patients using Medicare, Medicaid, VA or other federal coverage are
generally outside this rule; self-pay patients, including people who choose not to bill their
insurance, are in it.
"""
from ..helpers import esc
from ..layout import V, page, page_hero

FILENAME = 'good-faith-estimate.html'
LAST_UPDATED = 'October 2026'
CMS_CONSUMERS = 'https://www.cms.gov/nosurprises/consumers'
CMS_EMAIL = 'FederalPPDRQuestions@cms.hhs.gov'
CMS_PHONE = ('+18009853059', '1-800-985-3059')


def render(site):
    p = site.practice
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)

    body = page_hero('Your rights', 'Good Faith Estimate',
                     'If you don&rsquo;t have health insurance, or you&rsquo;re not using it, you can get an '
                     'estimate of the cost of your care before your visit.',
                     f'Last updated {LAST_UPDATED}') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="gfe-h">
  {V}
  <div class="wrap">
    <h2 id="gfe-h" class="display-2">You have the right to receive a &ldquo;Good Faith Estimate&rdquo; explaining how much your health care will cost</h2>
    <div class="measure mt-15">
      <p>Under the law, health care providers need to give patients who don&rsquo;t have certain types of health care coverage or who are not using certain types of health care coverage an estimate of their bill for health care items and services before those items or services are provided.</p>
      <ul class="list-tight">
        <li>You have the right to receive a Good Faith Estimate for the total expected cost of any health care items or services upon request or when scheduling such items or services. This includes related costs like medical tests, prescription drugs, equipment, and hospital fees.</li>
        <li>If you schedule a health care item or service at least 3 business days in advance, make sure your health care provider or facility gives you a Good Faith Estimate in writing within 1 business day after scheduling. If you schedule a health care item or service at least 10 business days in advance, make sure your health care provider or facility gives you a Good Faith Estimate in writing within 3 business days after scheduling. You can also ask any health care provider or facility for a Good Faith Estimate before you schedule an item or service. If you do, make sure the health care provider or facility gives you a Good Faith Estimate in writing within 3 business days after you ask.</li>
        <li>If you receive a bill that is at least $400 more for any provider or facility than your Good Faith Estimate from that provider or facility, you can dispute the bill.</li>
      </ul>
      <p>For questions or more information about your right to a Good Faith Estimate, visit <a href="{esc(CMS_CONSUMERS)}">www.cms.gov/nosurprises/consumers</a>, email <a href="{esc('mailto:' + CMS_EMAIL)}">{esc(CMS_EMAIL)}</a>, or call <a href="{esc('tel:' + CMS_PHONE[0])}">{esc(CMS_PHONE[1])}</a>.</p>

      <h3 class="display-3 mt-2">Ask us for an estimate</h3>
      <p>To ask {esc(p.name)} for a Good Faith Estimate, <a href="{tel}">call us at {phone}</a> or ask at the front desk.</p>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Good Faith Estimate | {p.name}',
                'If you don’t have health insurance or aren’t using it, you have the right to a Good Faith '
                f'Estimate of what your care at {p.name} will cost.',
                body)
