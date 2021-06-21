# fp-stats

`flathub-application-cloner.py`:This script clones all non-EOL applications on Flathub. 

`flathub-runtime-information-compiler.py`:This script uses all of those repositories and compiles a JSON file which categories the runtimes and subdivides 
it into their versions which contain a list of all applications using that version.

`flathub-runtime-summarize.py`:This script uses the JSON produced by `flathub-runtime-information-compiler` to show a simple output of the number of applications
using each runtime

`flathub-architecture-information-compiler.py`:This script uses all of those repositories and compiles a JSON file which categories the applications by their architectures.

`flathub-architecture-summarize.py`:This script uses the JSON produced by `flathub-architecture-information-compiler` to show a simple output of the number of applications
using each architecture.

## Data produced by these tools

They can be found [here](https://github.com/lionirdeadman/fp-stats/tree/data)

## Code
I chose LGPLv2.1 because it seemed to me to be the most compatible *GPL license and I wanted to keep it free software so I didn't choose permissive. 
I'm willing to change that if needed for a good cause.
