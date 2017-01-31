# Use MediaWiki External Links for Solr Boosting

This is a simple Python script for extracting popularity scores based on external links in MediaWiki dumps and saving them in a sorted key/value text file.  It is designed to be used as a ranking component for search engines that use Solr (such as YaCy).

## Usage instructions for YaCy

Download a SQL dump of a MediaWiki `externallinks` table.  [RSS feed for English Wikipedia is here](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-externallinks.sql.gz-rss.xml) but don't forget to replace `http` with `https` in the link the RSS feed provides.  [Other Wikimedia wikis are here](https://dumps.wikimedia.org/).

If you want a nice progress bar, do something like this (use a different package manager as needed):

```
sudo dnf install pv
pv enwiki-20170120-externallinks.sql.gz | gzip --decompress --stdout | ./count_hosts.py > external_wikipedia_en_host
```

If you don't want a nice progress bar, just do something like this:

```
cat enwiki-20170120-externallinks.sql.gz | gzip --decompress --stdout | ./count_hosts.py > external_wikipedia_en_host
```

Shut off YaCy.

Move `external_wikipedia_en_host` to YaCy's `DATA/INDEX/freeworld/SEGMENTS/solr_5_5/collection1/data/` directory.

Copy `DATA/INDEX/freeworld/SEGMENTS/solr_5_5/collection1/conf/schema.xml` to `DATA/INDEX/freeworld/SEGMENTS/solr_5_5/collection1/conf/schemawithwikipedia.xml`.

In `schemawithwikipedia.xml`, inside the `<types>` section, add `<fieldType name="external_host_file" class="solr.ExternalFileField" keyField="host_s" defVal="0" indexed="false" stored="false" valType="float"/>`.

In `schemawithwikipedia.xml`, inside the `<fields>` section, add `<field name="wikipedia_en_host" type="external_host_file" />`.

Edit `/home/user/QubesIncoming/offline-build-yacy/yacy_v1.91_20161017_9278_wikipedia_experiment/DATA/INDEX/freeworld/SEGMENTS/solr_5_5/collection1/core.properties`; in the line that begins `schema=`, change `schema.xml` to `schemawithwikipedia.xml`.

Start up YaCy again.  It might take a few seconds longer to boot than usual.  (Or it might not; feel free to send me test reports on this.)

Go to YaCy's Solr Ranking settings.  You can now use the field `wikipedia_en_host` in the Boost Function.

You're done!  Your YaCy peer is now compatible with Wikipedia ranking.  You should be able to replace the `external_wikipedia_en_host` file with an updated one when new Wikipedia dumps are released without shutting down YaCy first; reboot YaCy to make the new file take effect.

## Author

This script was written by Jeremy Rand.

## License

License is GPLv2+.
