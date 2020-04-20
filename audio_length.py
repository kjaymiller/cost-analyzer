import mutagen
import click
from pathlib import Path


@click.command()
@click.argument('directory')
@click.option('--cost', '-c', default=0.00, help='The cost per file to calculate at the bottom')
@click.option('--extension', '-e', default='.mp3', help='The audio file that we be looking up')
@click.option('--output', '-o', default='', help='The output file to be calculated. If empty, will be the <DIRECTORY>-audio-costs.txt')
def process_file_length(directory, cost, extension, output):
    """Todo: Add Support for Multiple File Types"""
    # Get All Files of Extension in Directory
    audio_files = Path(directory).rglob(f'*{extension}')
    audio_list = []
    total_minutes = 0
    total_cost = 0

    for audio_file in audio_files:
        if audio_file.suffix == extension:
            audio = mutagen.File(audio_file)
            audio_length = round(audio.info.length)
            audio_file_cost = cost * audio_length
            total_minutes += audio_length
            total_cost += audio_file_cost
            audio_list.append(f'{audio_file} - {audio_length} - {audio_file_cost}')

    audio_list.append(f'Grand Total: {total_minutes/60} minutes - ${round(total_cost, 2)}')

    if not output:
        dir_path = Path(directory)
        output = dir_path.joinpath(f'{dir_path.name}-audio-calc.txt')

    with open(output, 'w') as output_file:
         output_file.write('\n'.join(audio_list))

if __name__ == '__main__':
    process_file_length()
