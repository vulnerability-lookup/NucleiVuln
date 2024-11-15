# NucleiVuln

A client designed to retrieve vulnerability-related information from the Nuclei Git repository of templates.
The gathered data is subsequently transmitted to the
[Vulnerability-Lookup](https://github.com/cve-search/vulnerability-lookup) API.


## Usage

### Installation

[pipx](https://github.com/pypa/pipx) is an easy way to install and run Python applications in isolated environments.
It's easy to [install](https://github.com/pypa/pipx?tab=readme-ov-file#on-linux).

```bash
$ pipx install NucleiVuln
$ export NUCLEIVULN_CONFIG=~/.NucleiVuln/conf.py
$ git clone https://github.com/projectdiscovery/nuclei-templates.git templates
```

The configuration for NucleiVuln should be defined in a Python file (e.g., ``~/.NucleiVuln/conf.py``).
You must then set an environment variable (``NUCLEIVULN_CONFIG``) with the full path to this file.


## License

[NucleiVuln](https://github.com/CIRCL/NucleiVuln) is licensed under
[GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.html)

~~~
Copyright (c) 2024 Computer Incident Response Center Luxembourg (CIRCL)
Copyright (C) 2024 Cédric Bonhomme - https://github.com/cedricbonhomme
~~~
