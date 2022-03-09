import os
import re

def extract_names(title, anime_name, anime_alt_names=[]):
    
    release_group = re.findall(r'^\[([^\]]*)\]', title)[0]

    if title.endswith('.torrent'):
        title = os.path.splitext(title)[0]

    original_episode_name = str(title)
    episode_name = str(title)

    while any(episode_name.endswith(ext) for ext in ['.mp4', '.mkv']):
        episode_name = os.path.splitext(episode_name)[0]

    episode_name = re.findall(r'([^\[^\]]+)(?![^\[]*\])', episode_name)

    if not episode_name:
        return (None,)*4

    def get_resolution(episode_name):
        rexp1 = [r'\[\D*(\d+)?[p|i]\D*\]', r'\[.*\d+x(\d+)?\.*\]']
        for rexp in rexp1:
            episode_resolution = re.findall(rexp, title)
            if any(episode_resolution):
                for er in episode_resolution:
                    if er: episode_resolution = er
                break

        if not episode_resolution:
            rexp2 = [
                (r'\(\D*(\d+)?p\D*\)', r'\([^\(]*\d+?p[^\)]*\)'),
                (r'\([^\(]*\d+x(\d+)?[^\)]*\)', r'\([^\(]*\d+x\d+?[^\)]*\)')
            ]
            for rexp in rexp2:
                rexp, rexpr = rexp
                if not rexpr: rexpr = rexp
                episode_resolution = re.findall(rexp, title)
                if any(episode_resolution) and re.findall(rexpr, episode_name[0]):
                    episode_name = [re.sub(rexpr, '', episode_name[0])]
                    for er in episode_resolution:
                        if er: episode_resolution = er
                    break

        return episode_name, episode_resolution

    episode_name, episode_resolution = get_resolution(episode_name)
    if not (episode_name and episode_resolution and release_group):
        return (None,)*4

    episode_name = episode_name[0].strip()
    episode_resolution = int(episode_resolution)

    if anime_name not in episode_name:
        for anime_alt_name in anime_alt_names:
            if anime_alt_name in episode_name:
                episode_name = episode_name.replace(anime_alt_name.strip(), anime_name)

    if anime_name not in episode_name:
        return (None,)*4

    return original_episode_name.strip(), episode_name, episode_resolution, release_group

if __name__ == "__main__":
    print(extract_names("[Marukazoku][Chibi Maruko-chan II][1326][2021.02.20][BIG5][1080P][MP4].mp4", "Chibi Maruko-chan II"))
