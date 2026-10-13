"""Every page the site generates. Each module has FILENAME and render(site) -> HTML.

PAGES is the one list of indexable pages: each one is built, gets a canonical URL and sharing
tags, and is listed in sitemap.xml in this order. Adding a page here is all the sitemap needs.
not_found (404.html) is built too, but it is noindex and stays out of PAGES and the sitemap.
"""
from . import (about, accessibility, contact, good_faith_estimate, index, new_patients, nondiscrimination,
               not_found, privacy, privacy_notice, recipe_book, services, success_stories)

PAGES = [index, about, services, success_stories, new_patients, recipe_book, contact, privacy, privacy_notice,
         accessibility, nondiscrimination, good_faith_estimate]
