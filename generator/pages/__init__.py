"""Every page the site generates. Each module has FILENAME and render(site) -> HTML."""
from . import about, contact, index, new_patients, recipe_book, services, success_stories

PAGES = [index, about, services, success_stories, new_patients, recipe_book, contact]
