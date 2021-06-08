# RSOPM-AKA Protocol Simulation

In this git, we implement a prototype system to simulate our desighed protocol RSOPM-AKA, which is a secure authenticaion protocol in a multi-cloud environmnet. Our protocl use PUF
to be the trust root rather than TPM, which is one of our innovation.

We basically make an intergrated protocol with chameleon hash funciton and ring signature under ECC. You can reproduce our work with your own IDE like pycharm or you can just use 
some useful cryptograhic primitives like Chameleon Hash Funciton under the file Cyptology. 

In the end, we declare two libraries called PyCryptodome3.9.8 and sslcrypto5.3 are principally used to implement cryptography primitives. Because the time is too tight and the code 
level of author is limited, we are sorry about the poor code qulity. And we welcome everyone to improve this git.
