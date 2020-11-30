import shlex
import shutil
import subprocess
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path


def existing_audio_file(fname):
    path = Path(fname)
    exts = {'.mp3', '.m4a', '.ogg', '.flac', '.wma'}
    if path.is_file() and path.suffix in exts:
        return path
    raise ArgumentTypeError(fname)


def guess_artist_and_title(path):
    path = path.resolve()
    artist_guess = path.parent.parent.name.lower()
    if artist_guess == 'various':
        artist_guess, title_guess = path.name.lower().split('-', 2)[1:]
    else:
        title_guess = path.name.partition('-')[2].lower()
    title_guess = title_guess[:len(title_guess)-len(path.suffix)]
    return artist_guess, title_guess


def transcode(in_, out):
    cmd = f'ffmpeg -v 5 -y -i "{in_}" -acodec libmp3lame -ac 2 -ab 192k "{out}"'
    print(cmd)
    subprocess.call(shlex.split(cmd))


def retag(path, *, artist, title):
    if not path.suffix == '.mp3':
        raise NotImplementedError
    cmd = f'eyed3 --remove-all "{path}"'
    subprocess.call(shlex.split(cmd))
    cmd = f'eyed3 --artist="{artist}" --title="{title}" "{path}"'
    subprocess.call(shlex.split(cmd))


def main():
    parser = ArgumentParser()
    parser.add_argument('paths', nargs='+', type=existing_audio_file)
    args = parser.parse_args()
    guesses = {x: guess_artist_and_title(x) for x in args.paths}
    for path, (artist, title) in guesses.items():
        print(path)
        print(f'artist : {artist}')
        print(f'title  : {title}')
        k = None
        while k not in {'y', 'n'}:
            k = input('ok? [y/n] ')
        if k == 'n':
            artist = input('artist? : ') or artist
            title = input('title? : ') or title
            guesses[path] = artist, title
    dest_dir = Path('/Volumes/walkman')
    for in_, (artist, title) in guesses.items():
        out = dest_dir/f'{artist}-{title}.mp3'
        if out.exists():
            k = None
            while k not in {'y', 'n'}:
                k = input(f'{out} exists. replace? [y/n] ')
            if k == 'n':
                continue
        if in_.suffix == '.mp3':
            print(f'{in_} -> {out}')
            shutil.copy2(in_, out)
        else:
            transcode(in_, out)
        retag(out, artist=artist, title=title)
        assert out.is_file()


if __name__ == '__main__':
    main()
