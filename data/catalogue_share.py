"""Share of self-hosted font requests whose family is in the Google Fonts catalogue (2026-07-01).

Usage: python3 -I data/catalogue_share.py data/google-fonts-catalogue-2026-10-12.txt data/family_by_service_totals_selfhosted_google_2026.csv
Inputs: the catalogue snapshot (fonts.google.com/metadata/fonts, 2026-10-12) and an export of
fonts_2026.performance__fonts_family_by_service_totals (top 100 families per service and client).
Families outside each service's top 100 are not classified, so the catalogue share is a lower bound.
"""
import csv
import re
import sys


def family_inner(n):  # mirrors FAMILY_INNER in sql/common.sql
    n = re.sub(r'(?i)([\s-]?(black|bold|book|cond(ensed)?|demi|ex(tra)?|heavy|italic|light|medium|narrow|regular|semi|thin|ultra|wide|\d00|\d+pt))+$', '', n)
    if re.search(r'(?i)font\s?awesome', n):
        return 'Font Awesome'
    n = n.strip()
    return n if len(n) >= 3 else None


cat = {family_inner(l.strip()).lower() for l in open(sys.argv[1], encoding='utf-8') if family_inner(l.strip())}
rows = list(csv.DictReader(open(sys.argv[2], encoding='utf-8')))
for cl in ('desktop', 'mobile'):
    rr = [r for r in rows if r['client'] == cl and r['service'] == 'self-hosted' and r['family']]
    total = int(rr[0]['service_requests_family'])
    listed = sum(int(r['count']) for r in rr)
    c = sum(int(r['count']) for r in rr if r['family'].lower() in cat)
    fa = sum(int(r['count']) for r in rr if r['family'] == 'Font Awesome')
    print(f"{cl}: self-hosted requests with a family {total:,}; top-100 families cover {listed/total:.1%}; "
          f"catalogue families {c/total:.1%} (lower bound); Font Awesome {fa/total:.1%}; "
          f"catalogue excluding Font Awesome {c/(total-fa):.1%}")
    print('  not in current catalogue but formerly Google:', [r['family'] for r in rr if r['family'] in ('Source Sans Pro', 'Muli', 'Material Icons')])
