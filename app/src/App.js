import React, { useEffect, useState } from 'react';
import './App.css';
import CandyMachine from './CandyMachine';


const App = () => {
  /* using wallet address as a state to decide whether to render connect wallet
     button or not
  */
  const [walletAddress, setWalletAddress] = useState(null);

  const checkIfWalletIsConnected = async () => {
    try {
      const { solana } = window;
      if (solana) {
        if (solana.isPhantom) {
          console.log("Phantom Wallet found!");

          const response = await solana.connect({ onlyIfTrusted: true });
          console.log(
            'Connected with public key:',
            response.publicKey.toString()
          );

          setWalletAddress(response.publicKey.toString());

        } else {
          alert("Please Use a Phantom Wallet!!");
        }
      } else {
        alert('Solana Phantom wallet not found! Get a phantom wallet');
      }
    } catch (error) {
      console.log(error);
    }
  };

  /* Connecting the wallet for the first time -- sign Up */

  const connectWallet = async () => {
    const { solana } = window;

    if (solana) {
      const response = await solana.connect();
      console.log('Connected with public key: ', response.publicKey.toString());
      setWalletAddress(response.publicKey.toString());
    } else {
      alert("Get a Phantom Solana wallet!!!")
    }
  };


  const renderNotConnectedContainer = () => (
    <button
      className="cta-button connect-wallet-button"
      onClick={connectWallet}
    >
      Connect to wallet
    </button>
  );

  useEffect(() => {
    const onLoad = async () => {
      await checkIfWalletIsConnected();
    };
    window.addEventListener('load', onLoad);
    return () => window.removeEventListener('load', onLoad);
  }, []);


  return (
    <div className="App">
      <div className="container">
        <div className="header-container">
          <p className="header">🏐 Your NFT Drop</p>
          <p className="sub-text">Get your Cool NFT</p>
          {/*Rendering the connect wallet button, only to connect the wallet for the first time*/}
          {/* Added this condition to render connect wallet button only when no wallet info is procured*/}
          {!walletAddress && renderNotConnectedContainer()}
        </div>
        {walletAddress && <CandyMachine walletAddress={window.solana} />}
      </div>
    </div>
  );
};

export default App;
