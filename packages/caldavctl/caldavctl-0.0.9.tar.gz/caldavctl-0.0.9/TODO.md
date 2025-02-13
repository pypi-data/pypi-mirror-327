# TODO List

* [x] Start using https://docs.python.org/3/library/zoneinfo.html instead of pytz
* [ ] Show datetime in the default timezone
* [ ] Validate the config file, maybe with structural pattern matching we cal
      also use either taplo ou pydantic libraries.
      https://www.adventuresinmachinelearning.com/streamlining-configuration-data-with-toml-in-python-applications/
        {
            'server': {
                'paxjulia': {
                    'password': 'XXXXXX',
                    'url': 'XXXX',
                    'username': 'XXXX'
                },
                'server2': {
                    ...
                }
            },
            'default': {
                'calendar': 'XXXX',
                'server': 'XXXX',
                'timezone': 'Asia/Tokyo'
            },
        }
