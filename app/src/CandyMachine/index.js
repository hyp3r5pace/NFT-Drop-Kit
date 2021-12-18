import React, { useEffect, useState } from 'react';
import { Connection, PublicKey } from '@solana/web3.js';
import { getProvider, Program, Provider, web3 } from '@project-serum/anchor';
import { MintLayout, TOKEN_PROGRAM_ID, Token } from '@solana/spl-token';
import { programs } from '@metaplex/js';
import './CandyMachine.css';
import {
  candyMachineProgram,
  TOKEN_METADATA_PROGRAM_ID,
  SPL_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID,
} from './helpers';
import { set } from '@project-serum/anchor/dist/cjs/utils/features';
import CountdownTimer from '../CountdownTimer';

const {
  metadata: { Metadata, MetadataProgram },
} = programs;

const config = new web3.PublicKey(process.env.REACT_APP_CANDY_MACHINE_CONFIG);
const { SystemProgram } = web3;
const opts = {
  preflightCommitment: 'processed',
};

const MAX_NAME_LENGTH = 32;
const MAX_URI_LENGTH = 200;
const MAX_SYMBOL_LENGTH = 10;
const MAX_CREATOR_LEN = 32 + 1 + 1;

const CandyMachine = ({ walletAddress }) => {
  // Actions

  const [machineStats, setMachineStats] = useState(null);
  // state property to store minted nfts
  const [mints, setMints] = useState([]);

  // loading states
  const [isMinting, setIsMinting] = useState(false);
  const [isLoadingMints, setIsLoadingMints] = useState(false);


  const fetchHashTable = async (hash, metadataEnabled) => {
    const connection = new web3.Connection(
      process.env.REACT_APP_SOLANA_RPC_HOST
    );

    const metadataAccounts = await MetadataProgram.getProgramAccounts(
      connection,
      {
        filters: [
          {
            memcmp: {
              offset:
                1 +
                32 +
                32 +
                4 +
                MAX_NAME_LENGTH +
                4 +
                MAX_URI_LENGTH +
                4 +
                MAX_SYMBOL_LENGTH +
                2 +
                1 +
                4 +
                0 * MAX_CREATOR_LEN,
              bytes: hash,
            },
          },
        ],
      }
    );

    const mintHashes = [];

    for (let index = 0; index < metadataAccounts.length; index++) {
      const account = metadataAccounts[index];
      const accountInfo = await connection.getParsedAccountInfo(account.pubkey);
      const metadata = new Metadata(hash.toString(), accountInfo.value);
      if (metadataEnabled) mintHashes.push(metadata.data);
      else mintHashes.push(metadata.data.mint);
    }

    return mintHashes;
  };

  const getMetadata = async (mint) => {
    return (
      await PublicKey.findProgramAddress(
        [
          Buffer.from('metadata'),
          TOKEN_METADATA_PROGRAM_ID.toBuffer(),
          mint.toBuffer(),
        ],
        TOKEN_METADATA_PROGRAM_ID
      )
    )[0];
  };

  const getMasterEdition = async (mint) => {
    return (
      await PublicKey.findProgramAddress(
        [
          Buffer.from('metadata'),
          TOKEN_METADATA_PROGRAM_ID.toBuffer(),
          mint.toBuffer(),
          Buffer.from('edition'),
        ],
        TOKEN_METADATA_PROGRAM_ID
      )
    )[0];
  };

  const getTokenWallet = async (wallet, mint) => {
    return (
      await web3.PublicKey.findProgramAddress(
        [wallet.toBuffer(), TOKEN_PROGRAM_ID.toBuffer(), mint.toBuffer()],
        SPL_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID
      )
    )[0];
  };

  const mintToken = async () => {
    try {
      // setting the minting loading state
      setIsMinting(true);

      const mint = web3.Keypair.generate();
      const token = await getTokenWallet(
        walletAddress.publicKey,
        mint.publicKey
      );
      const metadata = await getMetadata(mint.publicKey);
      const masterEdition = await getMasterEdition(mint.publicKey);
      const rpcHost = process.env.REACT_APP_SOLANA_RPC_HOST;
      const connection = new Connection(rpcHost);
      const rent = await connection.getMinimumBalanceForRentExemption(
        MintLayout.span
      );

      const accounts = {
        config,
        candyMachine: process.env.REACT_APP_CANDY_MACHINE_ID,
        payer: walletAddress.publicKey,
        wallet: process.env.REACT_APP_TREASURY_ADDRESS,
        mint: mint.publicKey,
        metadata,
        masterEdition,
        mintAuthority: walletAddress.publicKey,
        updateAuthority: walletAddress.publicKey,
        tokenMetadataProgram: TOKEN_METADATA_PROGRAM_ID,
        tokenProgram: TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
        rent: web3.SYSVAR_RENT_PUBKEY,
        clock: web3.SYSVAR_CLOCK_PUBKEY,
      };

      const signers = [mint];
      const instructions = [
        web3.SystemProgram.createAccount({
          fromPubkey: walletAddress.publicKey,
          newAccountPubkey: mint.publicKey,
          space: MintLayout.span,
          lamports: rent,
          programId: TOKEN_PROGRAM_ID,
        }),
        Token.createInitMintInstruction(
          TOKEN_PROGRAM_ID,
          mint.publicKey,
          0,
          walletAddress.publicKey,
          walletAddress.publicKey
        ),
        createAssociatedTokenAccountInstruction(
          token,
          walletAddress.publicKey,
          walletAddress.publicKey,
          mint.publicKey
        ),
        Token.createMintToInstruction(
          TOKEN_PROGRAM_ID,
          mint.publicKey,
          token,
          walletAddress.publicKey,
          [],
          1
        ),
      ];

      const provider = getProvider();
      const idl = await Program.fetchIdl(candyMachineProgram, provider);
      const program = new Program(idl, candyMachineProgram, provider);

      const txn = await program.rpc.mintNft({
        accounts,
        signers,
        instructions,
      });

      console.log('txn:', txn);

      // Setup listener
      connection.onSignatureWithOptions(
        txn,
        async (notification, context) => {
          if (notification.type === 'status') {
            console.log('Receievd status event');

            const { result } = notification;
            if (!result.err) {
              console.log('NFT Minted!');
              alert('NFT Minting completed!!');
              setIsMinting(false);
              // updating the meta data of candy machine displayed
              await getCandyMachineState();
            }
          }
        },
        { commitment: 'processed' }
      );
    } catch (error) {
      let message = error.msg || 'Minting failed! Please try again!';

      // there was a error during the minting
      setIsMinting(false);

      if (!error.msg) {
        if (error.message.indexOf('0x138')) {
        } else if (error.message.indexOf('0x137')) {
          message = `SOLD OUT!`;
        } else if (error.message.indexOf('0x135')) {
          message = `Insufficient funds to mint. Please fund your wallet.`;
        }
      } else {
        if (error.code === 311) {
          message = `SOLD OUT!`;
        } else if (error.code === 312) {
          message = `Minting period hasn't started yet.`;
        }
      }

      console.warn(message);
      alert(`${message}`);
    }
  };

  const createAssociatedTokenAccountInstruction = (
    associatedTokenAddress,
    payer,
    walletAddress,
    splTokenMintAddress
  ) => {
    const keys = [
      { pubkey: payer, isSigner: true, isWritable: true },
      { pubkey: associatedTokenAddress, isSigner: false, isWritable: true },
      { pubkey: walletAddress, isSigner: false, isWritable: false },
      { pubkey: splTokenMintAddress, isSigner: false, isWritable: false },
      {
        pubkey: web3.SystemProgram.programId,
        isSigner: false,
        isWritable: false,
      },
      { pubkey: TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
      {
        pubkey: web3.SYSVAR_RENT_PUBKEY,
        isSigner: false,
        isWritable: false,
      },
    ];
    return new web3.TransactionInstruction({
      keys,
      programId: SPL_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID,
      data: Buffer.from([]),
    });
  };

  useEffect(() => {
    getCandyMachineState();
  }, []);

  const getProvider = () => {
    const rpcHost = process.env.REACT_APP_SOLANA_RPC_HOST;
    // create a new connection object
    const connection = new Connection(rpcHost);
    
    // Create a new provider object
    const provider = new Provider(
      connection,
      window.solana,
      opts.preflightCommitment
    );

    return provider;
  };

  const getCandyMachineState = async () => {
    const provider = getProvider();
    
    // get metadata about the deployed candy machine program
    const idl = await Program.fetchIdl(candyMachineProgram, provider);

    // create a program that I can call
    const program = new Program(idl, candyMachineProgram, provider);

    // Fetch the metadata from the candy machine
    const candyMachine = await program.account.candyMachine.fetch(
      process.env.REACT_APP_CANDY_MACHINE_ID
    );
    
    // parse out all the metadata and log them
    const itemsAvailable = candyMachine.data.itemsAvailable.toNumber();
    const itemsRedeemed = candyMachine.itemsRedeemed.toNumber();
    const itemsRemaining = itemsAvailable - itemsRedeemed;
    const goLiveData = candyMachine.data.goLiveDate.toNumber();

    const goLiveDateTimeString = `${new Date(
      goLiveData * 1000
    ).toLocaleDateString('en-GB', {month: '2-digit',day: '2-digit',year: 'numeric'})} @ ${new Date(
      goLiveData * 1000
    ).toLocaleTimeString()}`;

    setMachineStats({
      itemsAvailable,
      itemsRedeemed,
      itemsRemaining,
      goLiveData,
      goLiveDateTimeString,
    });

    console.log({
      itemsAvailable,
      itemsRedeemed,
      itemsRemaining,
      goLiveData,
      goLiveDateTimeString
    });

    setIsLoadingMints(true);

    const data = await fetchHashTable(
      process.env.REACT_APP_CANDY_MACHINE_ID,
      true
    );

    if (data.length !== 0) {
      for (const mint of data) {
        console.log(mint.data)
        const response = await fetch(mint.data.uri);
        const parse = await response.json();
        console.log("Past minted NFT ", mint)

        // this checks is done to prevent adding of same mint twice
        if (!mints.find((mint) => mint.image === parse.image)) {
          setMints((prevState) => [...prevState, parse])
        }
      }
    }
    setIsLoadingMints(false);
  };


  // function to give component displaying the minted items
  const renderMintedItems = () => (
    <div className="gif-container">
      <p className="sub-text">Minted Items ✨</p>
      <div className="gif-grid">
        {mints.map((mint) => (
          <div className="gif-item" key={mint.image}>
            <figure>
              <img src={mint.image} alt={`Minted NFT ${mint.image}`} />
              <figcaption>{mint.name}</figcaption>
            </figure>
          </div>
        ))}
      </div>
    </div>
  );

  // render the countdown timer
  const renderDropTime  = () => {
    // get the current date/time and drop date/time in JS date object
    const currentDate = new Date();
    const dropDate = new Date(machineStats.goLiveData*1000);

    if (currentDate < dropDate) {
      console.log("Before drop date!");
      return <CountdownTimer dropDate={dropDate} />;
    }

    return <p>{`Drop Date: ${machineStats.goLiveDateTimeString}`}</p>

  };

  // function to check if drop date arrived
  // it helps to know if mint NFT button should be kept disabled
  const checkIfDropDateArrived = () => {
    const currentDate = new Date();
    const dropDate = new Date(machineStats.goLiveData*1000);
    return (currentDate < dropDate);
  };

  return (
    machineStats && (
    <div className="machine-container">
      {renderDropTime()}
      {<p>{`Items Minted: ${machineStats.itemsRedeemed} / ${machineStats.itemsAvailable}`}</p>}
      {machineStats.itemsRedeemed === machineStats.itemsAvailable ? (
        <p className="sub-text">Sold Out 🙊</p>
      ) : (
      <button className="cta-button mint-button" onClick={mintToken} disabled={isMinting || checkIfDropDateArrived()}>
        Mint NFT
      </button>
      )}
      {/* component to display the images of the minted items */}
      {isLoadingMints && <p>LOADING MINTS...</p>}
      {mints.length > 0 && renderMintedItems()}
    </div>
    )
  );
};

export default CandyMachine;