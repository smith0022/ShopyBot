import React, { useState } from "react";
import "./Chatbot.css"; // Import your CSS file
import io from "socket.io-client";
import Dictaphone from "./Dictophone";
import image from "/home/cutesaggisture/amazon-hackon/Search-Engine-And-Recommendation-system-on-Amazon-Product/frontend/src/componenets/Untitled (1).png";
const socket = io("http://localhost:5001");

function Chatbot() {
  const getCurrentTime = () => {
    const currentTime = new Date();
    return currentTime.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };
  const [conversation, setConversation] = useState([
    {
      text: "Hi! 👋 it's great to see you! How can I help you?",
      sender: "chatbot",
      time: getCurrentTime(),
      image: "",
    },
  ]);
  const [inputText, setInputText] = useState("");

  const handleInputChange = (event) => {
    console.log(event.target);
    setInputText(event.target.value);
    const newwMessage = {
      text: event.target.value,
      sender: "user",
      time: getCurrentTime(),
      image: "",
    };
    setConversation([...conversation, newwMessage]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(inputText);
    console.log("b4 ");
    console.log(conversation);

    socket.emit("response", inputText);
    socket.on("response", (data) => {
      const newMessage = {
        text: data[0],
        sender: "chatbot",
        time: getCurrentTime(),
        image: data[1],
      };

      setConversation([...conversation, newMessage]);
      setInputText("");
      return () => {
        socket.off("response");
      };
    });
    console.log("after ");
    console.log(conversation);
    if (inputText.trim() === "") return;

    // // Clear input field
    // setInputText("");

    // // Generate and add chatbot response
    // setTimeout(() => {
    //   const response = generateResponse(inputText);
    //   const botMessage = {
    //     text: response,
    //     sender: "chatbot",
    //     time: getCurrentTime(),
    //   };
    //   setConversation([...conversation, botMessage]);
    // }, 500); // Simulating some delay before getting the response
  };

  const generateResponse = (input) => {
    // Your response generation logic here
    const responses = [
      "Hello, how can I help you today? 😊",
      "I'm sorry, I didn't understand your question. Could you please rephrase it? 😕",
      // Add more responses here...
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  // Existing imports and component definition...

  return (
    <div className="chatbot-container">
      <div id="header">
        <h1>Chatbot</h1>
        <img src={image} style={{ width: "3rem", height: "3rem" }} />
      </div>
      <div id="chatbot">
        <div id="conversation">
          {conversation.map((message, index) => (
            <div
              key={index}
              className={`chatbot-message ${
                message.sender === "chatbot" ? "chatbot" : "user-message"
              }`}
            >
              <p className="chatbot-text" senttime={message.time}>
                {message.text}
              </p>
              <br />
              {message.image === "" ? null : (
                <img
                  src={message.image}
                  style={{
                    width: "5rem",
                    height: "4rem",
                    marginTop: "1.25rem",
                    borderRadius: "1rem",
                    marginLeft: "0.25rem",
                  }}
                />
              )}
            </div>
          ))}
        </div>
        <form id="input-form" onSubmit={handleSubmit}>
          <div className="message-container">
            {" "}
            {/* Replace message-container with div */}
            <input
              id="input-field"
              type="text"
              placeholder="Type your message here"
              value={inputText}
              onChange={handleInputChange}
            />
            <button id="submit-button" type="submit">
              <img className="send-icon" src="send-message.png" alt="" />
            </button>
          </div>
          <Dictaphone text={setInputText} />
        </form>
      </div>
    </div>
  );
}

export default Chatbot;
