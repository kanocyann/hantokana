from .dict_view_core import entry_matches_filters, split_search_keywords


def filter_entries(entries, current_type="全部", search_text=""):
    search_keywords = split_search_keywords(search_text)
    return [
        entry for entry in entries
        if entry_matches_filters(entry, current_type, search_keywords)
    ]


def calculate_total_pages(total_entries, entries_per_page):
    try:
        page_size = int(entries_per_page)
    except (TypeError, ValueError):
        page_size = 1
    page_size = max(1, page_size)
    return max(1, (total_entries + page_size - 1) // page_size)


def page_bounds(current_page, entries_per_page, total_entries):
    try:
        page = int(current_page)
    except (TypeError, ValueError):
        page = 1
    try:
        page_size = int(entries_per_page)
    except (TypeError, ValueError):
        page_size = 1

    page = max(1, page)
    page_size = max(1, page_size)
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_entries)
    return start_idx, end_idx


def get_page_entries(entries, current_page, entries_per_page):
    start_idx, end_idx = page_bounds(current_page, entries_per_page, len(entries))
    return start_idx, entries[start_idx:end_idx]


def entry_at_page_row(entries, current_page, entries_per_page, row):
    start_idx, page_entries = get_page_entries(entries, current_page, entries_per_page)
    if row < 0 or row >= len(page_entries):
        return None
    return entries[start_idx + row]
