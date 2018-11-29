# Meeting Protocols

## Nov. 20 2018

1. We brainstormed the following ideas: classifying music genres from billboard songs, generating new possibly cheesy song lyrics, making tools to convert simple text into fancy text, making tools to help prevent people from plagiarizing

2. We all really liked the idea of generating cheesy or nice songs based on the personality of a person. We could make some inferences on the personality using the Twitter API given the user's twitter username. We also wanted to implement a Telegram bot to communicate this song with the user. This is where we stopped.

## Nov. 29 2018

1. We discussed further ideas for the exact implementation techniques for our project. We brainstormed using a Recursive Neural Network (RNN) with word-embedding to generate words of music related to one another. We could then use these vector spaces to generate lyrics of songs. We found an already developed implementation of this here: https://github.com/minimaxir/textgenrnn.

2. Since this is already developed, we suggested using this on our project and perhaps optimizing it for our purposes.

3. However, as a counter-argument, we realized that using RNNs might be counter-productive since they do not represent the crux of what we learned in our ANLP module. We mostly learned statistical/probabilistic techniques and will not be delving into neural networks significantly. Therefore, it might not make sense to take a neural-network-centric approach.

4. This brings us back to using "simpler" models such as n-gram text generation, Naive Bayes, HMMs, etc., for our project. However, we are uncertain of how we should go about this and how realistic it is for us to develop a complex project with these models.

5. We proposed developing a very simple implementation of our idea for now and perhaps deepening this further by implementing it as one of our group project modules or PMs. This would be a natural continuation of our current work and would therefore be efficient for the future.

6. To get a realistic idea of what we should do for our current ANLP project, we decided that we should consult Tatjana and ask her about her views on what is reasonable for us to implement given the skills we learned from this module. We propose to do this tomorrow, on Friday Nov 30. 2018. We hope that this will give us clarity on a reasonable task for the ANLP project which could be expanded later on as a PM.
