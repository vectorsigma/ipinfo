# ipinfo: All about an IPv4 address

This tool's purpose is to take in an IPv4 address on the command line,
and using a variety of techniques and tools, tell you everything it
can about that address.

## General use case

This tool is designed to be driven in a shell script, looping through a
list of IP addresses, gleaned from wherever.

e.g.:

```
for ip in $(cat addresses); do
	ipinfo $ip | tee -a ipinfo.out
done
```

Chances are good that this tool will be useful to infosec blue team type folks
during investigations or incident response.

## Design

Information sources will typically be divided into two camps:

1. Information you can gather directly from the Internet infrastructure itself.
2. Information you can get only from specific services on the 'net.

As such, functionality is grouped into two different modules:

1. local (checks that do not rely on specialized databases)
2. remote (checks do)

One day, if there's enough use cases, there will be support hacked in for
commerical systems as well.  The module would likely be: `commercial` to
distinguish it.

## Warnings

*N.B.:* This tool is not designed to be stealthy.  Do not use it in cases
of blackhattery, or on networks where you wish to remain unseen.  This tool
features very little limiting, no proxy support, or really anything of the sort
at this time, and it is loud and announces itself appropriately to any services
it uses.

I am also not a well trained python developer.  I would consider much of this
code to be suspect, at best.  I wrote this little utility to give me a reason
to learn Python a bit better.  Pull requests for fixing the lack of pythonic
or idiomatic code are greatly appreciated.
