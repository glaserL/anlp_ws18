# partition training data with `filter.sh`

Due to the large size of the `lyrics-2.csv` file (~350mb), it is more efficient to partition this data into smaller chunks which can then later be processed in python.

In order to partition this file efficiently, a shell script `filter.sh` can be utilized.

This is a simple regex based script which conducts grep-style searches for songs. As an example, if we wanted to partition all songs from Beyonce and output them into `test.txt`, we could execute:

```shell
$ ./filter.sh -b "lyrics-2.csv" -d "test.txt" -a "beyonce"
```

There exist more input parameters to play around with. In order to see complete documentation for this script, simply execute:

```shell
$ ./filter.sh -h
```
