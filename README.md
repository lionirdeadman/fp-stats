# fp-stats

`flathub-application-cloner.py`:This script clones all non-EOL applications on Flathub. 

`flathub-runtime-information-compiler.py`:This script uses all of those repositories and compiles a JSON file which categories the runtimes and subdivides 
it into their versions which contain a list of all applications using that version.

## runtime-information format

It's a simple JSON which ressembles this
```
{
    "Freedesktop": {
        "org.freedesktop.Platform//20.08": [
            "tld.domain.app"
        ]
    }
}
```

# License

## Data
I believe that all data produced through these tools are free of copyright. There is no creativity being used here therefore there is no copyright. I waive all rights
with regards to those if necessary.

## Code
I chose LGPLv2.1 because it seemed to me to be the most compatible *GPL license and I wanted to keep it free software so I didn't choose permissive. 
I'm willing to change that if needed for a good cause.
