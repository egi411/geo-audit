"""Small inline icons for topics and actions in the page layouts."""

PATHS = {
    'chat': '<path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5H5l1.2-3.4A7.5 7.5 0 1 1 20 11.5Z"/><path d="M9 10h7m-7 3h5"/>',
    'quote': '<path d="M10 6H6a2 2 0 0 0-2 2v4h5c0 2-1 4-3 6m14-12h-4a2 2 0 0 0-2 2v4h5c0 2-1 4-3 6"/>',
    'link': '<path d="m10 13 4-4m-5 7-2 2a3 3 0 0 1-4-4l4-4a3 3 0 0 1 4 0m2-2 2-2a3 3 0 0 1 4 4l-4 4a3 3 0 0 1-4 0"/>',
    'search': '<circle cx="10" cy="10" r="5.5"/><path d="m14 14 5 5"/>',
    'compare': '<rect x="3" y="5" width="8" height="14" rx="1.5"/><rect x="13" y="5" width="8" height="14" rx="1.5"/><path d="M6 9h2m8 0h2m-2 4h2"/>',
    'refresh': '<path d="M19 9a7 7 0 1 0 .2 5m.8-10v6h-6"/>',
    'target': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
    'document': '<path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6m-6 4h6"/>',
    'map': '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Zm6-3v15m6-12v15"/>',
    'checklist': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="m7 8 1 1 2-2m-3 7 1 1 2-2m3-5h4m-4 6h4"/>',
    'cursor': '<path d="m5 4 14 9-6 1-3 6L5 4Z"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
}


def topic_icon(name):
    return (f'<svg class="topic-icon" width="24" height="24" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{PATHS[name]}</svg>')
