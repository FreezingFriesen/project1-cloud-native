
console.log("firebase.js loaded");

// Firebase setup 
const firebaseConfig = {
  apiKey: "AIzaSyDDmkMUTzwkW0UPQJNWnTEcNfXmIQSEJHM",
  authDomain: "cloud-computing-ced36.firebaseapp.com",
  projectId: "cloud-computing-ced36",
  storageBucket: "cloud-computing-ced36.firebasestorage.app",
  messagingSenderId: "761394230012",
  appId: "1:761394230012:web:31f942837f49ae774a5d79"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const googleProvider = new firebase.auth.GoogleAuthProvider();
const githubProvider = new firebase.auth.GithubAuthProvider();


window.handleGoogleLogin = function () {
  console.log("Google clicked");

  auth.signInWithPopup(googleProvider)
    .then(result => {
      alert("Logged in as " + result.user.email);
    })
    .catch(error => console.error(error));
};

window.handleGithubLogin = function () {
  console.log("GitHub clicked");

  auth.signInWithPopup(githubProvider)
    .then(result => {
      alert("Logged in as " + result.user.email);
    })
    .catch(error => console.error(error));
};