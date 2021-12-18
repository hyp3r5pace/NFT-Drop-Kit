# NFT-Drop-Kit
Create your NFT drop on solana with a single command

# ABOUT
NFT DROP KIT Allows you to deploy your NFT to Solana Chain with a single command.

# Dependency
Before running the script, install the following dependency
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [node](https://nodejs.org/en/download/)
* [yarn](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable)
* [ts-node](https://www.npmjs.com/package/ts-node#installation)

# Assets
Before uploading, create a directory named 'assets' in the root of the repo and copy the assets you want to be NFT to the 'assets' directory. 

PS: The assets for now can only be .png images

# Running the script
Run the script 'deploy' to start the process of deploying your NFTS

# start the App locally
Once the NFT deployment is complete, you can start up a demo app using to mint NFT.
To start the React App, go to app directory,
* npm install
to install the NPM dependencies
and to start the app locally run
* npm run start

To be able to sucessfully mint NFT, download [phantom wallet](https://phantom.app/).

Now you have succesfully deployed your NFT on solana devnet :)

To be able to deploy the app on hosting platforms like vercel or netlify, you have to just upload the app directory to these platforms.
Also, while deploying on these platforms, copy paste the environment variables from .env file in the app directory. 

# References
[buildspace](https://buildspace.so/)  

[hackmd](https://hackmd.io/@levicook/HJcDneEWF)  

[metaplex](https://docs.metaplex.com/create-candy/introduction)  

[solana](https://github.com/solana-labs/solana)
