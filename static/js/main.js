// Main JavaScript file for the Artist Pop-up Event application

let web3;
let userAccount;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Implement a simple dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });

        // Check for saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }

    // Add fade-in effect for content
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transition = 'opacity 0.5s ease-in-out';
        setTimeout(() => {
            element.style.opacity = '1';
        }, 100);
    });

    // Initialize Web3 and MetaMask connection
    initWeb3();
});

async function initWeb3() {
    if (typeof window.ethereum !== 'undefined') {
        web3 = new Web3(window.ethereum);
        const connectWalletBtn = document.getElementById('connectWalletBtn');
        if (connectWalletBtn) {
            connectWalletBtn.addEventListener('click', connectWallet);
        }
    } else {
        console.log('Please install MetaMask!');
        showError('MetaMask is not installed. Please install MetaMask to use this application.');
    }
}

async function connectWallet() {
    try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        userAccount = accounts[0];
        console.log('MetaMask connected');
        updateUIForConnectedWallet();
    } catch (error) {
        console.error('User denied account access');
        showError('Failed to connect to MetaMask. Please try again.');
    }
}

function updateUIForConnectedWallet() {
    const connectWalletBtn = document.getElementById('connectWalletBtn');
    if (connectWalletBtn) {
        connectWalletBtn.textContent = 'Wallet Connected';
        connectWalletBtn.disabled = true;
    }
    const walletAddress = document.getElementById('walletAddress');
    if (walletAddress) {
        walletAddress.textContent = `Connected: ${userAccount}`;
    }
    showSuccess('Wallet connected successfully!');
}

async function disconnectWallet() {
    userAccount = null;
    const connectWalletBtn = document.getElementById('connectWalletBtn');
    if (connectWalletBtn) {
        connectWalletBtn.textContent = 'Connect Wallet';
        connectWalletBtn.disabled = false;
    }
    const walletAddress = document.getElementById('walletAddress');
    if (walletAddress) {
        walletAddress.textContent = '';
    }
    showSuccess('Wallet disconnected successfully!');
}

async function claimArtwork(artworkId, title, description) {
    if (!web3 || !userAccount) {
        showError('Please connect your MetaMask wallet first.');
        return;
    }

    try {
        const contractABI = await fetch('/get_contract_abi').then(response => response.json());
        const contractAddress = await fetch('/get_contract_address').then(response => response.text());

        const contract = new web3.eth.Contract(contractABI, contractAddress);

        const claimFunction = contract.methods.mintNFT(userAccount, `ipfs://${artworkId}`, title, description);
        const gas = await claimFunction.estimateGas({ from: userAccount });
        const data = claimFunction.encodeABI();

        const transactionParameters = {
            to: contractAddress,
            from: userAccount,
            gas: web3.utils.toHex(gas),
            data: data,
        };

        const txHash = await window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [transactionParameters],
        });

        console.log('Artwork claimed:', txHash);
        showSuccess('Artwork claimed successfully! Transaction hash: ' + txHash);
        return txHash;
    } catch (error) {
        console.error('Error claiming artwork:', error);
        showError('Failed to claim artwork. Please try again.');
        throw error;
    }
}

async function transferArtwork(tokenId, to) {
    if (!web3 || !userAccount) {
        showError('Please connect your MetaMask wallet first.');
        return;
    }

    try {
        const contractABI = await fetch('/get_contract_abi').then(response => response.json());
        const contractAddress = await fetch('/get_contract_address').then(response => response.text());

        const contract = new web3.eth.Contract(contractABI, contractAddress);

        const transferFunction = contract.methods.transferFrom(userAccount, to, tokenId);
        const gas = await transferFunction.estimateGas({ from: userAccount });
        const data = transferFunction.encodeABI();

        const transactionParameters = {
            to: contractAddress,
            from: userAccount,
            gas: web3.utils.toHex(gas),
            data: data,
        };

        const txHash = await window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [transactionParameters],
        });

        console.log('Artwork transferred:', txHash);
        showSuccess('Artwork transferred successfully! Transaction hash: ' + txHash);
        return txHash;
    } catch (error) {
        console.error('Error transferring artwork:', error);
        showError('Failed to transfer artwork. Please try again.');
        throw error;
    }
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.role = 'alert';
    errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.insertBefore(errorDiv, document.body.firstChild);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success alert-dismissible fade show';
    successDiv.role = 'alert';
    successDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.insertBefore(successDiv, document.body.firstChild);
}

// Export functions for use in other scripts
window.claimArtwork = claimArtwork;
window.transferArtwork = transferArtwork;
window.connectWallet = connectWallet;
window.disconnectWallet = disconnectWallet;
