import subprocess


def document_to_html(name, format='txt'):
    command = "/usr/bin/abiword --to={} --to-name=fd://1 {}".format(format, name)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    html = p.stdout.readlines()
    return b"".join(html)
