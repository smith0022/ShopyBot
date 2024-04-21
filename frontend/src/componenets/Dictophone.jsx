import React from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { HiMicrophone, HiOutlineMicrophone } from "react-icons/hi2";
const Dictaphone = ({ text }) => {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }
  const handleButton = () => {
    if (!listening) {
      text(transcript);

      {
        SpeechRecognition.startListening({ continuous: true });
      }
    } else {
      text(transcript);
      {
        SpeechRecognition.stopListening();
      }
      {
        resetTranscript();
      }
    }
  };
  return (
    <div>
      {/* <p>Microphone: {listening ? "on" : "off"}</p> */}
      <button onClick={handleButton}>
        {!listening ? (
          <HiMicrophone size={"2rem"} />
        ) : (
          <HiOutlineMicrophone size={"2rem"} />
        )}
      </button>
    </div>
  );
};
export default Dictaphone;
