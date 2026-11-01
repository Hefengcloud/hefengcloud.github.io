"""Keep the PEP curriculum and its workbook separate from the extension course."""
def track_for(item):
    paths = item['sources']
    if item.get('series') in ('PEP', '英语作业本') or any('/PEP/' in p or '英语作业本' in p for p in paths):
        return 'pep'
    if item['title'] == 'Mid 2':
        return 'mixed'
    return 'main'
