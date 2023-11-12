# VCP-Core
Video Content Preprocessor (VCP) enables fetching of YouTube Video Contentes including information about the video. The Framework does allow to download and process a script for further usage.


## Installation

Execute the command below:

```py -3.11 -m pip install git+https://github.com/vQid/VCP-Core.git --force-reinstall```

You might have to add the scripts installation folder to your environment variables (only once). Otherwise, you will not be able to execute the commands below...

## Usage

If preconditions are done then basically typ ```vcp --help``` to get help.

You will need to set up a configuration file. Save the ```example-cfg.yml``` locally and add API keys to the file. This configuration file is the driver of VCP.

Simply then execute:

```vcp fetch-videos <cfg.yml PATH>``` to get potential CreativeCommon Videos for processing from the YouTube API

```vcp download-videos <cfg.yml PATH>``` to download the Videos locally to the storage path defined in the cfg.yml file

```vcp enrich-chat-gpt <cfg.yml PATH>``` to generate analysed/enriched content by chat-gpt

```vcp create-shorts <cfg.yml PATH>``` to generate shorts out of the enriched file and save them in sub-folder called "shorts"






