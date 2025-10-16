// Firebase Web SDK config
const firebaseConfig = {
    apiKey: "AIzaSyDZSixOAT-st0B1pgKOXYyRQiPPp_31u6o",
    authDomain: "smartcampus-bbd3f.firebaseapp.com",
    databaseURL: "https://smartcampus-bbd3f-default-rtdb.firebaseio.com",
    projectId: "smartcampus-bbd3f",
    storageBucket: "smartcampus-bbd3f.firebasestorage.app",
    messagingSenderId: "873396415589",
    appId: "1:873396415589:web:49c3de361749f781706a8c",
    measurementId: "G-QNB7T7ZPTB"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const database = firebase.database(app);
