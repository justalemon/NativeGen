# NativeGen<br>[![GitHub Actions][actions-img]][actions-url] [![Patreon][patreon-img]][patreon-url] [![PayPal][paypal-img]][paypal-url] [![Discord][discord-img]][discord-url]

> NOTICE: NativeGen has been deprecated and has been merged with [Collei](https://github.com/justalemon/Collei)
> 
> You can invoke Collei's native generator with similar parameters to NativeGen
> ```
> collei natives "OutputFile.cs" shvdn
> ```
> 
> You can run `collei natives --help` to see the parameters that have been changed after the merge.

NativeGen is a simple Python application for generating list of natives. It supports SHVDN 2 and 3 Enums, FiveM Mono Enums, Lua Stubs and Lua Caller functions.

## Download

* [GitHub Actions (Windows)](https://nightly.link/justalemon/NativeGen/workflows/main/master/NativeGen-Windows.zip)
* [GitHub Actions (Ubuntu & Derivatives)](https://nightly.link/justalemon/NativeGen/workflows/main/master/NativeGen-Ubuntu.zip)

## Installation

Open the compressed file and extract the file called `nativegen.exe` (Windows) or `nativegen` (Ubuntu and Derivatives) where you need it.

A proper installer will be added later if needed.

## Usage

Run NativeGen with the `--help` parameter to see a list of available parameters.

The minimal way to run NativeGen is

> nativegen[.exe] "OutputFile.cs" shvdn

Where the first parameter is the output file, and the second parameter is the format. You can see the different formats available by running the program with the `--help` parameter.

[actions-img]: https://img.shields.io/github/actions/workflow/status/justalemon/NativeGen/main.yml?branch=master&label=actions
[actions-url]: https://github.com/justalemon/NativeGen/actions
[patreon-img]: https://img.shields.io/badge/support-patreon-FF424D.svg
[patreon-url]: https://www.patreon.com/lemonchan
[paypal-img]: https://img.shields.io/badge/support-paypal-0079C1.svg
[paypal-url]: https://paypal.me/justalemon
[discord-img]: https://img.shields.io/badge/discord-join-7289DA.svg
[discord-url]: https://discord.gg/Cf6sspj
