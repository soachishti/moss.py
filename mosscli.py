import click
import logging
import mosspy

from configparser import ConfigParser

@click.command()
@click.option("--base", type=click.Path(exists=True, readable=True), multiple=True)
@click.option("--report", type=click.Path(exists=False, writable=True))
@click.option("--download", type=click.Path(exists=False, writable=True))
@click.argument("language", type=click.Choice(list(mosspy.Moss.languages)))
@click.argument("files", nargs=-1)
def moss(base, report, download, language, files):
    config_ini = click.get_app_dir("moss.ini")
    parser = ConfigParser()
    parser.read([config_ini])
    if "SERVER" not in parser or "userid" not in parser["SERVER"]:
        click.echo(click.style(f"missing userid SERVER section in {config_ini}", fg='red'))
        exit(2)

    m = mosspy.Moss(parser["SERVER"]["userid"], language)
    for file in files:
        m.addFilesByWildcard(file)

    for b in base:
        m.addBaseFile(b)

    with click.progressbar(length=len(m.files), label="uploading") as bar:
        url = m.send(lambda path, name: bar.update(1, name))

    print(url)

    if report:
        m.saveWebPage(url, report)

    if download:
        with click.progressbar(length=10101010101010101010, label="downloading") as bar:
            left_max = 10
            def update_bar(left):
                nonlocal left_max
                if left > left_max:
                    left_max = left
                bar.length = left_max
                bar.update(1)
            mosspy.download_report(url, download, connections=8, log_level=logging.INFO,
                    on_read2=lambda u, left: update_bar(left))

if __name__ == '__main__':
    moss()
