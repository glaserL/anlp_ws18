## Frequency Analysis

Using kaggle data as preliminary data, we had performed most frequent word analysis on music genres using all the data we had.

To do this, we firstly tokenized lyrics and then removed non-alphanumeric characters. Next, we removed lyrics-specific tokens such as "chorus" and "verse". Finally, we removed common stop-words such as "i" and "he".

With the resulting tokens, we then extracted tokens that were unique to each genre in order to display key differences between the genres.

The corresponding WordClouds can be seen below:

**1. Hip-Hop**

<img src = "/data/img/cloudhipPlain.png" width = "500">

**2. Country**

<img src = "/data/img/cloudcountryPlain.png" width = "500">

We also experimented using more exciting masks for word-clouds.

**1. Hip-Hop (Biggie)**

<img src = "/data/img/cloudHipMask.png" width = "500">

**2. Rock (Guitar)**

<img src = "/data/img/cloudRock.png" width = "500">
