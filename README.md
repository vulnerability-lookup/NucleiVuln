# NucleiVuln

A client designed to retrieve vulnerability-related information from the Nuclei Git repository of templates.
The retrieved data is then transmitted to the
[Vulnerability-Lookup](https://github.com/cve-search/vulnerability-lookup) API as sightings.

Templates form the core of the Nuclei scanner. When a template is linked to a vulnerability, the resulting detection
(observation) is classified as _confirmed_, signifying a higher level of certainty compared to the _seen_ classification.
More information about the sightings:

- [Corresponding MISP taxonomy](https://github.com/MISP/misp-taxonomies/blob/fd2fbaf2a450e42a490551e5a8e2fa6df039a6b8/vulnerability/machinetag.json#L26-L63)
- [Vulnerability-Lookup documentation](https://vulnerability-lookup.readthedocs.io/en/latest/sightings.html#sightings)


## Installation

[pipx](https://github.com/pypa/pipx) is an easy way to install and run Python applications in isolated environments.
It's easy to [install](https://github.com/pypa/pipx?tab=readme-ov-file#on-linux).

```bash
$ pipx install NucleiVuln
$ export NUCLEIVULN_CONFIG=~/.NucleiVuln/conf.py
$ git clone https://github.com/projectdiscovery/nuclei-templates.git templates
```

The configuration for NucleiVuln should be defined in a Python file (e.g., ``~/.NucleiVuln/conf.py``).
You must then set an environment variable (``NUCLEIVULN_CONFIG``) with the full path to this file.

## Usage

```bash
$ NucleiVuln --help
usage: NucleiVuln [-h] [--init]

Find new Nuclei templates related to a vulnerability in a Git repository.

options:
  -h, --help  show this help message and exit
  --init      Find Nuclei templates even if no new commits were detected.
```


## License

[NucleiVuln](https://github.com/CIRCL/NucleiVuln) is licensed under
[GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.html)

~~~
Copyright (c) 2024 Computer Incident Response Center Luxembourg (CIRCL)
Copyright (C) 2024 Cédric Bonhomme - https://github.com/cedricbonhomme
~~~
