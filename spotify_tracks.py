import sys, json, io

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

item_type = sys.argv[1] if len(sys.argv) > 1 else 'playlist'
item_id = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]

if item_type == 'album':
    from spotapi import PublicAlbum
    obj = PublicAlbum(item_id)
    raw = obj.get_album_info()
    pages = [raw]
else:
    from spotapi import PublicPlaylist
    obj = PublicPlaylist(item_id)
    pages = list(obj.paginate_playlist())


def extract_name(obj):
    name = obj.get('name', '') or ''
    artists = []
    for a in (obj.get('artists') or {}).get('items') or []:
        aname = (a.get('profile') or {}).get('name', '') or ''
        if aname:
            artists.append(aname)
    return (name + ' - ' + ', '.join(artists)) if artists else name


all_tracks = []

for page in pages:
    if item_type == 'album':
        items = (((page.get('data') or {}).get('albumUnion') or {}).get('tracksV2') or {}).get('items') or []
        for entry in items:
            track = entry.get('track') or {}
            if track.get('name'):
                all_tracks.append(extract_name(track))
    else:
        items = page.get('items') or []
        for entry in items:
            data = ((entry.get('itemV2') or {}).get('data') or {})
            if data.get('name'):
                all_tracks.append(extract_name(data))

print(json.dumps(all_tracks, ensure_ascii=False))
