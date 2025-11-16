// connect-integration.js
import { Connect } from "https://cdn.openbanking.mastercard.com/js/connect-web-sdk@2.2.0/mastercard-connect-esm.min.js";

// Define your event handlers
const eventHandlers = {
  onDone: (event) => {
    // This function is called when the connection is successful
    console.log("Connection successful!");
  },
  onCancel: (event) => {
    // This function is called if the user cancels the process
    console.log("User cancelled");
  },
  onError: (event) => {
    // This function is called if an error occurs
    console.log("Error occurred");
  },
};

// Function to launch Connect
export function launchConnect(url) {
  Connect.launch(url, eventHandlers, {
    popup: true,
    popupOptions: {
      width: 520, // Width in pixels
      height: 720, // Height in pixels
    },

    redirectUrl: "https://localhost:8000",
  });
}
